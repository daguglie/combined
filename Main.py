#LCD Only

def message1():
  return "first"
def message2():
  return "second"
def message3():
  return "last"

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate(busnum=1)
choosenScreen = 3

lcd.clear()
lcd.message("Raspberry Pi\nOven Mitt!")
sleep(2)

while True:
  if choosenScreen == 0:
    choosenScreen = 3 #avoid modulus of 0 problems
  if lcd.buttonPressed(lcd.RIGHT):
    choosenScreen+=1
  elif lcd.buttonPressed(lcd.LEFT):
    choosenScreen-=1
  choosenScreen = choosenScreen % 3
  if (choosenScreen == 0):
    displayMessage = message1()
    lcd.clear()
  elif (choosenScreen == 1):
    displayMessage = message2()
    lcd.clear()
  elif (choosenScreen == 2):
    displayMessage = message3()
    lcd.clear()
  lcd.message(displayMessage)
