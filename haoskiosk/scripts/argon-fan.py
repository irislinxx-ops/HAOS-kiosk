#!/usr/bin/env python3
import os, time, glob
I2C_BUS=1; FAN_ADDR=0x1a; FAN_REG=0x00; TEMP_LOW=48; TEMP_HIGH=72
def read_temp():
    try:
        for p in sorted(glob.glob('/sys/class/thermal/thermal_zone*/temp')):
            with open(p) as f: return int(f.read().strip())/1000.0
    except: return 0
def set_fan(s):
    s=max(0,min(100,s))
    try:
        import smbus2; bus=smbus2.SMBus(I2C_BUS)
        bus.write_byte_data(FAN_ADDR,FAN_REG,s); bus.close(); return True
    except: return False
def main():
    time.sleep(15); last=-1
    while True:
        t=read_temp()
        if t>0:
            if t<=TEMP_LOW: spd=0
            elif t>=TEMP_HIGH: spd=100
            else: spd=int((t-TEMP_LOW)/(TEMP_HIGH-TEMP_LOW)*100)
            if spd!=last: set_fan(spd); last=spd
        time.sleep(10)
if __name__=='__main__': main()
