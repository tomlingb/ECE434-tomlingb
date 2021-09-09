#! /bin/bash

led=0
value=0
command="heartbeat"

while getopts l:v:c: flag
do
    case "${flag}" in
        l) led=${OPTARG};;
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
elif [ $command = "off" ]
then
    echo none > trigger
    echo 0 > brightness
elif [ $command = "heartbeat" ]
then
	echo heartbeat > trigger
elif [ $command = "timer" ]
then
	echo timer > trigger
	echo $value > delay_on
	echo 500 > delay_off
fi

