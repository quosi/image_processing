import os
import cv2

def log(detected_frame, name, path):
    log_file = open(path + "log_qc_" + name +".txt", "a")
    x = 6
    log_file.write("Start processing " + name)
    log_file.write(detected_frame)
    log_file.close()
    return True, x

def corner_analysis(image, size):
    # size defines size of square, that will analyse luminance value of pixel in 4 corners of the image
    # img = cv2.imread(image)
    img = image
    width = size
    height = size
    # origin of corners / roi = region of interest
    x1 = 0
    y1 = 0
    x3 = img.shape[0] - 1
    y3 = img.shape[1] - 1
    x2 = img.shape[0] - 1
    y2 = 0
    x4 = 0
    y4 = img.shape[1] - 1
    roi1 = img[x1:x1+width, y1:y1+height]
    roi2 = img[x2-width:x2, y2:y2+height]
    roi3 = img[x3-width:x3, y3-height:y3]
    roi4 = img[x4:x4+width, y4-height:y4]

    if (sum(sum(sum(roi1))) == 0) or (sum(sum(sum(roi2))) == 0) or (sum(sum(sum(roi3))) == 0) or (sum(sum(sum(roi4))) == 0):
        return True
    else:
        return False


def video_processor(values):

    # Create a VideoCapture object and read from input file

    path, file = os.path.split(values)
    file_name = file[:-4]

    cap = cv2.VideoCapture(path + "/" + file)

    print("Start processing " + path + file)

    # Check if camera opened successfully
    if (cap.isOpened()== False):
      print("Error opening video stream or file")
    # frame count
    n = 0
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()
      n = n+1
      if ret == True:

    # Display the resulting frame
        cv2.imshow('Frame',frame)
    # mark frames with black corners in log file
        mark = corner_analysis(frame, 20)

        if mark == True:
          print("Frame " + str(n) + " True")

          log(str(n), file, path)

    # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break

    # Break the loop
      else:
        outcome = False
        break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    outcome = True

    return outcome
