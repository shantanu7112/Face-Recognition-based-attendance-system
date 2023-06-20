import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

image_paths = []
path = "Faces/"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
for fileCount in range(0, len(files)) :
    # Read the image
    filePath = path + files[fileCount]
    image_paths.append(filePath)

# Get the list of images
images = [cv2.imread(image_path) for image_path in image_paths]

# Calculate the width and height of each image
width = images[0].shape[1]
height = images[0].shape[0]

# Create a new image with the desired size
rows = 4
cols = 4
output_image = np.zeros((height * rows, width * cols, 3), dtype=np.uint8)

# Iterate over the images and add them to the output image
for i in range(len(images)):
    try :
        x_start = i % rows * width
        y_start = i // cols * height
        output_image[y_start:y_start + height, x_start:x_start + width] = images[i]
    except :
        continue

# Save the output image
fname = 'output_image.bmp'
cv2.imwrite(fname, output_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])            
plt.imshow(output_image)