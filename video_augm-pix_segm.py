import os, logging, cv2, sys, random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

LOCATION_SRC = '/home/pepper/Projects/spiced/final_project/images/videos_errors/'
LOCATION_SQR = '/home/pepper/Projects/spiced/final_project/cnn_25-09-2019/train/clean/'
LOCATION_SQR_ER = '/home/pepper/Projects/spiced/final_project/cnn_25-09-2019/train/error/'
FILENAME = 'D84_h264_errors_px.mp4'

def img_aug_px(img):
    for i in range(1, random.choice([3, 2])):
        #Add some hot-pixel errors
        x_ = np.random.randint(low=0,high=(64))
        y_ = np.random.randint(low=0,high=(64))
        x2_ = np.random.randint(low=0,high=(64))
        y2_ = np.random.randint(low=0,high=(64))
        img[x_:x_+3, y_:y_+3] = np.random.randint(low=230,high=255)
        img[x2_:x2_+3, y2_:y2_+3] = np.random.randint(low=0,high=10)
    return img

def video_seg_augm(filename, location, location_squares, location_squares_er):
    """reads video file, does augmentation (pixel error),
    stores augmented video to disc"""
    print(f"[INFO] loading {filename} from {location}...")
    #create video capture object
    cap = cv2.VideoCapture(f"{location}{filename}")
    # Define the codec and create VideoWriter object
    frame_width, frame_height = 1920, 1080
    out = cv2.VideoWriter(f'{location}out/aug_{filename}', cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width, frame_height))
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
            for x in range(0, frame.shape[0], 64):
                xvon = x
                xbis = x+64
                if xvon > frame.shape[0]-64:
                    xvon = frame.shape[0]-64
                    xbis = frame.shape[0]
                for y in range(0, frame.shape[1], 64):
                    yvon = y
                    ybis = y+64
                    if ybis > frame.shape[1]:
                        yvon = frame.shape[1]-64
                        ybis = frame.shape[1]

                    square = frame[xvon:xbis, yvon:ybis,:]
                    Image.fromarray(square).convert("RGB").save(location_squares+name+str(frame_n)+"_"+str(x)+"_"+str(y)+".png")
                    sq_mod = img_aug_px(square)
                    Image.fromarray(sq_mod).convert("RGB").save(location_squares_er+name+str(frame_n)+"_"+str(x)+"_"+str(y)+".png")
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
    video_seg_augm(FILENAME, LOCATION_SRC, LOCATION_SQR, LOCATION_SQR_ER)
