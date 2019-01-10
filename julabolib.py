# -*- coding: utf-8 -*-
"""
A library for communicating to Julabo Economy Series CF30/CF40/FL11006 cooling units
using the serial RS232 interface

Protocol data format is 4800 baud 7E1 (7 bit, parity even, 1 stop bit, hardware handshake)
"""
__author__ = "Joonas Konki"
__license__ = "MIT, see LICENSE for more details"
__copyright__ = "2018 Joonas Konki"

import logging
import serial
import time
import re

# Set the minimum safe time interval between sent commands that is required according to the user manual
SAFE_TIME_INTERVAL = 0.25

END_CHAR = '\x0D'

class JULABO():
	def __init__(self,port,baud):
		self.port = port
		self.ser = serial.Serial( port=self.port,
					  bytesize=serial.SEVENBITS,
					  parity=serial.PARITY_EVEN,
					  stopbits=serial.STOPBITS_ONE,
					  baudrate=baud,
					  xonxoff=False,
					  rtscts=True,
					  timeout=1 )

		logging.basicConfig(format='julabolib: %(asctime)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.WARNING)
		#logging.basicConfig(format='julabolib: %(asctime)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.DEBUG)
		logging.debug('Serial port ' + self.port + ' opened at speed ' + str(baud))

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
		time.sleep(SAFE_TIME_INTERVAL)
		self.ser.write( bytes( command+END_CHAR , 'ascii') )
		time.sleep(0.1)
		logging.debug('Command sent to the unit: ' + command)
		response = self.ser.readline()
		logging.debug('Response from unit: ' + response.decode('ascii'))
		return response.decode('ascii') # return response from the unit

	def flush_input_buffer(self):
		""" Flush the input buffer of the serial port.
		"""
		self.ser.flushInput()

	def set_power_on(self):
		""" The function turns the power ON.

		"""
		response = self.send_command( 'out_mode_05 %d' % 1 )

	def set_power_off(self):
		""" The function turns the power OFF.

		"""
		response = self.send_command( 'out_mode_05 %d' % 0 )

	def get_power(self):
		""" The function gets the power state of the unit.
			1 == ON
			0 == OFF

		"""
		response = self.send_command( 'in_mode_05' )
		return response

	def set_work_temperature(self, temp):
		""" The function sets the working temperature to the given value.

		"""
		response = self.send_command( 'out_sp_00 %.2f' % temp )

	def get_work_temperature(self):
		""" The function gets the working temperature to the given value.

		"""
		response = self.send_command( 'in_sp_00')
		return float(response)

	def get_version(self):
		""" The function gets the software version of the unit.

		"""
		response = self.send_command( 'version')
		return response

	def get_status(self):
		""" The function gets the status message or error message from the unit.

		"""
		response = self.send_command( 'status')
		return response

	def get_temperature(self):
		""" The function gets the actual bath temperature of the unit

		"""
		response = self.send_command( 'in_pv_00')
		return float(response)
