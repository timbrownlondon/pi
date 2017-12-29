#!/usr/bin/env python

import time
import picamera
import RPi.GPIO as GPIO
import os

# set up button
button = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # button level is inverted (false means pressed)
        while GPIO.input(button):
            time.sleep(0.1)

        # choose filename to save video to
        i = 0
        while os.path.exists("video%03d.h264" % i):
            i += 1

        camera = picamera.PiCamera()
        camera.resolution = (512, 512)
        camera.start_recording('video%03d.h264' % i)
        button_off_count = 0

        # record number of times have detected button off as a de-bounce protection
        while button_off_count < 3:
            camera.wait_recording(0.2)
            if GPIO.input(button):
                button_off_count += 1

        camera.stop_recording()




# hit Ctrl + C to stop program
except KeyboardInterrupt:
    GPIO.cleanup() #cleanup GPIO channels
    print ('program stopped')
