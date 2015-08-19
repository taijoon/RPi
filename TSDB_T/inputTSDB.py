#!/usr/bin/env python

import time
from time import sleep

f = open("/usr/local/tcollector/collectors/0/05_B_100_vibX", "r")

print 'input TSDB Start'
while True:
    line = f.readline()
    if not line: break
    print str(line)
    time.sleep(0.001)
print 'input Done'

f.close()
