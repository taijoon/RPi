#name : test.py
	tsdb input data test code for python
        location is /usr/local/tcollector/collector/0/
	print "python run"
		you can see error message tail -f /var/log/tcollector.log | grep test
	print "tj_RPi.test %d %d nodeid=%d" % ( t, v1, nodeID);
		input data tsdb line

#name : inputTSDB.py
    this py read file and input TSDB
    running location is /tcollector/collector/0/
    must need file name change in inputTSDB.py

#name : PdM_test.py
   this code runing acc sensor
   and input TSDB 100Hz
   [code] time.sleep() => speed control
   code setting 1600Hz sampling and 2G for sensor
