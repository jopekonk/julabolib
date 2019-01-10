#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script to turn the JULABO chiller OFF.
# Requires that the remote control has been enabled.
# 20190110 - Joonas Konki
import julabolib

mychiller = julabolib.JULABO('/dev/ttyUSB2', baud=4800)

print("Sending turn OFF command")
val = mychiller.set_power_off()

val = mychiller.get_power()
print("Julabo power is (1 == ON, 0 == OFF): " + str(val) )

mychiller.close()
