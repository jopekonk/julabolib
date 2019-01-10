#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Example script to read the status from the julabo unit
# 20190110 - Joonas Konki

import julabolib
import time

mychiller = julabolib.JULABO('/dev/ttyUSB2', baud=4800)

val = mychiller.get_status()
print("Julabo status is: " + val)

val = mychiller.get_version()
print("Julabo version is: " + val)

val = mychiller.get_work_temperature()
print("Julabo working temperature is: " + str(val) )

val = mychiller.get_temperature()
print("Julabo actual bath temperature is: " + str(val) )

val = mychiller.get_power()
print("Julabo power mode is (1 == ON, 0 == OFF): " + str(val) )

mychiller.close()
