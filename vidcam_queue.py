import cv2
import queue
import threading
import time

# bufferless VideoCapture
class VideoCapture:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


cam = VideoCapture(0)
try:
    while True:
        time.sleep(0.5)  # simulate time between events
        try:
            frame = cam.read()
            print(frame.shape)
            cv2.imshow("frame", frame)
            if chr(cv2.waitKey(1) & 255) == "q":
                break
        except KeyboardInterrupt:
            print(f"^c:")
            break
except Exception as e:
    print(e)
finally:
    cam.cap.release()

