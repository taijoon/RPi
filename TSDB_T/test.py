#!/usr/bin/env python
import time
import os
import sys
import serial

v1 = 1
nodeID = 99

while(1):
	t= int(time.time())
	print "python run"
	print "tj_RPi.test %d %d nodeid=%d" % ( t, v1, nodeID);
	v1 = v1 +2;
	time.sleep(3);

