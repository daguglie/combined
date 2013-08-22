#Temperature Module

import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-0000047d8dd7')[0] #initially glob.glob(base_dir + '28*')
device_file = device_folder + '/w1_slave'

def readRawData():
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines
    
def getTemp():
  lines = readRawData()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = readRawData()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    tempString = lines[1][equals_pos+2:]
    tempC = float(tempString)/1000.0
    tempF = tempC * 9.0 / 5.0 + 32.0
    return tempC, tempF
  else:
    return "Unknown error"
