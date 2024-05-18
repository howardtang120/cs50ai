import cv2
import os

IMG_WIDTH = 30
IMG_HEIGHT = 30
PATH = 'gtsrb/40'


for img in os.listdir(PATH):
    file_path = os.path.join(PATH, img)
    image = cv2.imread(file_path)
    if image is not None:
        # Display the image
        print(file_path)
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        
        resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
        cv2.imshow('Image', resized)
        cv2.waitKey(0)        
        cv2.destroyAllWindows()
    else:
        print('Failed to load the image.')

