from urllib.request import urlopen
import numpy as np
import cv2

# Set the image cropping option with the mouse
def click_and_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, getROI
    
    # If the left side of the mouse is pressed, start cutting
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    
    # Check if the left side of the mouse is pressed
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        getROI = True

# Address where the camera can be found
address = 'http://192.168.43.1:8080/shot.jpg'

#  While loop for start recording
while True:
    # Open the camera address and save it under variable imgcode
    imgadd = urlopen(address)
    imgarr = np.array(bytearray(imgadd.read()), dtype=np.uint8)
    imgcode = cv2.imdecode(imgarr, -1)

    # 60% image reduction
    frame = cv2.resize(imgcod, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    cv2.imshow('Frame', frame)

    # Pressing the letter "i" saves the image under Image.jpg
    key = cv2.waitKey(1) & 0xFF
    if key == ord("i"):
        cv2.imwrite('image.jpg', frame)
        break

# Setting the beginning and end of the variables x and y
x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False
getROI = False
refPt = []

# Save the image.jpg under the variable img and make a copy
img = cv2.imread("image.jpg")
clone = img.copy()

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# While loop to display the part we want to cut
while True:
    i = img.copy()
    if not cropping and not getROI:
        cv2.imshow("image", img)
    
    elif cropping and not getROI:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("image", i)
    
    elif not cropping and getROI:
        cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("image", img)
    
    key = cv2.waitKey(1) & 0xFF

    # If we press the r key, we will reset the procedure
    if key == ord("r"):
        image = clone.copy()
        getROI = False

    # If we press the c key, it exits the while loop
    elif key == ord("c"):
        break

# Determining the limits of the HSV color method
refPt = [(x_start, y_start), (x_end, y_end)]
if len(refPt) == 2:
    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    cv2.imshow("ROI", roi)

    hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    print('min H = {}, min S = {}, min V = {}; max H = {}, max S = {}, max V = {}'.format(hsvRoi[:, :, 0].min(), hsvRoi[:, :, 1].min(), hsvRoi[:, :, 2].min(), hsvRoi[:, :, 0].max(), hsvRoi[:, :, 1].max(), hsvRoi[:, :, 2].max()))
    lower = np.array([hsvRoi[:, :, 0].min(), hsvRoi[:, :, 1].min(), hsvRoi[:, :, 2].min()])
    upper = np.array([hsvRoi[:, :, 0].max(), hsvRoi[:, :, 1].max(), hsvRoi[:, :, 2].max()])

    image_to_thresh = clone
    hsv = cv2.cvtColor(image_to_thresh, cv2.COLOR_BGR2HSV)
    
    # Creating a kernel
    kernel = np.ones((3, 3), np.uint8)

    # Mask for a specific color
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("Mask", mask)
    cv2.waitKey(0)

# Closes all windows
cv2.destroyAllWindows()