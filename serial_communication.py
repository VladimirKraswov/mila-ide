import serial
import time

class SerialCommunication:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate)

    def send_data(self, data):
        self.ser.write(data.encode())

    def read_data(self):
        if self.ser.in_waiting > 0:
            return self.ser.read(self.ser.in_waiting).decode()
        return ""