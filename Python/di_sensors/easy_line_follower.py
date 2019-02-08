from __future__ import print_function
from __future__ import division

# from di_sensors import line_follower
import line_follower
import pickle

'''
MUTEX HANDLING
'''
# from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

class EasyLineFollower(object):

    def __init__(self, 
        bus = "RPI_1SW", 
        module_id = -1, 
        calib_dir = '/home/pi/Dexter/',
        white_file = 'white_line.txt',
        black_file = 'black_line.txt'):
        """
        keyword params:
        bus (default "RPI_1SW") -- The I2C bus
        module_id (default -1) -- Which module to use (1 for old, 2 for new) and -1 to automatically detect
        """

        self.file_white_calibration = calib_dir + white_file
        self.file_black_calibration = calib_dir + black_file
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
        representation - raw, bivariate, weighted-avg, string
        """
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
        elif representation == 'weighted-avg':
            raw_vals = self.sensor.read_sensors()
            for i in range(self._no_vals):
                raw_vals[i] = (raw_vals[i] - self.black_calibration[i]) / (self.white_calibration[i] - self.black_calibration[i])
                if raw_vals[i] < 0: raw_vals[i] = 0.0
                if raw_vals[i] > 1: raw_vals[i] = 1.0
                raw_vals[i] = 1.0 - raw_vals[i]
            norm_vals = raw_vals

            print(norm_vals)

            numerator = sum([i * norm_vals[i] for i in range(self._no_vals)])
            denominator = float(sum(norm_vals))
            try:
                position = numerator / (denominator * (self._no_vals - 1))
            except ZeroDivisionError:
                position = 0.5

            # returns a value in [-1, 1] range with negative values
            # indicating the left of the robot and the positive
            # values the right
            return position
        elif representation == 'position-based':
            pass
        elif representation == 'string':
            pass
        else:
            pass

    def set_calibration(self, color, inplace = True):
        """
        color - white or black
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
        color - white or black
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

