#!/usr/bin/env python

"""main.py: MicroPython Program that connects to airnow.gov, retrieves data and displays it on an OLED attached to an ESP8266.  Note need to change the CHANGE_MEs in init_values to valid values"""

__author__ = "Aaron Grothe"
__copyright__ = "Copyright 2018, Planet Earth"
__licnese__ = "GPL 3.0 or later"

import network
import time
import urequests
import ujson
import machine
import ssd1306

def init_values():
  global ssid
  global psk
  global apikey
  ssid   = "CHANGE_ME"
  psk    = "CHANGE_ME"
  apikey = "CHANGE_ME"

def init_network():
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect (ssid, psk)

def init_display():
  i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
  oled = ssd1306.SSD1306_I2C(128, 32, i2c, 0x3c)
  oled.fill(0)
  oled.text("Hello World", 0, 0)
  oled.show()
  return oled

def get_data():
  response = urequests.post (apikey)
  parsed = ujson.loads(response.text)
  return parsed

def ljust(text, size):
  if len(text) < size:
    for i in range (len(text), size): 
      text = text + ' '
  return text

def display (option, parsed, oled):
  oled.fill (0)
  if (option == 0): # display place
      text = "Area:   " + parsed[0]['ReportingArea']
      oled.text (text, 0, 10)
      hour = parsed[0]['HourObserved']
      if (hour > 12):
         text = "Sample: " + str(hour-12) + ":00 PM " + str(parsed[0]['LocalTimeZone'])
      elif (hour == 0):
         text = "Sample: 12:00 AM " + str(parsed[0]['LocalTimeZone'])
      else:
         text = "Sample: " + str(hour) + ":00 PM " + str(parsed[0]['LocalTimeZone'])
      oled.text (text, 0, 20)
  if (option == 1):
    for i in range (0, 3):
      text = ljust(parsed[i]['ParameterName'], 5)  + ' - ' + str(parsed[i]['AQI'])
      oled.text (text, 0, (10 * i))
  if (option == 2): # display good/bad/etc
    for i in range (0, 3):
      text = ljust(parsed[i]['ParameterName'], 5)  + ' - ' + str(parsed[i]['Category']['Name'])
      oled.text (text, 0, (10 * i))
  oled.show()

def once ():
  init_network()
  oled = init_display()
  parsed = get_data()
  display (1, parsed, oled)

def loop():
  init_values()
  init_network()
  oled = init_display()
  while (1):
    parsed = get_data()
    for i in range (600):
      for j in range (0, 3):      
        display (j, parsed, oled)
        time.sleep(2)

if __name__ == "__main__":
  loop()
