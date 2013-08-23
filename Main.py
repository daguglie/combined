#LCD Only

import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import TempMod



lcd = Adafruit_CharLCDPlate(busnum=1)
choosenScreen = 3
lastButtonPress = time.time()
lastRefresh = time.time()
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
  if selection == 0: #avoid modulus of 0 or negative problems
    selection = 2
  selection = selection % 2
  if selection == 1:
    now = datetime.datetime.now()
    retStr = now.strftime('%a, %b %d') +"\n"+now.strftime('%I:%M %p')
  elif selection == 0:
    now = datetime.datetime.now()
    retStr = now.strftime('%a, %b %d') +"\n"+now.strftime('%H:%M')
    return now.strftime('%a, %b %d')
    
def message2():
  return "second"
def message3():
  return "last"

while True:
  if (time.time() - lastButtonPress) > 0.5: #trying to debounce the buttons 
    if choosenScreen == 0:
      choosenScreen = 3 #avoid modulus of 0 or negative problems
    if lcd.buttonPressed(lcd.RIGHT):
      choosenScreen+=1
      lastButtonPress = time.time()
    elif lcd.buttonPressed(lcd.LEFT):
      choosenScreen-=1
      lastButtonPress = time.time()
      
    choosenScreen = choosenScreen % 3
    
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
      displayMessage = message2()
      #lcd.clear()
    elif (choosenScreen == 2):
      displayMessage = message3()
      #lcd.clear()
    lcd.clear()
    lcd.message(displayMessage)
    
