#!/usr/bin/python3

from curses import raw
import rospy
import serial
import utm
import math
from gps_driver_package.msg import gps_msg
import sys
from std_msgs.msg import String

#ser = serial.Serial("/dev/ttyACM0")
ser = serial.Serial(sys.argv[1])
ser.baudrate = 4800
#######$GNGGA,171916.00,4220.29439,N,07105.19113,W,4,12,0.61,34.8,M,-33.2,M,1.0,0000*6E
def parsing(ser_line):
	ls = ser_line.split(",")
	latitude_raw = float(ls[2])
	latitude_raw = latitude_raw/100
	minutes,degrees = math.modf(latitude_raw)
	latitude = degrees + 100*minutes/60
	if ls[3] == "S":
		latitude = -latitude
	longitude_raw = float(ls[4])
	longitude_raw = longitude_raw/100

	minutes,degrees = math.modf(longitude_raw)
	longitude = degrees + 100*minutes/60
	if ls[5] == "W":
		longitude = -longitude
	altitude = float(ls[9])
	pos_stat = int(ls[6])
	stamp = float(ls[1])
	HDOP = float(ls[8])
	return latitude,longitude,altitude,pos_stat

def parse_time(serline) :
	ls = serline.split(",")
	raw_time = ls[1]
	l = len(raw_time)
	rospy.loginfo(type(raw_time))
	seconds = float(raw_time[4:])
	# rospy.loginfo((raw_time[l-10:l-8]), 'hereeeeeeeeeeeeeeeeeeeee')
	minutes = float(raw_time[2:3])
	hours = float(raw_time[0:1])
	time_secs = hours*3600 + minutes*60 + seconds
	return time_secs

def sensor():
	pub = rospy.Publisher('/gps',gps_msg, queue_size = 5)
	pubGPGGA = rospy.Publisher('/gpgga',String,queue_size = 5)
	rospy.init_node('gps_sensor', anonymous = True)
	r = rospy.Rate(1)
	msg = gps_msg()
	gpggastring = String()
	msg.header.seq = 0
	msg.header.frame_id = "GPS1_Frame"
	
	while not rospy.is_shutdown():
		ser_line = ser.readline().decode("utf-8")  # utf-8 is a protocol by which the device is communicating with the serial port. 
	# Doing .decode("utf-8") removes all characters of the protocol and leaves only latitude longitude values. 
		GNGGA = "GNGGA"
		if GNGGA in ser_line:
			rospy.loginfo("inside")
			msg.header.seq+=1
			gpggastring.data = ser_line
			rospy.loginfo(ser_line)
			latitude,longitude,altitude,pos_stat= parsing(ser_line)
			rospy.loginfo("Latitude :"+ str(latitude))
			rospy.loginfo("Longitude :" + str(longitude)) 
			rospy.loginfo("Below the location in UTM is rospy.print")
			utm_coordinates = utm.from_latlon(latitude,longitude)
			rospy.loginfo(utm_coordinates)
			rospy.loginfo("Altitude :" + str(altitude))
			
			time_stamp = parse_time(ser_line)
			msg.header.stamp = rospy.Time.from_sec(time_stamp)
			msg.latitude = latitude
			msg.longitude = longitude
			msg.altitude = altitude
			msg.utm_easting = utm_coordinates[0]
			msg.utm_northing = utm_coordinates[1]
			msg.zone = utm_coordinates[2]
			msg.letter = utm_coordinates[3]
			msg.pos_stat = pos_stat
			
			#rospy.loginfo(msg)
			pub.publish(msg)
			pubGPGGA.publish(gpggastring)

			r.sleep()	


if __name__ == '__main__':
	try:
		sensor()
	except rospy.ROSInterruptException: pass


	

