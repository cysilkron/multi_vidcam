from matplotlib.pyplot import show
from imutils.vidstream import VideoStream
from imutils.fps_counter import FPS_COUNTER
import numpy as np
import argparse

# import imutils
import time
import cv2


# def filterFrame(frame):
# 	frame = imutils.resize(frame, width=450)
# 	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	frame = np.dstack([frame, frame, frame])
# 	return frame


def main(args):
    vid = VideoStream(args['src']).start()
    # time.sleep(1.0)

    # start the FPS timer
    fps_counter = FPS_COUNTER().start()

    # loop over frames from the video file stream
    try:
        count = 0
        founds = 0
        while vid.running():
            # grab the frame from the threaded video file stream, resize
            # it, and convert it to grayscale (while still retaining 3
            # channels)
            count += 1
            try:
                frame = vid.read()

                # Relocated filtering into producer thread with transform=filterFrame
                # frame = filterFrame(frame)

                # show the frame and update the FPS counter
                if args['show']:
                    cv2.imshow("Frame", frame)

                if args['show_q_size']:
                    print('show q size')
                    # display the size of the queue on the frame
                    # cv2.putText(frame, "Queue Size: {}".format(vid.Q.qsize()),
                    #     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                if isinstance(frame, np.ndarray):
                    founds += 1
                    print(f"frame.shape:  {frame.shape}")

                # cv2.waitKey(1)
                if vid.Q.qsize() < 2:  # If we are low on frames, give time to producer
                    time.sleep(0.001)  # Ensures producer runs now, so 2 is sufficient
                fps_counter.update()
            except KeyboardInterrupt:
                break

        # stop the timer and display FPS information
    except Exception as e:
        raise Exception
    finally:
        # do a bit of cleanup
        fps_counter.stop()
        print("fps stopped")
        print("[INFO] elasped time: {:.2f} s".format(fps_counter.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps_counter.fps()))
        print(f"count:  {count}")
        print(f"founds:  {founds}")
        cv2.destroyAllWindows()
        vid.stop()
        vid.release()


ap = argparse.ArgumentParser()
ap.add_argument("--src", default=0, help="src of video")
ap.add_argument("--show", action='store_true', default=False, help="show video on recording")
ap.add_argument("--show-q-size", action='store_true', default=False, help="show queue size in display window")
args = vars(ap.parse_args())
main(args)