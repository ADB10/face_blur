
# -*- coding: utf-8 -*-
"""
Author: Lima Vallantin
https://medium.com/@limavallantin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details on http://www.gnu.org/licenses/.
"""

import cv2

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def find_and_blur(bw, color): 
    # detect al faces
    faces = cascade.detectMultiScale(bw, 1.1, 4)
    # get the locations of the faces
    for (x, y, w, h) in faces:
        # select the areas where the face was found
        roi_color = color[y:y+h, x:x+w]
        # blur the colored image
        blur = cv2.GaussianBlur(roi_color, (101,101), 0)
        # Insert ROI back into image
        color[y:y+h, x:x+w] = blur            
    
    # return the blurred image
    return color

# turn camera on
video_capture = cv2.VideoCapture("video.mp4")

while True:
    # get last recorded frame
    _, color = video_capture.read()
    # transform color -> grayscale
    bw = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    # detect the face and blur it
    blur = find_and_blur(bw, color)
    # display output
    cv2.imshow('Video', blur)
    # break if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# turn camera off        
video_capture.release()
# close camera  window
cv2.destroyAllWindows()