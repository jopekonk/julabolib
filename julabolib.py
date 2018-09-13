# -*- coding: utf-8 -*-
"""
A library for communicating to Julabo Economy Series CF30/CF40 cooling units
using the serial RS232 interface

Protocol data format is 4800 baud 8E1 (8 bit, parity even, 1 stop bit, hardware handshake)
The input characters are echoed before the response from the unit.
"""
__author__ = "Joonas Konki"
__license__ = "MIT, see LICENSE for more details"
__copyright__ = "2018 Joonas Konki"

import logging
import serial
import time
import re


class JULABO():
	def __init__(self,port,baud):
		self.port = port
		self.ser = serial.Serial( port=self.port,
		                          bytesize=serial.EIGHTBITS,
								  parity=serial.PARITY_EVEN,
								  baudrate=baud,
								  xonxoff=False,
								  rtscts=True,
								  timeout=1 )

		logging.basicConfig(format='julabolib: %(asctime)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S')
		logging.debug('Serial port ' + self.port + 'opened at speed ' + str(baud))

		time.sleep(0.1) # Wait 100 ms after opening the port before sending commands
		self.ser.flushOutput() # Flush the output buffer of the serial port before sending any new commands
		self.ser.flushInput() # Flush the input buffer of the serial port before sending any new commands

	def close(self):
		"""The function closes and releases the serial port connection attached to the unit.

		"""
		if self.ser != None :
			self.ser.close()

	def send_command(self, command=''):
		"""The function sends a command to the unit and returns the response string.

		"""
		if command == '': return ''
		self.ser.write( bytes(command, 'ascii') )
		time.sleep(0.1)
		first_res = self.ser.readline() # read out echoed command
		logging.debug('First response from unit (command): ' + first_res.decode('ascii'))
		second_res = self.ser.readline()
		logging.debug('Second response from unit (response): ' + second_res.decode('ascii'))
		return second_res # return response from the unit

	def flush_input_buffer(self):
		""" Flush the input buffer of the serial port.
		"""
		self.ser.flushInput()

	def set_power_on(self):
		""" The function turns the power ON.

		"""
		response = self.send_command( 'out_mode_05 %d\r' % 1 )

	def set_power_off(self):
		""" The function turns the power OFF.

		"""
		response = self.send_command( 'out_mode_05 %d\r' % 0 )

	def set_work_temperature(self, temp):
		""" The function sets the working temperature to the given value.

		"""
		response = self.send_command( 'out_sp_00 %.2f\r' % temp )

	def get_work_temperature(self, temp):
		""" The function gets the working temperature to the given value.

		"""
		response = self.send_command( 'in_sp_00\r')
		return float(response)

	def get_version(self):
		""" The function gets the software version of the unit.

		"""
		response = self.send_command( 'version\r')
		return response

	def get_status(self):
		""" The function gets the status message or error message from the unit.

		"""
		response = self.send_command( 'status\r')
		return response

	def get_temperature(self):
		""" The function gets the actual bath temperature of the unit

		"""
		response = self.send_command( 'in_pv_00\r')
		return float(response)
