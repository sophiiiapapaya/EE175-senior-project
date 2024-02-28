import cv2.cv as cv
import cv2
import time
from socket import socket
import sys
import numpy

cv.NamedWindow("camera",cv.CV_WINDOW_AUTOSIZE)

capture = cv.CaptureFromCAM(0)

sock = socket()
sock.connect(('192.168.0.2', 5001))
sock.send('Pi - Hallo')

while True:
    frame = cv.QueryFrame(capture)
    cv.ShowImage("camera", frame)

    mat = cv.GetMat(frame)
    buf = [1,90]

    image = cv.CreateImage (cv.GetSize (frame), 8, 3)
    nuImage = numpy.asarray(frame[:,:])
    imgencode = cv2.imencode('.png', nuImage, buf)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    sock.send('Pi - Sending image data');
    sock.send( stringData );

    if cv.WaitKey(10) == 27:
        break

sock.send('Pi - closing connection')
sock.close()