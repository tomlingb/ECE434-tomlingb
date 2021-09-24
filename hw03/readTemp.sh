#!/bin/bash

i2cset -y 2 0x4a 3 0x19
while [ True ] 
do
	temp1=$(i2cget -y 2 0x4a 0)
	temp2=$(i2cget -y 2 0x48 0)
	temp1F=$(($(($(($temp1*9))/5))+32))
	temp2F=$(($(($(($temp2*9))/5))+32))
	echo $temp1F
	echo $temp2F
done
