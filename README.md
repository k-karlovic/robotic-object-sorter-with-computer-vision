# Robotic object sorter with computer vision
Sorting and controlling objects with a certain number of holes by a robotic arm!
<br />
<br />
<br />
<p align="center">
  <a href="https://youtu.be/jOdGGo3MNKM"> <img width="90%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/youtube_image.png?raw=true"/> </a>
</p>

&nbsp;
## Table of Contents or Overview
* [Summary](#summary)
* [Setup](#setup)
* [Equipment](#equipment)
	* [Robotic arm Mover4](#robotic-arm-mover4)
	* [Samsung S8+ camera](#samsung-s8-camera)
	* [Conveyor](#conveyor)
	* [Arduino](#arduino)
* [Object detection method](#object-detection-method)
* [Holes detection method](#holes-detection-method)
* [Conclusion](#conclusion)
* [Literature](#literature)

&nbsp;
## Summary
This project involves finding a defined workpiece with holes on the conveyor, controlling the number of holes on the workpiece, and sorting them using a robotic arm. The workpiece on the conveyor is detected by the HSV model of the color space over the camera. Using functions in OpenCV (cv2.Canny() and cv2.findContours()) holes (closed contours) are found on the workpiece. Closed contours are counted, and the workpieces are sorted by a robotic arm into correct and incorrect workpieces.

&nbsp;
## Setup
### 1. Equipment
* [Robotic arm](#robotic-arm-mover4)
* [Camera](#samsung-s8-camera)
* [Conveyor](#conveyor)
* [Arduino](#arduino)
 	* 2 wires
 	* USB cable
* Computer
### 2. Install Requirements
* [ArduinoIDE](https://www.arduino.cc/en/software)

* [CPRog](https://cpr-robots.com/robot-control)

* [Python](https://www.python.org/downloads/)

To install the necessary packages in python run **`pip install -r requirements.txt`**.
### 3. Connect the Arduino with the robotic arm
Connect one end of the wire to pin 12 on the Arduino and the other end to pin 4 on the robot arm. Connect another wire to pin 13 on the Arduino and pin 5 on the robotic arm. For more see [here](#robotic-arm-mover4).
### 4. Connect the Arduino with the computer
Connect the Arduino using a USB cable to the computer
### 5. Connect the cammera with the computer
Download the [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&gl=US) app on your mobile phone and start the server. Your phone and your computer must be connected to the same wifi.

You can use any camera, such as a webcam that is connected with a USB cable.
### 6. Run the `hsv_color_detector.py` script
Position the workpiece so that it is visible in the image and press the I button to display the workpiece. To determine the color boundary it is necessary to crop the object (press the left mouse button in the upper left corner and release the button in the lower right corner). When you have finished, press the c button and 3 windows will open. On which it is visible that the object is marked in white, and everything else in black. If you are not satisfied, repeat the procedure. For more see [here](#object-detection-method).
### 7. Enter the color boundaries
Enter the given color boundaries from the previous step in `holes_detector.py` script under lower and upper.
### 8. Transfer the code to Arduino
Open the arduino_signal.ino scipt in the ArduinoIDE software and transfer the code to Arduino.
### 9. Run the robot script
Run the robot.xml script in CPRog software.
### 10. Run the `holes_detector.py` script
The camera must be positioned before the sensor on the conveyor. Place the workpieces on the conveyor and allow the conveyor to bring the workpieces to the sensor where the robotic arm will sort the workpieces. For more see [here](#holes-detection-method).

&nbsp;
## Equipment
For this project, a 4-axis Mover4 robot, a Samsung S8+ mobile phone camera with a resolution of 12.0 MP, a conveyor, and an Arduino were used to connect the robotic arm and laptop. The main programming language used to accomplish the final work is Python with additional packages installed. The Arduino uses ArduinoIDE, and the robotic arm uses CPRog software.
&nbsp;
### Robotic arm Mover4
The robotic arm consists of 4 axes, which allow work in space. At the end of the robotic arm, various tools (electromagnet or gripper) can be placed. With a radius of 55 cm, the robot can lift objects weighing 500g.
<br />
<br />
<p align="center">
  <img width="30%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/robot.jpg?raw=true"/>
</p>
<br />
D-Sub Male consists of 9 pins of which pins 4, 5, 6, and 7 are input pins.
<br />
<br />
<br />
<p align="center">
  <img width="40%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/pins_on_robot_arm.PNG?raw=true"/>
</p>

&nbsp;
### Samsung S8+ camera

The mobile phone serves as an IP webcam and images from the mobile phone are read via the IP address.
&nbsp;
### Conveyor
The conveyor is used to transport the object from one workplace to another, and the object is stopped by a sensor at the end of the conveyor.
<br />
<br />
<p align="center">
  <img width="50%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/conveyor.jpg?raw=true"/>
</p>

&nbsp;
### Arduino
The Arduino is connected via USB to a computer and is programmed using the ArduinoIDE softwer. The Arduino will serve as a circuit for communicating with the robot, which sends 5V to the input channels as a logical one and 0V as a logical zero.
<br />
<br />
<p align="center">
  <img width="30%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/arduino.jpg?raw=true"/>
</p>

&nbsp;
## Object detection method
The program starts finding holes only after it detects an object. So it is necessary to choose and adjust the method that detects the object. The chosen method is based on recognition via the HSV color model. It is necessary to set the boundaries within which the color of the object is located. To find these boundaries, the script `hsv_color_detector.py` is attached. It works on the principle of setting the subject to the appropriate position and then pressing the "i" key to save the image. This image is then displayed and the area from which the color boundary is to be drawn can be determined with the mouse. The "c" key completes the determination and three windows are displayed. The first shows the whole image with the area selected. The second image shows only the area that is selected. On the third, the color chosen was converted to white, and the others became black. This shows that the procedure was done correctly, and if black is visible on the object, then the procedure should be repeated.After that, the boundaries min H = {}, min S = {}, min V = {}, max H = {}, max S = {} and max V = {} are thrown out.
<br />
<br />
<p align="center">
  <img width="90%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/HSV_boundaries.JPG?raw=true"/>
</p>
<br />

There is also some disturbance in the upper-right edge, which is present due to the reflection of light. The procedure should be repeated or the boundaries should be set manually.
After that, the boundaries are entered in the script `holes_detector.py`. In that script, a kernel is created and parameters are set to find the colors of objects. If a contour is found a red circle is created around the contour.
<br />
<br />

<p align="center">
  <img width="30%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/circle.JPG?raw=true"/>
</p>

&nbsp;
## Holes detection method
Once the boundaries of the HSV color rendering model are defined and the object is spotted, an aperture is found. Finding openings is based on finding closed contours. Uploaded images are converted to Grayscale (gray image) and processed using a Threshold. The threshold is binary and inverse with certain parameters. The image is further filtered using a bilateral filter. Edge detection is introduced to the processed image using the Canny Edge detection method and contours can now be found using the cv2.findContours() function. To find the contours, certain parameters are set and displayed in the image. It is necessary to set in which area the contours are, with some approximation. An if-loop has also been added to define whether the object has the required number of holes. The final result with the found object, holes, number of openings, and certain correctness of the workpiece is shown in the following image.
<br />
<br />
<p align="center">
  <img width="90%" src="https://github.com/k-karlovic/Item_Sorter/blob/main/images/holes_detection.JPG?raw=true"/>
</p>
<br />

The correct workpiece would be a 2 hole object, so this workpiece on the image above would be incorrect. Disturbances of light reflection are visible and the contour of the workpiece is not well noticed. The contour could be corrected by changing the defined boundary of the HSV model. Neither interference affects the final result, the program for finding the number of holes spotted the correct number of holes.

&nbsp;
## Conclusion
This project contains two scripts related to the vision system of robots, the so-called robotic vision. The first script `hsv_color_detector.py` determines the color boundaries in the HSV model and is needed because it serves as a basis for the script `holes_detector.py`. After the first script sets the boundaries, in the same HSV color space model, the second script will recognize the object. The located holes are counted, after which the correctness of the obtained number is checked. One of the difficulties is the reflection of light on the conveyor that was detected after defining the boundaries of the HSV color space model. Next, contours that were not properly marked or interrupted followed. In that case, holes were found where there were none. The solution to such a problem is achieved by setting the parameters of different filters, defining the search area of the closed contour and its approximation. In general, the small diameter of holes requires small closed contours which makes it a big problem in practice. Namely, the function marks and recognizes every irregularity on the observed object as a hole. Some minor disturbances were ignored as they did not affect the final result. Changing the environment or brightness in the room could cause interference that leads to the wrong result when controlling the object. In this case, individual parameters would have to be changed or certain image filters would have to be added and changed. The problem of communication with the robot was solved using an open computer and software platform - Arduino. By sending a logical one that is equivalent to 5V, the robot program is started, and with it the robot itself. The robotic vision program can be further improved to perform other functions such as recognizing the complete drilling of the hole or the appropriate positioning of the hole and sorting defective objects with a robotic arm and so on.

&nbsp;
## Literature

https://www.arduino.cc/en/Tutorial/HomePage

https://cpr-robots.com/education#Mover4

Bradski, G.; Kaehler, A..: „ Learning OpenCV“, O’Reilly Media., Gravenstein Highway North, Sebastopol, 2008.

García, G.,B.; Suarez, O., D.; Aranda, J.,L., E.; Tercero, J., S.; Gracia, I., S.; Enano, N., V.: „ Learning Image Processing with OpenCV“, Packt Publishing., Birmingham, 2015.

https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html

https://pythonprogramming.net/loading-images-python-opencv-tutorial/



