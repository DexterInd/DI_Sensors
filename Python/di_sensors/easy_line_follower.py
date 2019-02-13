from __future__ import print_function
from __future__ import division

from di_sensors import line_follower
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease
import pickle

class EasyLineFollower(object):
    """
    Higher-level of abstraction class for either the :py:class:`~di_sensors.line_follower.LineFollower` or :py:class:`~di_sensors.line_follower.OldLineFollower`.
    """

    def __init__(self, 
        port = 'I2C', 
        module_id = -1, 
        calib_dir = '/home/pi/Dexter/',
        white_file = 'white_line.txt',
        black_file = 'black_line.txt',
        use_mutex = True):
        """
        Initialize a class to interface with either the :py:class:`~di_sensors.line_follower.LineFollower` or the :py:class:`~di_sensors.line_follower.OldLineFollower`.

        :param str port = "I2C": The port to which the line follower is connected. The ``"I2C"`` port corresponds to ``"RPI_1SW"`` bus. Can also choose port ``"AD1"``/``"AD2"`` only if it's connected to the GoPiGo3 and the ``module_id`` is specifically set to **2**. To find out more, check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param int module_id = -1: **-1** to automatically detect the connected line follower - this is the default value. It can also set to **1** to only use it with the old line follower (:py:class:`~di_sensors.line_follower.OldLineFollower`) or to **2** for the new line follower (:py:class:`~di_sensors.line_follower.LineFollower`) [#]_.
        :param str calib_dir = "/home/pi/Dexter/": Directory where the calibration files are saved. It already has a default value set.
        :param str white_file = "white_line.txt": The name of the calibration file for the white line.
        :param str black_file = "black_line.txt": The name of the calibration file for the black line.
        :param bool use_mutex = True: Whether to use a mutex on the sensor or not. Recommended when the same sensor is called from multiple threads/processes. It's meant for the I2C line and does not protect the file I/O in multi-threaded applications.

        Upon instantiating an object of this class, after detecting the line follower, the calibration values are read and if they are not compatible with those required for the given line follower,
        default/generic calibration values will be set for both colors computed by taking the average of the 2 extremes. 
        
        Important to keep in mind is that both line followers' 
        calibration files are incompatible, because one uses 5 sensors and the other one 6 - there are also, more factors to consider, such as the kind of sensors used in the
        line follower, but for the most part, the incompatibility comes from the different number of sensors.

        .. [#] To see what module has been detected, check :py:attr:`~di_sensors.easy_line_follower.EasyLineFollower.module_id` attribute. If it's set to 0, then no line follower has been detected.

        """

        self.file_white_calibration = calib_dir + white_file
        self.file_black_calibration = calib_dir + black_file
        self.use_mutex = use_mutex

        if port == "I2C":
            bus = "RPI_1SW"
        elif port == "AD1" and module_id == 2:
            bus = "GPG3_AD1"
        elif port == "AD2" and module_id == 2:
            bus = "GPG3_AD2"
        else:
            raise ValueError("selected port is not valid")

        ifMutexAcquire(self.use_mutex)
        try:
            self._test_dev = line_follower.LineFollower(bus)
            if module_id == 1:
                self.module_id = module_id
                self.sensor = line_follower.OldLineFollower(bus)
            elif module_id == 2:
                self.module_id = module_id
                self.sensor = line_follower.LineFollower(bus)
            elif module_id == -1:
                self.module_id = self._detect_line_follower()
                if self.module_id == 1:
                    self.sensor = line_follower.OldLineFollower(bus)
                else: # sensor_module can only be 2, because otherwise an exception is raised
                    self.sensor = line_follower.LineFollower(bus)
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        if self.module_id == 1:
            self._no_vals = 5
        else:
            self._no_vals = 6

        try:
            self.white_calibration = self.get_calibration('white', inplace=False)
            self.black_calibration = self.get_calibration('black', inplace=False)
        except ValueError:
            self.white_calibration = [1.0] * self._no_vals
            self.black_calibration = [0.0] * self._no_vals

        self._calculate_threshold()

    def _calculate_threshold(self):
        """
        calculates threshold for black and white based on the calibration data
        """
        self._threshold = [(a + b) / 2.0 for a,b in zip(self.black_calibration, self.white_calibration)]

    
    def _detect_line_follower(self):
        """
        returns
        0 - for no line follower detected
        1 - for detecting the old line follower
        2 - for detecting the new line follower
        """
        # see if the device is up and running
        device_on = False
        try:
            self._test_dev.i2c_bus.read_8()
            device_on = True
        except:
            pass
        
        if device_on is True:
            # then it means we have a line follower connected
            # we still don't know whether it is the new one or the old one
            board = 1
            try:
                if self._test_dev.get_board() == 'Line Follower':
                    board = 2
            except:
                pass
            return board
        else:
            return 0


    def read(self, representation="raw"):
        """
        Read the sensors' values from either line follower.

        :param str representation="raw": It's set by-default to ``"raw"`` , but it can also be ``"bivariate"``, ``"bivariate-str"`` or ``"weighted-avg"``.
        :raises ~exceptions.OSError: If the line follower sensor is not reachable.

        Each of the line followers' order of the sensors is the same as the one in each read method of them both: :py:meth:`di_sensors.line_follower.LineFollower.read_sensors` and :py:meth:`di_sensors.line_follower.OldLineFollower.read_sensors`.
        

        For ``representation="raw"``
            For this, raw values are returned from the line follower sensor. Values range between **0** and **1023** and there can be 5 or 6 values returned depending on what line follower sensor is used.
        
        For ``representation="bivariate"``
            In this case, a list with the length equal to the number of sensors present on the given line follower is returned. Values are either **0** (for black) or **1** (for white). 
            In order to get good results, make sure the line follower is properly calibrated.

        For ``representation="bivariate-str"``
            Same as ``"bivariate"`` except that **0** is replaced with letter `b` (for black) and **1** with `w` (for white).

        For ``representation="weighted-avg"``
            Returns a 2-element tuple. The first element is an estimated position of the line. 
            
            The estimate is computed using a weighted average of each sensor value (regardless of which line follower sensor is used), 
            so that if the black line is on the right of the line follower, the returned value will be in the **0.0-0.5** range and if it's on the left, 
            it's in the **0.5-1.0** range, thus making **0.5** the center point of the black line. Keep in mind that the sensor's orientation is determined by the order
            of the returned sensor values and not by how the sensor is positioned on the robot. 
            Check :py:meth:`~di_sensors.line_follower.LineFollower.read_sensors` and :py:meth:`~di_sensors.line_follower.OldLineFollower.read_sensors` methods to see
            how the values are returned. 
            
            If the line follower sensor ends up on a surface with an homogeneous color  (or shade of grey), the returned value will circle around **0.5**.
            
            The 2nd element is an integer taking 3 values: **1** if the line follower only detects black, **2** if it only detects white and **0** for the rest of cases.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            if representation == 'raw':
                return self.sensor.read_sensors()
            elif representation == 'bivariate':
                raw_vals = self.sensor.read_sensors()
                six_vals = [0] * self._no_vals
                for i in range(self._no_vals):
                    if raw_vals[i] > self._threshold[i]:
                        six_vals[i] = 1
                    else:
                        six_vals[i] = 0
                return six_vals
            elif representation == 'bivariate-str':
                raw_vals = self.read('bivariate')
                string_vals = ''.join(['b' if sensor_val == 0 else 'w' for sensor_val in raw_vals])
                return string_vals
            elif representation == 'weighted-avg':
                raw_vals = self.sensor.read_sensors()
                for i in range(self._no_vals):
                    raw_vals[i] = (raw_vals[i] - self.black_calibration[i]) / (self.white_calibration[i] - self.black_calibration[i])
                    if raw_vals[i] < 0: raw_vals[i] = 0.0
                    if raw_vals[i] > 1: raw_vals[i] = 1.0
                    raw_vals[i] = 1.0 - raw_vals[i]
                norm_vals = raw_vals

                numerator = sum([i * norm_vals[i] for i in range(self._no_vals)])
                denominator = float(sum(norm_vals))
                try:
                    position = numerator / (denominator * (self._no_vals - 1))
                except ZeroDivisionError:
                    position = 0.5
                
                hits = 0
                lost_line_type = 0
                for i in range(self._no_vals):
                    hits += 1 if raw_vals[i] > self._threshold[i] else 0
                if hits == self._no_vals:
                    lost_line_type = 1
                if hits == 0:
                    lost_line_type = 2

                return position, lost_line_type
            else:
                pass
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

    def set_calibration(self, color, inplace = True):
        """
        Calibrate the sensor for the given ``color`` and save the values to file.

        :param str color: Either ``"white"`` for calibrating white or ``"black"`` for black.
        :param bool inplace = True: Apply the calibration values to this instantiated object too. Use :py:attr:`~di_sensors.easy_line_follower.EasyLineFollower.white_calibration` :py:attr:`~di_sensors.easy_line_follower.EasyLineFollower.black_calibration` to access the calibration values.

        """
        vals = self.read()
        
        if color == 'white':
            fname = self.file_white_calibration
        elif color == 'black':
            fname = self.file_black_calibration
        else:
            fname = ''
        
        if fname != '':
            with open(fname, 'wb') as f:
                pickle.dump(vals, f)
                if inplace is True:
                    if color == 'white':
                        self.white_calibration = vals
                    if color == 'black':
                        self.black_calibration = vals
                    self._calculate_threshold()
    
    def get_calibration(self, color, inplace = True):
        """
        Read the calibration values from the disk for the given ``color``.

        :param str color: Either ``"white"`` for reading the calibration values for white or ``"black"`` for black.
        :param bool inplace = True: Apply the read values to this instantiated object too. Use :py:attr:`~di_sensors.easy_line_follower.EasyLineFollower.white_calibration` :py:attr:`~di_sensors.easy_line_follower.EasyLineFollower.black_calibration` to access the calibration values.
        :rtype: 5/6-element list depending on which line follower is used.
        :returns: The calibrated values for the given color.
        :raises ~exception.ValueError: When the read file is incompatible with what the line follower expects. This can happen if a line follower has been calibrated and then switched with another one of a different type (like going from the old -> new or vice-versa).

        """
        line = []
        try:
            if color == 'white':
                fname = self.file_white_calibration
            elif color == 'black':
                fname = self.file_black_calibration
            if color == 'white' or color == 'black':
                with open(fname, 'rb') as f:
                    line = pickle.load(f)
        except:
            if color == 'white':
                line = [1.0] * self._no_vals
            elif color == 'black':
                line = [0.0] * self._no_vals

        if len(line) != self._no_vals:
            raise ValueError('incompatible calibration file')
        else:
            if inplace is True:
                if color == 'white':
                    self.white_calibration = line
                if color == 'black':
                    self.black_calibration = line
                self._calculate_threshold()
            return line

