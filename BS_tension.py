#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Bandsaw Tension Application

Parts:
    1ea - Raspberry Pi Zero V1.2
    1ea - Phidgets - 3141_0 - Button Load Cell (0-1000kg) - CZL204
    1ea - HX711 Weighing Pressure Sensor 24 Bit Precision AD Module For Arduino
    1ea - MCP23008 - 8-Bit I/O Expander with High-speed I2C interface
    1ea - 4x4 Matrix keypad
    1ea - Serial I2C 20X4 Character LCD Module Display
Modules:
    hx711.py - Source: https://github.com/tatobari/hx711py/blob/master/hx711.py
    keypad16.py - original from  http://Mikronauts.com but modified by me to support MCP23008
    RPi_I2C_driver.py - Source: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

Date: November 15, 2016
By: Stephen B. Kirby
'''
import RPi.GPIO as GPIO
import RPi_I2C_driver
import time
import sys
import os
import json
import signal
import keypad16 as matrix
from hx711 import HX711

# Load configuration from config JSON file.
with open('config.json', 'r') as infile:
    config = json.load(infile)

# calculate Area
AREA = config['blade_width'] * config['blade_thickness'] * 2
# Key functions dictionary
'''
KEY_FUNCTION = {
    "A": "blade_dimension",
    "B": "tare_menu",
    "C": "display_tension",
    "D": "display_force", # D - also used in tare_menu option
    "#": "main_menu"}
