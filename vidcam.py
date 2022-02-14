import cv2
import threading
import time
import numpy as np

# bufferless VideoCapture
class VideoCapture:
    def __init__(self, name, retry_delay=0.2):
        self.cap = cv2.VideoCapture(name)
        self.retry_count = 0
        self.max_retry_count = 5
        self.retry_delay = retry_delay

        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.reader_on = True
        self.t.start()
        

    # grab frames as soon as they are available
    def _reader(self):
        while self.reader_on:
            ret = self.cap.grab()
            print(f"ret:  {type(ret)}")
            if not ret:
                time.sleep(self.retry_delay)
                self.retry()
                break

    def retry(self):
        
        self.retry_count += 1
        print(f'retrying reading cam... {self.retry_count} time')
        if self.retry_count >= self.max_retry_count:
            print('reach max retry count, off cam reader')
            self.reader_on = False

    # retrieve latest frame
    def read(self):
        ret, frame = self.cap.retrieve()
        return frame


cam1 = VideoCapture(0)
count = 0
while True:
    time.sleep(0.5)  # simulate time between events
    count += 1
    try:
        print(f"count:  {count}")
        frame = cam1.read()

        print(f"type(frame):  {type(frame)}")
        if frame is not None and isinstance(frame, np.ndarray):
            print(frame.shape)
        # cv2.imshow("frame", frame)
        # if chr(cv2.waitKey(1) & 255) == "q":
        #     break
    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print(f"^c:")
        break
    finally:
        cam1.cap.release()