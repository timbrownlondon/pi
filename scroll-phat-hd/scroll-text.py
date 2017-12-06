#!/usr/bin/env python3

import time
import signal
import sys
import scrollphathd
from scrollphathd.fonts import font5x7

for line in sys.stdin:
    
    scrollphathd.clear()
    scrollphathd.write_string(line.rstrip(), x=17, y=0, font=font5x7, brightness=0.3)

    buffer_length = scrollphathd.get_buffer_shape()[0]

    for i in range(buffer_length+1):
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(0.05)

  
    time.sleep(0.5)

