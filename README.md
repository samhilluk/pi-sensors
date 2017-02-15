# Interacting with sensors from a Raspberry PI
The Raspberry PI is a fantastic device and great for the hobbist or anyone who just wants to explore and learn a bit more about computers and electronics.

Using sensors can at the start seem a little daunting however its actually really quite simple.

This guide will walk through a number of different sensors and python scripts are provided to show how to use them "in code".

Sensors covered:

- Temperature Sensor




## Temperature Sensor

The easiest sensor to start with is with the temperature sensor, most people use the **DALLAS 18B20** sensor which you can pick up for a few pennies on various websites, this is a digital sensor and runs at 3V so no risk of frying the Raspberry PI.

### Wiring the sensor

Once you have the sensor you need to connect it up, the easiest way is as follows, however the pins you use can be (to a certain extent) varied as there are multiple 3V out, ground and data in pins available. The way I have done it is as shown in this picture:

![Wiring diagram](https://github.com/samhilluk/pi-sensors/raw/master/wiring.png)

Connect the Vcc (voltage in) pin on the sensor to Pin 1 on the GPIO. Pin 1 is the top left pin when you look at the PI with the USB ports at the bottom. Then connect the middle pin (data) to Pin 7 on the GPIO - (count down 4 pins from the top). Then connect the GND (Ground) pin to pin 6 (count 3 pins down from the top, right column this time). You also need to add a 10k resistor between Vcc and Data however most sensors you buy have this pre-attached so check first.

### Letting the Raspberry PI know its there

Once its all wired up then its time to power up the PI and to connect.

Firstly, it is always good practice to update Linux first:
    
`sudo apt-get update` then `sudo apt-get upgrade`

Accessing the sensor is now relatively easy. To test the sensor is there and working correctly, run the following:

`modprobe w1-gpio`
then
`ls -l /sys/bus/w1/devices/`

You should see the sensor listed... (If not try the *housekeeping* step at the bottom then reboot).

```
root@raspberrypi:/home/sam# ls -l /sys/bus/w1/devices/
total 0
lrwxrwxrwx 1 root root 0 Feb 15 09:22 28-011515e78cff -> ../../../devices/w1_bus_master1/28-011515e78cff
lrwxrwxrwx 1 root root 0 Feb 15 09:22 w1_bus_master1 -> ../../../devices/w1_bus_master1
```

The sensors address starts with `28` and all sensors have a unique address allowing you to connect multiple ones to the same Raspberry PI - for example inside and outside temperature checking.

To find out the temperature its then a case of simply asking the sensor!
```
root@raspberrypi:/home/sam# cat /sys/bus/w1/devices/28-011515e78cff/w1_slave
0a 01 55 00 7f ff 0c 10 64 : crc=64 YES
0a 01 55 00 7f ff 0c 10 64 t=16625
```
Replace the unique sensor address with your own (28-011515e78cff above will not be the identifier for your sensor as that is my unique code).

That is it - it works we have a temperature sensor. The temperature is given by the `t=...` value, that needs to be made into something meaningful - its actually simply a case of dividing by 1000 the number returned (16.625 degrees in my example here).

Now, to have the sensor working everytime the Raspberry PI boots up we need to bo one more bit of housekeeping....

Using your linux editor of choice, I'm a bit old-school and like **vi** however others are available (like the much easier to use **nano**) and change the **boot/config.txt** file, this tells the Raspberry PI what modules to load at boot time - and we need to add in the temperature module.

`sudo vi /boot/config.txt`

Just add the following into the file:

`dtoverlay=w1-gpio`

Then reboot your PI.


### Using the sensor in a useful way

There are lots of ways to interact with the sensor, the easist is with the command line as shown above - simply `cat` the `w1_slave` file to find out the temperature. This can be made into a one line script to give a meaningful answer using:

```
cat /sys/bus/w1/devices/28-011515e78cff/w1_slave | sed -n 's/^.*\(t=[^ ]*\).*/\1/p' | sed 's/t=//' | awk '{x=$1}END{print(x/1000)}'
```

This uses a bit of `sed` and `awk` magic to convert it into something useful, again, replace the sensor address - starts 28 - with your own (28-011515e78cff above will not be the identifier for your sensor as that is my unique code).


To help here I have a simple **python** script that will read the sensor and then convert the value into both Celsius and Fahrenheit - available here [temp.py](https://github.com/samhilluk/pi-sensors/raw/master/temp.py "temp.py").

You can then use the `crontab` to run this script at scheduled intervals to create a text file with the current temperature (to then show on a webpage) or to create a temperature history file (to draw graphs with!).

My crontab is as follows:

```
*/5 * * * *  python /var/sensors/temp.py > /var/www/temp.txt
*/5 * * * *  python /var/sensors/temp.py >> /var/www/temp-history.csv
30 * * * *  python /var/sensors/temp.py >> /var/www/temp-history-hourly.csv
```

This captures the current temperature every 5 minutes into a single file that is shown on a webpage, it also produces 2 history files, one at 5 minute intervals the other 30 minute intervals. The difference between `>` and `>>` the first replaces the file each time, the latter appends the data to the end of the file.




  