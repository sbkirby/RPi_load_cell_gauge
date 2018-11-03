# Digital Bandsaw Blade Tension Gauge with RPi
![Front View of Bandsaw](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/main_photo_1.jpg)
![Photo of Controls](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/main_photo_2.jpg)

This is a electronic/digital gauge to measure the tension of band saw blades in order to get the best performance from the blade and the saw. Once installed, this device provides a convenient method for measuring the force or tension a bandsaw blade without interfering with the blade guides or attaching something to the blade. This gauge/scale can be setup to display either imperial (default) or metric.

There are several techniques for measuring band saw blade tension. They include commercially available gauges that attach to the blade, and range in price from $200 to $450. A simple and relatively inexpensive technique for [Bandsaw Tensioning](https://woodgears.ca/bandsaw/tension.html) can be found at Matthias Wandel's website. One of his simplest techniques uses only a digital caliper and a couple of small C-clamps. All of the commercially available methods and including Matthias's are based on the elastic stretching of steel and using Young's modulus to measure the force exerted to stretch the metal bandsaw.

On other technique for tensioning a bandsaw blade is the "Flutter Test". With minimal tension on the blade, the bladesaw tracking is adjusted as would normally be done, and the blade guides are moved up and out of the way of the blade to allow it to flutter freely during this procedure. Next, the bandsaw is started, and the tension is increased until the blade runs straight and true without any "Flutter". American Woodworker has an excellent video on the The [Flutter Test](https://www.youtube.com/watch?v=z8zZuDosSy0) which explains this procedure in greater detail.

The methods mentioned above are accurate and reliable, but requires attaching a device to the blade or moving or adjusting the blade guides in order to tension the blade. My device can be setup once after a blade change, and checked each time the blade is used without attaching a device or adjusting the blade guides. It is true that almost all commercially available bandsaws probably have a tension indicator which may or may not be accurate. After testing the scale on my saw I found it to be inaccurate. While searching for solutions, I ran across Carl Holmgren's video [Blade Tension 101](https://www.youtube.com/watch?v=FZ3CD6pqFZE) that inspired me to build this device. In Carl's video you will see how inaccurate his bandsaw tension gauge was, and the steps he took to calibrate the scale on his gauge.

One source for the proper bandsaw blade tensions can be found at Timber Wolf Bandsaw Blades [Blade Tension](http://timberwolfblades.com/blade-tension.php).

## Design Considerations
![Existing Tension Gauge](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/existing_spring_tension_gauge.jpg)
![View of Tension Spring](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/view_of_spring_on_bandsaw.jpg)

I constructed my tension gauge in order to have an accurate, and readily available gauge to measure blade tension. A similar device was manufactured by the Carter Products Co. a few years ago, and sold for approximately $200 but is no longer available. This design is specific to the Hitachi Model CB-75F bandsaw, but might be adapted to fit other bandsaw models. One unique feature of the Model CB-75F is its ability to use a 75 mm wide blade. When a 75mm blade is tensioned to 12,000 psi it can exert approximately 1,900 lbs force on the band saw frame and load-cell. If I were using a band saw with a maximum capability of 3/4" wide blades and tensioned to 14,000 psi, the force on the frame would be 546 lbs. Therefore, the load-cell needs to be sized to handle the maximum amount of force (plus spare capacity) applied to them to prevent damaging the sensor. Therefore, I choose a 0-1000 Kg load-cell since this sensor is readily available; had the highest range of force; and is capable of handling the maximum load. Lastly, this load-cell must fit within the same space as the tensioning spring (#95 in Figure #1).

![Hitachi Diagram of Tension Assembly](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/hitachi_diagram_of_tension_assembly.jpg)

My preference for a micro-controller required the use of Python. This is my preferred language because I used it professionally for many years, and I like it very much. Therefore, I chose to use a Raspberry Pi Zero because it has Python; it's cheap; it has a large support group, and I had several of them. Probably any of the Raspberry Pi Models would work, but I chose the Zero because of space consideration. Processor speed isn't a requirement. Additionally, any of the Micropython boards might work just as well (e.g. ESP8266 or Adafruit Feather HUZZAH, etc.). There's no reason this program couldn't be adapted to an Arduino.

## Parts

This device is constructed with off the shelf parts including a Raspberry Pi, Load Cell, HX711 Bridge Amplifier, LCD and other parts costing approximately $100.

### PARTS

* 1 Raspberry Pi Zero 
* 1 3141_0 - Button Load Cell (0-1000kg) - CZL204 
* 1 HX711 Weighing Pressure Sensor 24 Bit Precision AD Module 
* 1 Microchip Technology MCP23008-E/P 18 pin DIP 
* 1 Yellow Serial IIC/I2C/TWI 2004 204 20X4 Character LCD Module Display 
* 1 Two Channel IIC I2C Logic Level Converter Bi-Directional Module 5V to 3.3V 
* 1 4x4 Matrix Array 16 Key Membrane Switch Keypad
* 1 GX12-4 GX12 4 Pin Diameter 12mm Male & Female Wire Panel Connector
*  Double Sided Prototype PCB Universal Board

* 2 Steel disk - 1/4" thick and 50mm Diameter
* 1 Steel pipe - ID > 27mm and L > 21mm
* 1 Steel or copper tube - ID > 10mm and L < 7mm
* 20mm Length of Abrasion-Resistant Polyurethane Rubber, 1-3/4" Diameter- McMaster Carr
* 20mm Length of Black Delrin Acetal Resin Rod 2-1/2" Diameter- McMaster Carr

* 1 Bud-Box PN-1324-DG High-Impact ABS NEMA 4x Indoor Box
* 3 Steel Cups For 1/2" Rare Earth Magnets - Woodcraft 
* 3 Rare Earth Magnet 1/2" x 1/8" - Woodcraft

## Electronics
![Wiring Diagram](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/wiring_diagram.jpg)

The electronics consist on a Raspberry Pi Zero (RPi) connected to an HX711 module, 4x4 Keypad, 2-Channel Level Shifter, MCP23008 I/O Expansion Chip and a LCD display. The 4x4 Keypad is interfaced to the RPi via I2C and a MCP23008 chip, and I2C is also used to communicate with the LCD display. I2C communications is accomplished through a 2-Channel Level Shifter module which is used just to be on the safe side. The Load Cell is connected to the HX711 module, and the DT and SCK pins of this module are connected directly to pins 29 and 31 of the RPi. Power and Ground for the Prototype PCB and HX711 module are supplied by pins 1, 2, 4 and 6 of the RPi. Pins 2 & 4 are the 5v power pins, which are connected directly to the RPi's power input. Details of the connects can be seen in Figure #3.

## Update and Configure the Raspberry Pi
![raspi-config](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/raspi-config_main_window.jpg)

Update the existing software on your Raspberry Pi (RPi) with the following command lines instructions
```
sudo apt-get update
sudo apt-get upgrade
```
Depending on how out-of-date your RPi is at the time will determine the amount of time needed to complete these commands.

Next, the RPi needs to be configured for I2C communications via Raspi-Config.
```
sudo raspi-config
```
The screen seen above will appear. First select Expand Filesystem and select Yes. After returning to the Main Menu of Raspi-Config select Enable Boot to Desktop/Scratch and choose to Boot to Console. From the Main Menu select Advanced Options, and enable I2C and SSH from the available options. Finally, select Finish and reboot the RPi.

## Software

Log into the RPi and create the following directories. The /Load_Cell contains the program files and /logs will contain the crontab log files.
```
cd ~
mkdir Load_Cell
mkdir logs
cd Load_Cell
```
Copy the files above to the /Load_Cell folder. I use WinSCP to connect and manage the files on the RPi. Connection to the RPi maybe done via Wifi or serial connection, but SSH needs be enabled in raspi-config to allow this type of connection.

The primary program is BS_tension.py and may be run from the command prompt. In order to test the script enter the following:
```
sudo python BS_tension.py
```
As mentioned previously, the BS_tension.py script is the primary file for the scale. It imports the hx711.py file to read the load-cell via HX711 module. The version of hx711.py used for my project comes from tatobari/hx711py. I found this version provided the features I wanted.

The LCD requires the RPi_I2C_driver.py by Denis Pleic and forked by Marty Tremblay, and can be found at MartyTremblay/RPi_I2C_driver.py.

Finally, I modified a version of William Henning'skeypad16.py to communicate with a MCP23008 and 4x4 keypad. I also added a function getkey to the file for use with the BS_tension.py script. The original version of this file can be located by reading the header of the file and following the links.

The config.json file contains the data stored by program, and is modified by several Menu options and at shutdown. The gauge can be setup for either imperial (default) or metric displays. To change the scale to metric change the "imperial_units" parameter to false and save. This should be done when the BS_tension.py script is not running, otherwise the program might overwrite any changes made to the config.json file.

## Replacing Spring With Load Cell
![Load Cell Diagram](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/drawing_load_cell_diagram.jpg)

Replacing the tension spring with a load-cell is easier said than done. The diameter of the load-cell used was wider than the spring it replaced, therefore, a base was designed and cut-out of a piece of Delrin on my CNC (E in Figure #2). This base fit into the 47mm diameter hole previously used by the spring, and contained a cup to support the 50mm diameter base of the load-cell (D in Figure #2). Since the design used a button load-cell, an adapter was made to focus all the load onto the 10mm diameter by 7mm high button on top of the load-cell. A 50mm diameter by 1/4" thick piece of steel was cut-out and a 6mm high by 10mm ID piece of steel pipe was centered and silver soldered onto the face of the steel disk (C in Figure #2). The same thing was done for the top adapter (A in Figure #2). A piece of 1" steel pipe approximately 22mm long was centered and silver soldered onto the second disk. Finally, a 20mm long piece of 1-3/4" Diameter Polyurethane Rubber (B in Figure #2) was glued between the two adapters using Shoe-Goo.

![Load Cell Cable](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/load_cell_cable_on_bandsaw.jpg)

As you can be seen from the photos above, a hole was drilled thru the back of the sliding frame to route the wire for the load cell.

## Calibration
![Calibration Setup](https://github.com/sbkirby/digital_bandsaw_blade_tension_gauge/blob/master/images/calibrate_full_view.jpg)

Calibrating the gauge is simply a matter of connecting an accurate scale to the slide (108 in Figure #1), and the other end to a part of the lower frame. In my case, I had to remove the belt guard, and tilt the table to rig the scale between the slide and the base. Once this was done, the tension is adjusted with the tensioning wheel and the readings compared. Adjustments are made in the "calibration_factor" variable found in the /Load_Cell/config.json file. In hind site, I should have made a menu option to adjust this variable, but this modification could be easily added to the BS_tension.py file. In any case, I thought that I had calibrated it using a bathroom scale when I had proto-typed it originally, but when I put it on the bandsaw it required more tweaking to calibrate the system. That's my excuse for not adding the calibration menu, and I'm sticking with it.

I do not recommend attaching the scale directly to the wheels. This might deform the wheel since a large load is required to calibrate the gauge. I suggest that you use either the axles or some portion of the upper frame that moves when tensioning the blade.

