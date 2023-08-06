import threading
import time


class MinuteTimer():
    """
    Minute Timer class calls the given callback function once every minute
    :param callback_function: Callback function to be called
    """
    def __init__(self, callback_function):
        self.callback_function = callback_function
        self.next_call = time.time()
        self.__timer()

    def cancel(self):
        """
        Cancel the timer and its internal thread
        """
        self.thread.cancel()

    def __timer(self):
        self.next_call = self.next_call + 60
        self.thread = threading.Timer(self.next_call - time.time(), self.__timer)
        self.thread.start()
        self.callback_function()
