#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script to set the working temperature of the JULABO chiller.
# 20190110 - Joonas Konki
import julabolib
import sys

if len(sys.argv) != 2:
	print("Usage: ./julabo_set_temp [TEMP]")
	print("where TEMP is the desired working temperature.")
	exit()

mychiller = julabolib.JULABO('/dev/ttyUSB2', baud=4800)

new_temp = float(sys.argv[1])

print("Setting working temperature to " + str(new_temp))
val = mychiller.set_work_temperature(new_temp)


val = mychiller.get_work_temperature()
print("Julabo working temperature is: " + str(val) )

val = mychiller.get_temperature()
print("Julabo actual bath temperature is: " + str(val) )

mychiller.close()
