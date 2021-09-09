#! /bin/bash

led=0
value=0
while getopts led:v: flag
do
    case "${flag}" in
        led) led_number=${OPTARG};;
        v) value=${OPTARG};;
    esac
done



echo working
cd /sys/class/leds/beaglebone\:green\:usr$led
echo $value > invert
