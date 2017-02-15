import os
import glob
import time
import subprocess

############################################################
## Simple python script to read the temperature and record the outcome
############################################################
## Sam Hill - www.samhill.uk
############################################################


## If the modules are not loaded into the system at boot, uncomment the following lines.
## os.system('modprobe w1-gpio')
## os.system('modprobe w1-therm')


## Find the sensor and read its values.
def read_sensor():
## The following looks to find the temperature sensor, this isn't locked to a specific identifier (change the "28*" below to be specific).
## It uses the first sensor listed, if you have multiple ones - for example internal and external this code needs modifying.
		base_dir = '/sys/bus/w1/devices/'
		device_folder = glob.glob(base_dir + '28*')[0]
		device_file = device_folder + '/w1_slave'
		catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = catdata.communicate()
		out_decode = out.decode('utf-8')
		lines = out_decode.split('\n')
		return lines

## Convert the sensor data into something displayable
def show_temperature():
	lines = read_sensor()
## If the sensor has an issue the first response will be a "NO" if so keep trying - but wait 1/2 a second first!
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.5)
		lines = read_sensor()
## Find the "t=" value which is the actual temperature
	temp_pos = lines[1].find('t=')
	if temp_pos != -1:
		temp_raw = float(lines[1][temp_pos+2:])
## Convert the raw value into both Celsius (temp_c) and Fahrenheit (temp_f)
		temp_c = temp_raw / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
## Choose which tempterature type to return by changing the line below
		return temp_c

## Display the putput with date and time pre-pended.
print(time.strftime("%Y/%m/%d")) + ", " + (time.strftime("%H:%M:%S")) + ", " + ('{:.2f}'.format(show_temperature()))
