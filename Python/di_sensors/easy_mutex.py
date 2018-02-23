'''
MUTEX HANDLING
'''
import I2C_mutex
mutex = I2C_mutex.Mutex(debug = False)
overall_mutex = mutex.overall_mutex()

def ifMutexAcquire(mutex_enabled = False):
    """
    Acquires the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.
    Always acquires if system-wide mutex has been set.
    
    """
    if mutex_enabled or overall_mutex==True:
        mutex.acquire()

def ifMutexRelease(mutex_enabled = False):
    """
    Releases the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.

    """
    if mutex_enabled or overall_mutex==True:
        mutex.release()