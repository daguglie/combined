#LCD Only

import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import TempMod
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

lcd = Adafruit_CharLCDPlate(busnum=1)
numScreens = 4
choosenScreen = 3
lastButtonPress = time.time()
lastRefresh = time.time()
timerRun = False
timerStart = datetime.datetime.now()
timerStop = timerStart
prevDispMessage = ""
lcd.clear()
lcd.backlight(lcd.TEAL)
lcd.message("Raspberry Pi\nOven Mitt!")
time.sleep(2)

beatTotalTime = 0
beatCount = 0
prevBeat = datetime.datetime.now()

configArray = [1,1,1]


def TempConfig():
  selection = configArray[0] 
  if selection == 0: #avoid modulus of 0 or negative problems
    selection = 2
  selection = selection % 2
  values = TempMod.getTemp()
  if selection == 1:
    return str(values[0]) + " C"
  elif selection == 0:
    return str(values[1]) + " F"

def TimeConfig():
  selection = configArray[1] 
  retStr = ""
  if selection == 0: #avoid modulus of 0 or negative problems
    selection = 2
  selection = selection % 2
  if selection == 1:
    now = datetime.datetime.now()
    retStr = now.strftime('%a, %b %d') +"\n"+now.strftime('%I:%M:%S %p')
  elif selection == 0:
    now = datetime.datetime.now()
    retStr = now.strftime('%a, %b %d') +"\n"+now.strftime('%H:%M:%S')
  return retStr
    
def TimerConfig():
  #Problem with writing to this variable because it is in it's own def so declared as global
  global timerRun, timerStart, timerStop
  if lcd.buttonPressed(lcd.UP) and timerRun == False:
    timerStart = datetime.datetime.now()
    timerRun = True
  elif lcd.buttonPressed(lcd.DOWN):
    timerRun = False
  elif lcd.buttonPressed(lcd.SELECT):
    timerStart = datetime.datetime.now()
    timerStop = timerStart
    timerRun = False
  if timerRun == True:
    timerStop = datetime.datetime.now()
  retVal = timerStop - timerStart
  return str(retVal)
  
def HeartBeatConfig():
  global lcd, prevState
  retMsg = ""
  if (beatTotalTime != 0 and beatCount == 10):
    retNum = beatTotalTime / 10
    retNum = 60/retNum
    retMsg = str(retNum)
  else:
    retMsg = "Not enough heart\n beats yet"
  return retMsg
  
  if ( GPIO.input(23) == False and prevState):
    lcd.backlight(lcd.RED)
    retMsg = "beat"
    prevState = False
  elif ( GPIO.input(23) == True and not prevState):
    lcd.backlight(lcd.BLUE)
    retMsg = "no beat"
    prevState = True
  return retMsg
  
def beat(channel):
  currentTime = datetime.datetime.now()
  if (count == 11):
    beatTotalTime = neatTotalTime - prevTime + (currentTime - prevTime)
    prevTime = currentTime
    lcd.backlight(lcd.RED)
    lcd.backlight(lcd.TEAL)
  elif(count > 0 and count < 11):
    beatTotalTime += (currentTime - prevTime)
    lcd.backlight(lcd.RED)
    lcd.backlight(lcd.TEAL)
  else:
    prevTime = currentTime
    lcd.backlight(lcd.RED)
    lcd.backlight(lcd.TEAL)

def message3():
  return "last"

GPIO.add_event_detect(23, GPIO.FALLING)
GPIO.add_event_callback(23, beat)

while True:
  if (time.time() - lastButtonPress) > 0.5: #trying to debounce the buttons 
    if choosenScreen == 0:
      choosenScreen = numScreens #avoid modulus of 0 or negative problems
    if lcd.buttonPressed(lcd.RIGHT):
      choosenScreen+=1
      lastButtonPress = time.time()
    elif lcd.buttonPressed(lcd.LEFT):
      choosenScreen-=1
      lastButtonPress = time.time()
      
    choosenScreen = choosenScreen % numScreens
    
    if lcd.buttonPressed(lcd.UP):
      configArray[choosenScreen] += 1
    elif lcd.buttonPressed(lcd.DOWN):
      configArray[choosenScreen] -= 1
    
 
  if (choosenScreen == 0):
      displayMessage = TempConfig() #Temperature Module
      #displayMessage = message1()
      #lcd.clear()
  elif (choosenScreen == 1):
      displayMessage = TimeConfig()
      #lcd.clear()
  elif (choosenScreen == 2):
      displayMessage = TimerConfig()
      #lcd.clear()
  elif (choosenScreen == 3):
      displayMessage = HeartBeatConfig()
  if(displayMessage != prevDispMessage):
    lcd.clear()
    lcd.message(displayMessage)
    prevDispMessage = displayMessage
