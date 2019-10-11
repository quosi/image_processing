import os, logging, cv2, sys, random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

LOCATION = '/home/pepper/Projects/spiced/final_project/images/videos_errors/'
FILENAME = 'D84_px.mp4'

def video_augmentation(filename, location):
    """reads video file, does augmentation (pixel error),
    stores augmented video to disc"""
    print(f"[INFO] loading {filename} from {location}...")
    #create video capture object
    cap = cv2.VideoCapture(f"{location}{filename}")
    # Define the codec and create VideoWriter object
    frame_width, frame_height = 1920, 1080
    out = cv2.VideoWriter(f'{location}out/{filename}', cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width, frame_height))
    name = filename.split('.')[0]
    frame_n = 1
    if (cap.isOpened()==False):
        logging.error('Error opening video stream or file')

    while (cap.isOpened()):
        print("opened")
        #capture frame-by-frame
        ret, frame = cap.read()
        print(frame)
        if ret == True:
            #cv2.imshow('Frame', frame)
            frame_n = frame_n + 1

            for i in range(3, random.choice([3, 4, 5])):
                #Add some hot-pixel errors
                x = np.random.randint(low=0,high=(frame_height))
                y = np.random.randint(low=0,high=(frame_width))
                frame[x:x+3, y:y+3] = np.random.randint(low=200,high=255)
                frame[x:x+3, y:y+3] = np.random.randint(low=0,high=10)
                frame[x:x+3, y:y+3] = np.random.randint(low=0,high=10)
            out.write(frame)
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break
    # release the video write objects
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    return print(f'Frame count of {name}: {frame_n}')

if __name__ == "__main__":
    video_augmentation(FILENAME, LOCATION)
