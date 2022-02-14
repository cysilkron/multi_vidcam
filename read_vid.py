import cv2
  
  
# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
    try:
    # Capture the video frame
    # by frame
        ret, frame = vid.read()
    
        # Display the resulting frame
        # cv2.imshow('frame', frame)
        if ret:
            print(frame.shape)
        else:
            print('cant capture')
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt as e:
        break
    finally:
    
        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()