#!/usr/bin/env python
# IIoT PdM openTSDB test
# author: PJ

import sys, time, datetime
#from adxl345 import ADXL345
import smbus
from time import sleep

# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
#bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)
bus = smbus.SMBus(1)
bus0 = smbus.SMBus(0)

# ADXL345 constants
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004

DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D

BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09

RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03

MEASURE             = 0x08
AXES_DATA           = 0x32

class ADXL345:

    address = None

    def __init__(self, address = 0x53):        
        self.address = address
        self.setBandwidthRate(BW_RATE_100HZ)
        self.setRange(RANGE_8G)
        self.enableMeasurement()

    def enableMeasurement(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)
        bus0.write_byte_data(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        bus.write_byte_data(self.address, BW_RATE, rate_flag)
        bus0.write_byte_data(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        value = bus.read_byte_data(self.address, DATA_FORMAT)
        value &= ~0x0F;
        value |= range_flag;  
        value |= 0x08;

        bus.write_byte_data(self.address, DATA_FORMAT, value)

        value1 = bus0.read_byte_data(self.address, DATA_FORMAT)
        value1 &= ~0x0F;
        value1 |= range_flag;  
        value1 |= 0x08;

        bus0.write_byte_data(self.address, DATA_FORMAT, value1)
    
    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce = False):
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)
        
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}
    def getAxes0(self, gforce = False):
        bytes = bus0.read_i2c_block_data(self.address, AXES_DATA, 6)
        
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}

if __name__ == "__main__":
    adxl345 = ADXL345()
    old_sec =0
    min1000 = 0 
    while True:
        d_metrix = datetime.datetime.fromtimestamp(
                time.time()
                ).strftime('IIoT_%02m_%02d_%02H')
        f_day = '% .3f' % time.time()
        iix = str(f_day).split('.')
        convertT = (int(iix[0])/10000000)*10000000 + int(iix[1])

        if(int(iix[1]) < old_sec):
            min1000 += 1
        old_sec = int(iix[1])
        convertT = convertT + (min1000 *1000)
        
        axes = adxl345.getAxes(True)
        sys.stdout.write( "1_%s.vibX %d %f nodeid=1\n" % ( d_metrix, convertT, axes['x'] ))
        sys.stdout.write( "1_%s.vibY %d %f nodeid=1\n" % ( d_metrix, convertT, axes['y'] ))
        sys.stdout.write( "1_%s.vibZ %d %f nodeid=1\n" % ( d_metrix, convertT, axes['z'] ))
        axes0 = adxl345.getAxes0(True)
        sys.stdout.write( "0_%s.vibX %d %f nodeid=1\n" % ( d_metrix, convertT, axes0['x'] ))
        sys.stdout.write( "0_%s.vibY %d %f nodeid=1\n" % ( d_metrix, convertT, axes0['y'] ))
        sys.stdout.write( "0_%s.vibZ %d %f nodeid=1\n" % ( d_metrix, convertT, axes0['z'] ))
        time.sleep(3)
