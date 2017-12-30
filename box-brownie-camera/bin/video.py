#!/usr/bin/env python

import time
import picamera
import RPi.GPIO as GPIO
import subprocess
import os

# set up button
button = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# pass this in so can use absolute paths and invoke by /etc/rc.local
base_dir = os.environ['base_dir']

# output is placed in content/<dir>/<index>.<ext>
filename = '{}/content/{}/{:04d}.{}'

def shoot_video_for_index(i):
    camera = picamera.PiCamera(resolution = (640, 640), framerate = 20)
    camera.start_recording(filename.format(base_dir, 'h264', i, 'h264'))
    print(filename.format(base_dir, 'h2d4', i, 'h264'))

    # continue recording until we have detected button off
    # several times (loop for switch bounce protection)
    button_off_count = 0
    while button_off_count < 3:
        camera.wait_recording(0.2)
        if GPIO.input(button):
            button_off_count += 1

    camera.stop_recording()
    camera.close()

    # save an mp4 wrapped version of shot video
    subprocess.call(['MP4Box',
                     '-add', 
                     filename.format(base_dir, 'h264', i, 'h264'),
                     filename.format(base_dir, 'mp4', i, 'mp4')
                   ])

try:
    while True:
        # button level is inverted (false means pressed)
        while GPIO.input(button):
            time.sleep(0.1)

        # choose next free filename to save video to
        i = 0
        while os.path.exists(filename.format(base_dir, 'h264', i, 'h264')):
            i += 1

        shoot_video_for_index(i)



# hit Ctrl + C to stop program
except KeyboardInterrupt:
    GPIO.cleanup()


