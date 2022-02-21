# import the necessary packages
import datetime


class FPS_COUNTER:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._first_frame_start = None
        self._program_start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._first_frame_start = datetime.datetime.now()
        return self

    def program_start(self):
        self._program_start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the program start and
        # end interval
        return (self._end - self._program_start).total_seconds()

    def frame_recorded_time(self):
        # return the total number of seconds between the first frame grabbed
        # and end interval
        return (self._end - self._first_frame_start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.frame_recorded_time()

    def info(self):
        # print("fps stopped")
        # print(f"[INFO] _first_frame_start: {self._first_frame_start}")
        print(f"[INFO] frame recorded time: {self.frame_recorded_time():.2f} s")
        print("[INFO] elasped time: {:.2f} s".format(self.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps()))