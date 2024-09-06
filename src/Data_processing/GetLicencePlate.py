import cv2
from matplotlib import pyplot as plt
import numpy as np
import easyocr
import imutils
import re
import os

# Since the tool that saves the images names them based on the date and time of saving,
# we can't work with that, so we search for the file that ends with .png
# because it gets deleted after processing
def find_png_file():
    # Search through all the files in the directory
    for filename in os.listdir("."):
        # Check if the file ends with .png
        if filename.endswith(".png"):
            return filename  
    return None 

def getLicencePlate():
    try:
        # Read the image containing the license plate
        filename = find_png_file()
        originalCarImage = cv2.imread(filename, 0)

        # Filter the image to remove noise and detect edges using Canny
        filteredImage = cv2.bilateralFilter(originalCarImage, 11, 17, 17)
        edgesImage = cv2.Canny(filteredImage, 30, 200)

        # Find contours, calculate their perimeters, and take the top 10 largest perimeters
        keypoints = cv2.findContours(edgesImage.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        # Check if the found contours form a rectangle (for the license plate)
        location = None
        for contour in contours:
            approxLoc = cv2.approxPolyDP(contour, 10, True)
            if len(approxLoc) == 4:
                location = approxLoc
                break

        # Mask the license plate area
        mask = np.zeros(originalCarImage.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(originalCarImage, originalCarImage, mask=mask)

        # Crop the area containing the license plate
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = originalCarImage[x1:x2+1, y1:y2+1]

        # Extract the license plate number
        reader = easyocr.Reader(['en'])
        carPlateProcessed = reader.readtext(cropped_image)

        # Clean up the extracted text, removing spaces and non-alphanumeric characters
        carPlate = carPlateProcessed[0][1]
        carPlateInfo = re.sub(r'[^a-zA-Z0-9\s]', '', carPlate)
        carPlateInfo = carPlateInfo.replace(" ", "")

        return carPlateInfo 
    except Exception as e:
        return None
