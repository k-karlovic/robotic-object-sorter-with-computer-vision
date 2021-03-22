from urllib.request import urlopen
import numpy as np
import cv2
import serial
import time

# The USB port to which the Arduino is connected
ser1 = serial.Serial('COM3', 9600)

# Defining the lower and upper limits in the HSV color display model
lower = {'item': (0, 0, 163)}
upper = {'item': (180, 30, 254)}

# Defining the color of the circle that will be around the object
color = {'item': (25, 40, 195)}

# Address where the camera can be found
address = 'http://192.168.43.1:8080/shot.jpg'

# While loop for start recording
while True:
    # Open the camera address and save it under variable imgcode
    imgadd = urlopen(address)
    imgarr = np.array(bytearray(imgadd.read()), dtype=np.uint8)
    imgcode = cv2.imdecode(imgarr, -1)

    # 80% image reduction
    frame = cv2.resize(imgcode, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
    org = frame.copy()
    clone = frame.copy()

    # Gaussian blurring
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    # Conversion to HSV model
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Color analysis of images to find objects
    for key, value in upper.items():
        # Mask construction
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])

        # Methods of morphological transformation open and close
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Merge mask and image
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # Find contours using cv2.findContours
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None

        # If at least one contour is found
        if len(contours) > 0:
            # It finds the largest contour in the mask and adds it to the minimum circle and origin
            c = max(contours, key=cv2.contourArea)

            # (x, y) origin of the circle
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # If the radius satisfies a minimum size of 0.5
            if radius > 0.5:
                # Draws a circle on the image and adds text
                cv2.circle(frame, (int(x), int(y)), int(radius), color[key], 2)
                cv2.putText(frame, key + "", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color[key], 2)
    
    # Convert BGR color to gray
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Add color limits
    _, gray_threshed = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
    
    # Bilateral filter
    bilateral_filtered_image = cv2.bilateralFilter(gray_threshed, 5, 175, 175)

    # Canny edge detection
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 25, 200)

    # Finding contours
    _, cont, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Determining contours
    contour_list = []
    for contour in cont:
        approx = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 3) & (area > 1)):
            contour_list.append(contour)
    
    # Display results on images
    cv2.drawContours(frame, contour_list, -1, (255, 0, 0), 2)
    a = int((len(contour_list)-1) / 2)

    # Displaying the number of holes
    print('Number of holes: {}'.format(a))

    # If the number of holes is equal to 2 and the found contours are greater than 0
    if a == 2 and len(contours) > 0:
        print('Correct number of holes')
        # Sending the letter M to the Arduino
        ser1.write('M'.encode())
    
    # If the number of holes is different from 2 and the contours found are greater than 0
    elif a != 2 and len(contours) > 0:
        print('Incorrect number of holes')
        # Sending the letter K to the Arduino
        ser1.write('K'.encode())
    
    # If the number of holes is equal to 0 and the found contours are greater than 0
    elif a == 0 and len(contours) > 0:
        print('There are no holes')
        # Sending the letter K to the Arduino
        ser1.write('K'.encode())
    
    # If the contours found are equal to 0
    elif len(contours) == 0:
        print('There are no items')
    
    # Displaying individual operations and results
    cv2.imshow("Original", org)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow('Smooth', bilateral_filtered_image)
    cv2.imshow('Edge', edge_detected_image)
    cv2.imshow('frame', frame)

    # If q is pressed all windows will close
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Closes all windows
cv2.destroyAllWindows()