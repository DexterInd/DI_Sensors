from __future__ import print_function
from __future__ import division

# from di_sensors import line_follower
import line_follower
import pickle

'''
MUTEX HANDLING
'''
# from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

class EasyLineFollower(line_follower.LineFollower):

    file_white_calibration = '/home/pi/Dexter/white_line.txt'
    file_black_calibration = '/home/pi/Dexter/black_line.txt'

    def __init__(self):
        super(EasyLineFollower, self).__init__()

        try:
            self._white_calibration = self.get_calibration('white')
            self._black_calibration = self.get_calibration('black')
        except ValueError:
            self._white_calibration = [1.0] * 6
            self._black_calibration = [0.0] * 6

        self._calculate_threshold()

    def _calculate_threshold(self):
        self._threshold = [(a + b) / 2.0 for a,b in zip(self._black_calibration, self._white_calibration)]


    def read(self, representation="raw"):
        """
        representation - float, position, string
        """
        if representation == 'raw':
            return self.read_sensors()
        elif representation == 'bivariate':
            raw_vals = self.read_sensors()
            six_vals = [0] * 6
            for i in range(6):
                if raw_vals[i] > self._threshold[i]:
                    six_vals[i] = 1
                else:
                    six_vals[i] = 0
            return six_vals
        elif representation == 'position':
            pass
        elif representation == 'string':
            pass
        else:
            pass

    def set_calibration(self, color):
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

    
    def get_calibration(self, color):
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
                line = [1.0] * 6
            elif color == 'black':
                line = [0.0] * 6

        if len(line) != 6:
            raise ValueError('incompatible calibration file')
        else:
            return line

