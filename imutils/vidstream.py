# import the necessary packages
from threading import Thread
import sys
import cv2
import time
from imutils.fps_counter import FPS_COUNTER
from imutils.frame_datetime_recorder import FrameDatetime

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


class VideoStream:
    def __init__(self, src, transform=None, queue_size=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(src)
        self.stopped = False
        self.transform = transform
        self.frame_idx = 0

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queue_size)
        # intialize thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        # start a thread to read frames from the file video stream
        self.thread.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                break

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stopped = True
                else:
                    # if there are transforms to be done, might as well
                    # do them on producer thread before handing back to
                    # consumer thread. ie. Usually the producer is so far
                    # ahead of consumer that we have time to spare.
                    #
                    # Python is not parallel but the transform operations
                    # are usually OpenCV native so release the GIL.
                    #
                    # Really just trying to avoid spinning up additional
                    # native threads and overheads of additional
                    # producer/consumer queues since this one was generally
                    # idle grabbing frames.
                    if self.transform:
                        frame = self.transform(frame)

                    # add the frame to the queue
                    self.frame_idx += 1
                    self.Q.put([self.frame_idx, frame])
            else:
                time.sleep(0.1)  # Rest for 10ms, we have a full queue

        self.release()

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    # Insufficient to have consumer use while(more()) which does
    # not take into account if the producer has reached end of
    # file stream.
    def running(self):
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1

        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        # wait until stream resources are released (producer thread might be still grabbing frame)
        self.thread.join()
        print(f"num of frame grabbed:  {self.frame_idx}")

    def release(self):
        self.stream.release()


class TimedVideoStream(VideoStream):
    def __init__(self, src, time_recorder: FrameDatetime, fps_counter: FPS_COUNTER, transform=None, queue_size=128):
        super().__init__(src, transform, queue_size)
        self.time_recorder = time_recorder
        self.max_retry = 3
        self.fps_counter = fps_counter
        self.camera_started = False

    def start(self):
        # start a thread to read frames from the file video stream
        if not self.is_camera_started():
            raise RuntimeError("Camera cant be started")

        self.fps_counter.start()
        self.camera_started = True
         
        self.thread.start()
        return self

    def is_camera_started(self):
        '''this function shall be call before the `update` thread is started'''
        # retry checking the camera is started every 0.01 seconds
        retry_count = 0
        grabbed = False
        while retry_count < self.max_retry:
            grabbed = self.stream.grab()  # cam record (without decode)
            if grabbed:
                break
            else:
                retry_count += 1
                time.sleep(0.01)

        return grabbed


    def update(self):
        while True:
            if self.stopped:
                break

            # ensure the queue has room in it
            if not self.Q.full():
                
                # (grabbed, frame) = self.stream.read()
                grabbed = self.stream.grab() # cam record (without decode)
                if not grabbed:
                    self.stopped = True

                # time recording is done right after the frame is properly grab,
                # to maximize precise time recording (avoiding the frame decoding time)
                else:
                    self.frame_idx += 1
                    self.time_recorder.record(self.frame_idx)
                    grabbed, frame = self.stream.retrieve() # decoding

                # if the producer computing is far ahead of the consumer, 
                # some transform is allowed to be done here
                # but make sure the computation wont block the IO of camera and decoding computation
                if self.transform:
                    frame = self.transform(frame)

                # add the frame to the queue
                self.Q.put([self.frame_idx, frame])
            else:
                time.sleep(0.1)  # Rest for 10ms, we have a full queue

        self.release()

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        # wait until stream resources are released (producer thread might be still grabbing frame)
        self.thread.join()
        self.fps_counter.stop()
        print(f"num of frame grabbed:  {self.frame_idx}")