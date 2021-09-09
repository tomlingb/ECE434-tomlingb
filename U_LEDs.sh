#! /bin/bash

led=0
value=0
command="on"
while getopts led:v:c: flag
do
    case "${flag}" in
        led) led_number=${OPTARG};;
        v) value=${OPTARG};;
	c) command=${OPTARG};;
    esac
done

echo editing user LEDs
cd /sys/class/leds/beaglebone\:green\:usr$led

if [ $command = "on" ]
then
	echo none > trigger 
	echo 1 > brightness 
elif [ $command = "invert" ]
then 
	echo $value > invert
elif [ $command = "heartbeat" ]
then
	echo heartbeat > trigger
fi