'''
KEY_FUNCTION = {
    "A": "display_tension",
    "B": "display_force",
    "C": "display_settings",
    "D": "shutdown_pi", # D - also used in tare_menu option
    "#": "main_menu"}

# Superscript two - squared Character
fontdata0 = [[
    0b00100,
	0b01010,
	0b00110,
	0b01000,
	0b01110,
	0b00000,
	0b00000,
	0b00000
    ]]

# HX711(dout, sck) - initialize Load Cell amplifier
hx = HX711(5, 6)
# initialize keypad and MCP23008
kp = matrix.keypad_module(0x20,0,0)
# initialize the LCD
disp = RPi_I2C_driver.lcd()
disp.lcd_clear() # Clear display

# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("LSB", "MSB")
# Set Reference unit for Phidgets Part: 3141_0 - Button Load Cell (0-1000kg) - CZL204
hx.set_reference_unit(config['calibration_factor'])
# Reset and set offset for the HX711 amplifier board
hx.reset()
hx.set_offset(config['offset']) # set the offset

# Shutdown Raspberry Pi
def shutdown_pi(lbs, klg, ch, row = 2):
    save_data() # save data file
    disp.lcd_clear() # clear LCD
    time.sleep(0.1)
    disp.backlight(0) # turn OFF LED
    time.sleep(0.1)
    GPIO.cleanup() # cleanup GPIO
    os.system('shutdown now -h')

# Event handler for Ctrl+C
def signal_handler(signal, frame):
    # print 'You pressed Ctrl+C!'
    clean_and_exit()

# save data to config.json data file
def save_data():
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)

# save the data, cleanup GPIO and exit
def clean_and_exit():
    save_data() # save data file
    disp.lcd_clear() # clear LCD
    time.sleep(0.1)
    disp.backlight(0) # turn OFF LED
    time.sleep(0.1)
    GPIO.cleanup() # cleanup GPIO
    sys.exit() #exit python to system

# Display Weight on LCD
def display_LbKg(lbs, klg, ch, row = 2): # WEIGHT - Lbs and Klg
    if config['imperial_units']:
        disp.lcd_display_string_pos("Lb: ",row,0)
        disp.lcd_display_string_pos("{:10.1f}".format(lbs),row,10)
    else:
        disp.lcd_display_string_pos("Kg: ",row,0)
        disp.lcd_display_string_pos("{:10.1f}".format(klg),row,10)

# Display TENSION on LCD - PSI and Kilo Pascals
def display_PsikPa(lbs, klg, ch, row = 2):
    if config['imperial_units']:
        # PSI
        tension = lbs/AREA
        disp.lcd_display_string_pos("PSI: ",row,0)
        disp.lcd_display_string_pos("{:6.0f}".format(tension),row,14)
    else:
        disp.lcd_load_custom_chars(fontdata0)  # load Superscript 2 - squared
        # kilograms per square centimeter
        tension = klg/AREA
        disp.lcd_display_string_pos("Kg/cm",row,0)
        disp.lcd_write_char(0) # print Superscript 2 - squared
        disp.lcd_display_string_pos(": ",row,6)
        disp.lcd_display_string_pos("{:6.0f}".format(tension),row,14)

# Main Displays for LCD
def main_menu(lbs, klg, ch):
    disp.lcd_display_string_pos("Tension:         A",1,0)
    disp.lcd_display_string_pos("Force:           B",2,0)
    disp.lcd_display_string_pos("Settings:        C",3,0)
    disp.lcd_display_string_pos("Shutdown:        D",4,0)

def display_settings(lbs, klg, ch):
    disp.lcd_display_string_pos("SETTINGS ",1,0)
    disp.lcd_display_string_pos("Blade Dimension: A",2,0)
    disp.lcd_display_string_pos("Tare Scale:      B",3,0)
    disp.lcd_display_string_pos("Menu: #",4,0)

def display_force(lbs, klg, ch):
    disp.lcd_display_string_pos("FORCE ",1,0)
    display_LbKg(lbs, klg, ch)
    disp.lcd_display_string_pos("Menu: #",4,0)

def display_tension(lbs, klg, ch):
    # display the Width x Thickness of Blade
    disp.lcd_display_string_pos("TENSION  {:0.3f}x{:0.3f}".format(config['blade_width'],config['blade_thickness']),1,0)
    display_PsikPa(lbs, klg, ch, 2)
    disp.lcd_display_string_pos("Menu: #",4,0)

def tare_menu(lbs, klg, ch):
    disp.lcd_display_string_pos("TARE SCALE ",1,0)
    display_LbKg(lbs, klg, ch)
    disp.lcd_display_string_pos("Tare: D    Menu: #",4,0)

# function called from TARE SCALE menu to TARE scale without a blade
def tare_scale(lbs, klg, ch):
    global config, menu_item
    disp.lcd_display_string_pos("Saving Tare...",2,2)
    hx.reset()
    hx.tare()
    config['offset'] = hx.OFFSET # read and store the OFFSET
    save_data() # save the new OFFSET to config.json data file
    menu_item = tare_menu # return to the TARE SCALE menu
    # clear screen
    disp.lcd_clear()

def blade_dimension(lbs, klg, ch):
    if config['imperial_units']:
        title = "BLADE DIMENSION - in"
    else:
        title = "BLADE DIMENSION - cm"
    disp.lcd_display_string_pos(title,1,0)
    disp.lcd_display_string_pos("Width:        {:0.3f}".format(config['blade_width']),2,0)
    disp.lcd_display_string_pos("Thickness:    {:0.3f}".format(config['blade_thickness']),3,0)
    disp.lcd_display_string_pos("W: 1  T: 2   Menu: #",4,0)

def input_blade_width(lbs, klg, ch):
    if config['imperial_units']:
        title = "BLADE WIDTH - in"
    else:
        title = "BLADE WIDTH - cm"
    disp.lcd_display_string_pos(title,1,0)
    disp.lcd_display_string_pos("Current W: {:0.3f}".format(config['blade_width']),2,0)
    disp.lcd_display_string_pos("Width:        {}".format(menu_variable),3,0)
    disp.lcd_display_string_pos("Save: A    Cancel: #",4,0)

def input_blade_thickness(lbs, klg, ch):
    if config['imperial_units']:
        title = "BLADE THICKNESS - in"
    else:
        title = "BLADE THICKNESS - cm"
    disp.lcd_display_string_pos(title,1,0)
    disp.lcd_display_string_pos("Current T: {:0.3f}".format(config['blade_thickness']),2,0)
    disp.lcd_display_string_pos("Thickness:    {}".format(menu_variable),3,0)
    disp.lcd_display_string_pos("Save: A    Cancel: #",4,0)

# convert menu_variable string to number
def num(s):
    if s == "": return 0
    try:
        return int(s)
    except ValueError:
        return float(s)

# Determine the menu function to call.
menu_item = globals().get(KEY_FUNCTION['#'], display_tension)
menu_variable = ""

# check for keypad events
def check_keypad_events(chk):
    if (chk != None):
        global menu_item, menu_variable, config, AREA
        # Input for menu options
        if chk in 'ABCD#':
            # Check for blade dimension input - 'A' = Save settings
            if (menu_item == input_blade_width) and (chk == "A"):
                config['blade_width'] = num(menu_variable)
                AREA = config['blade_width'] * config['blade_thickness'] * 2
                save_data() # save the new blade_width to config.json data file
            if (menu_item == input_blade_thickness) and (chk == "A"):
                config['blade_thickness'] = num(menu_variable)
                AREA = config['blade_width'] * config['blade_thickness'] * 2
                save_data() # save the new blade_thickness to config.json data file
            # Check for TARE SCALE input
            if (menu_item == tare_menu) and (chk == "D"):
                menu_item = tare_scale
            # SETTINGS MENU:
            # A = blade_dimension, B = tare_menu, # = main_menu
            if (menu_item == display_settings) and ((chk == "A") or (chk == "B")):
                if (chk == "A"): menu_item = blade_dimension
                if (chk == "B"): menu_item = tare_menu
            #  MAIN MENU:
            #  A = display_tension,  B = display_force,  C = display_settings
            #  D = shutdown_pi,  # = main_menu
            elif (menu_item == main_menu):
                menu_item = globals().get(KEY_FUNCTION[chk], display_tension)
            elif (chk == "#"):
                # if in blade width or Thickness menu then return to blade_dimension menu
                if (menu_item == input_blade_width) or (menu_item == input_blade_thickness):
                    menu_item = blade_dimension
                else:
                    # return to main_menu
                    menu_item = main_menu
            # clear screen, set menu_item and reset menu_variable
            disp.lcd_clear()
            # reset the menu_variable
            menu_variable = ""
        # check for '1' kep stroke in 'blade_dimension' menu
        # change menu to Blade Width
        elif (menu_item == blade_dimension) and (chk == "1"):
            disp.lcd_clear()
            menu_item = globals().get('input_blade_width')
            menu_variable = ""
        # check for '2' kep stroke in 'blade_dimension' menu
        # change menu to Blade Thickness
        elif (menu_item == blade_dimension) and (chk == "2"):
            disp.lcd_clear()
            menu_item = globals().get('input_blade_thickness')
            menu_variable = ""
        else:
            # Input numeric data and store in menu_variable
            if chk == "*": # convert * to decimal point
                chk = "."
            # check for a decimal point in menu_variable - only one per value
            if (chk == ".") and ("." not in menu_variable):
                menu_variable += chk
            else:
                menu_variable += chk

# Main loop:
signal.signal(signal.SIGINT, signal_handler)
# print 'Press Ctrl+C'

while True:
    # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
    val = hx.get_weight(1)
    if (val < 0): val = 0
    # convert to kilograms
    kilos = val * 0.453592
    # Check for key strokes on keypad
    key = kp.getkey()
    time.sleep(0.1)
    # check for Keypad events
    check_keypad_events(key)
    # call function
    menu_item(val, kilos, key)
    # power down and power up the HX711
    hx.power_down()
    hx.power_up()
