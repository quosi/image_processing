# generate  list of images from dataset directory
# initialize the list of data (i.e., images) and class images
import os
#import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

LOCATION = 'images/movie_pics/'
location_squares = LOCATION+"squares/"

print("[INFO] loading images...")
images = os.listdir(LOCATION)

data = []
labels = []
b = 0
# loop over the images
for image in images:
	# extract the image label from the filename
	label = image.split('.')[-2]
	labels.append(label)
	# load the image, and slice it into 64x64 squares
	img = Image.open('images/movie_pics/'+image)
	img = np.array(img)
	i = []
	for x in range(0, img.shape[0], 64):
		for y in range(0, img.shape[1], 64):
			square = img[x:x+64, y:y+64,:]
			#save each of the squares as 'label+n.jpg'
			Image.fromarray(square).convert("RGB").save(location_squares+label+"_"+str(x)+"_"+str(y)+".png")

	# performe image augmentation on each square, save as 'label+n+_aug.jpg'
	# add PIXE ERRORS
		for i in range(0,11):
		    #Add some hot pixels
		    square[np.random.randint(low=0,high=199),np.random.randint(low=0,high=199)]= np.random.randint(low=200,high=255)
		    #and dead pixels
		    square[np.random.randint(low=0,high=199),np.random.randint(low=0,high=199)]= np.random.randint(low=0,high=10)

			img_plt.imsave(location_squares+label+"_"+str(x)+"_"+str(y)+".png", square)


	# update the data and labels list
	b+=1
	if b > 19:
		break


# TRY SECTION
print(img)
plt.imshow(img)

for x in range(0, img.shape[0], 64):
	for y in range(0, img.shape[1], 64):
		print(x,y)
