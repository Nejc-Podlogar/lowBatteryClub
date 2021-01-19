# This Python file uses the following encoding: utf-8
import serial
import sys


class STM32F411:
    def __init__(self, **kwargs):
        self.sensorOpen = True
        self.port = 'COM7'
        self.baudrate = 115200
        self.timeout = None
        self.parity = serial.PARITY_NONE
        self.bytesize = 8
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, parity=self.parity, bytesize=self.bytesize)
        except:
            self.sensorOpen = False

    def read_line_from_port(self):
        try:
            return self.ser.readline()
        except:
            print(sys.exc_info)
            return ""

    def is_sensor_open(self):
        return self.sensorOpen

    def get_port(self):
        return self.port

    def get_baudrate(self):
        return self.baudrate

    def get_timeout(self):
        return self.timeout

    def get_parity(self):
        return self.parity

    def get_bytesize(self):
        return self.bytesize
