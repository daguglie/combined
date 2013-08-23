#LCD Only

import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import TempMod
import datetime


lcd = Adafruit_CharLCDPlate(busnum=1)
numScreens = 4
choosenScreen = 3
lastButtonPress = time.time()
lastRefresh = time.time()
timerRun = False
timerStart = datetime.datetime.now()
timerStop = datetime.datetime.now()

lcd.clear()
lcd.message("Raspberry Pi\nOven Mitt!")
time.sleep(2)

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
  if lcd.buttonPressed(lcd.UP) and timerRun == False:
    timerStart = datetime.datetime.now()
    timerRun = True
  elif lcd.buttonPressed(lcd.DOWN):
    timerRun = False
  elif lcd.buttonPressed(lcd.SELECT):
    timerStart = datetime.datetime.now()
    timerStop = datetime.datetime.now()
    timerRun = False
  if timerRun == True:
    timerStop = datetime.datetime.now()
  retStr = timerStop - timerStart
  return retStr.strftime('%H:%M:%S')
  
def message3():
  return "last"

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
    
  if (time.time() - lastRefresh) > 2: #stop screen flickers
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
      displayMessage = message3()
    lcd.clear()
    lcd.message(displayMessage)
    
