#LCD Only

def message1():
  return "first"
def message2():
  return "second"
def message3():
  return "last"

import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate(busnum=1)
choosenScreen = 3
lastButtonPress = time.time()
lcd.clear()
lcd.message("Raspberry Pi\nOven Mitt!")
time.sleep(2)

while True:
  if (time.time() - lastButtonPress) > 0.5: #trying to debounce the buttons 
    if choosenScreen == 0:
      choosenScreen = 3 #avoid modulus of 0 problems
    if lcd.buttonPressed(lcd.RIGHT):
      choosenScreen+=1
      lastButtonPress = time.time()
    elif lcd.buttonPressed(lcd.LEFT):
      choosenScreen-=1
      lastButtonPress = time.time()
    choosenScreen = choosenScreen % 3
    if (choosenScreen == 0):
      displayMessage = message1()
      #lcd.clear()
    elif (choosenScreen == 1):
      displayMessage = message2()
      #lcd.clear()
    elif (choosenScreen == 2):
      displayMessage = message3()
      #lcd.clear()
    lcd.message(displayMessage)
    
