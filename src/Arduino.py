import serial
from typing import List

import numpy as np

from src.refsys.system import ReferenceSystem
from src.refsys.vector import Vector


class Arduino:
    def __init__(self, serial_port, ref_sys_list: List[ReferenceSystem]):
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.ref_sys_list = ref_sys_list

    def set_computer_position(self, arduino_computer: np.ndarray):
        """Set computer position with respect to arduino reference system"""
        self.arduino_computer = arduino_computer

    def send_coordinates(self, target: Vector):
        """Send pan and tilt angles in degrees through serial communication"""
        target.to(self.ref_sys_list[-1])

        pan = np.arccos(-target.array[0] / np.sqrt(target.array[0]**2 + target.array[2]**2))
        tilt = np.arccos(-target.array[1] / np.sqrt(target.array[1]**2 + target.array[2]**2))

        pan = np.rad2deg(pan)
        tilt = np.rad2deg(tilt)
        
        data = f"{int(pan)},{int(tilt)}\n"
        self.ser.write(data.encode("utf-8"))

    def close(self):
        self.ser.close()
