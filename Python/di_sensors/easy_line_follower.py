import easy_sensors
from I2C_mutex import Mutex
import time
from os import path
# from numpy import mean, std

try:
    from di_sensors import line_follower
except:
    # think about what we should do 
    # goal is to support both line followers seamlessly
    raise ImportError("Line Follower library not found")
    exit()

class EasyLineFollower(Sensor):
    """
    Class for interacting with the `Line Follower`_ sensor.
    With this sensor, you can make your robot follow a black line on a white background.

    The `Line Follower`_ sensor has 5 IR sensors.
    Each IR sensor is capable of diferentiating a black surface from a white one.

    In order to create an object of this class, we would do it like in the following example.

    .. code-block:: python

         # initialize an EasyGoPiGo3 object
         gpg3_obj = EasyGoPiGo3()

         # and then initialize the LineFollower object
         line_follower = gpg3_obj.init_line_follower()

         # use it however you want it
         line_follower.read_raw_sensors()

    .. warning::

         This class requires the :py:mod:`line_sensor` library.

    """

    DIR_PATH="/home/pi/Dexter/"
    # If for some reason this got installed in a weird way, 
    # then default to pi home dir
    if not path.isdir(DIR_PATH):
        DIR_PATH = "/home/pi/"

    FILE_BLACK=dir_path+'black_line.txt'
    FILE_WHITE=dir_path+'white_line.txt'
    FILE_RANGE=dir_path+'range_line.txt'

    def __init__(self, port="I2C", gpg=None, use_mutex=False):
        """
        Constructor for initalizing a :py:class:`~easygopigo3.LineFollower` object.

        :param str port = "I2C": The port to which we have connected the `Line Follower`_ sensor.
        :param easygopigo3.EasyGoPiGo3 gpg = None: The :py:class:`~easygopigo3.EasyGoPiGo3` object that we need for instantiating this object.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises ImportError: If the :py:mod:`line_follower` module couldn't be found.
        :raises TypeError: If the ``gpg`` parameter is not a :py:class:`~easygopigo3.EasyGoPiGo3` object.
        :raises IOError: If the line follower is not responding.


        The only value the ``port`` parameter can take is ``"I2C"``.

        The I2C ports' location on the `GoPiGo3`_ robot can be seen in the following graphical representation: :ref:`hardware-ports-section`.

        """
        try:
            self.set_descriptor("Line Follower")
            easy_sensors.Sensor.__init__(self, port, "INPUT", gpg, use_mutex)
            if line_sensor.read_sensor() == [-1, -1, -1, -1, -1]:
                raise IOError("Line Follower not responding")
        except:
            raise

    # Function for removing outlier values
    # For bigger std_factor_threshold, the filtering is less aggressive
    # For smaller std_factor_threshold, the filtering is more aggressive
    # std_factor_threshold must be bigger than 0
    # def _statisticalNoiseReduction(values, std_factor_threshold = 2):
    #     if len(values) == 0:
    #         return []

    #     calculated_mean = mean(values)
    #     standard_deviation = std(values)

    #     # just return if we only got constant values
    #     if standard_deviation == 0:
    #         return values

    #     # remove outlier values which are less than the average but bigger than the calculated threshold
    #     filtered_values = [element for element in values if element > mean - std_factor_threshold * standard_deviation]
    #     # the same but in the opposite direction
    #     filtered_values = [element for element in filtered_values if element < mean + std_factor_threshold * standard_deviation]

    #     return filtered_values

    def read_raw_sensors(self):
        """
        Read the 6 IR sensors of the `Line Follower`_ sensor.
        Note: the old line follower (with red board) has 5 sensors, not 6.

        :returns: A list with 5 10-bit numbers that represent the readings from the line follower device.
        :rtype: list[int]
        :raises IOError: If the line follower is not responding.

        """

        try:
            sensor_vals = line_sensor.read_sensor()
        except IOError as e:
            print(e)
            sensor_vals = [-1]*6

        if five_vals != [-1, -1, -1, -1, -1]:
            return five_vals
        else:
            raise IOError("Line Follower not responding")

    def get_white_calibration(self):
        """
        Place the `GoPiGo3`_ robot on top of a white-colored surface.
        After that, call this method for calibrating the robot on a white surface.

        :returns: A list with 5 10-bit numbers that represent the readings of line follower sensor.
        :rtype: int

        Also, for fully calibrating the sensor, the :py:class:`~easygopigo3.LineFollower.get_black_calibration` method also needs to be called.

        """
        return line_sensor.get_white_line()

    def get_black_calibration(self):
        """
        Place the `GoPiGo3`_ robot on top of a black-colored surface.
        After that, call this method for calibrating the robot on a black surface.

        :returns: A list with 5 10-bit numbers that represent the readings of line follower sensor.
        :rtype: int

        Also, for fully calibrating the sensor, the :py:class:`~easygopigo3.LineFollower.get_white_calibration` method also needs to be called.

        """
        return line_sensor.get_black_line()

    def read(self):
        """
        Reads the 5 IR sensors of the `Line Follower`_ sensor.

        :returns: A list with 5 numbers that represent the readings of the line follower device. The values are either **0** (for black) or **1** (for white).
        :rtype: list[int]

        .. warning::

             If an error occurs, a list of **5 numbers** with values set to **-1** will be returned.
             This may be caused by bad calibration values.

             Please use :py:meth:`~easygopigo3.LineFollower.get_black_calibration` or :py:meth:`~easygopigo3.LineFollower.get_white_calibration` methods before calling this method.

        """
        five_vals = scratch_line.absolute_line_pos()

        return five_vals

    def read_position(self):
        """
        Returns a string telling to which side the black line that we're following is located.

        :returns: String that's indicating the location of the black line.
        :rtype: str

        The strings this method can return are the following:

            * ``"center"`` - when the line is found in the middle.
            * ``"black"`` - when the line follower sensor only detects black surfaces.
            * ``"white"`` - when the line follower sensor only detects white surfaces.
            * ``"left"`` - when the black line is located on the left of the sensor.
            * ``"right"`` - when the black line is located on the right of the sensor.

        .. note::

            This isn't the most "intelligent" algorithm for following a black line, but it proves the point and it works.

        """
        five_vals = [-1, -1, -1, -1, -1]


        five_vals = self.read()

        if five_vals == [0, 0, 1, 0, 0] or five_vals == [0, 1, 1, 1, 0]:
            return "center"
        if five_vals == [1, 1, 1, 1, 1]:
            return "black"
        if five_vals == [0, 0, 0, 0, 0]:
            return "white"
        if five_vals == [0, 1, 1, 0, 0] or \
           five_vals == [0, 1, 0, 0, 0] or \
           five_vals == [1, 0, 0, 0, 0] or \
           five_vals == [1, 1, 0, 0, 0] or \
           five_vals == [1, 1, 1, 0, 0] or \
           five_vals == [1, 1, 1, 1, 0]:
            return "left"
        if five_vals == [0, 0, 0, 1, 0] or \
           five_vals == [0, 0, 1, 1, 0] or \
           five_vals == [0, 0, 0, 0, 1] or \
           five_vals == [0, 0, 0, 1, 1] or \
           five_vals == [0, 0, 1, 1, 1] or \
           five_vals == [0, 1, 1, 1, 1]:
            return "right"
        return "unknown"

    def read_position_str(self):
        """
        returns a string of five letters indicating what the line sensor is seeing.
        'b' indicates that specific sensor has detected a black line.
        'w' indicates that specific sensor has not detected a black line.

        :returns: String indicating what the line follower just read.
        :rtype: str

        Here's an example of what could get returned:
            * ``'bbbbb'`` - when the line follower reads black on all sensors.
            * ``'wwbww'`` - when the line follower is perfectly centered.
            * ``'bbbww'`` - when the line follower reaches an intersection.
        """
        five_vals  = self.read()
        out_str = "".join(["b" if sensor_val == 1 else "w" for sensor_val in five_vals])
        return out_str
##########################
