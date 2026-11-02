# for pin layout,  check the following 
# https://rmtplusstoragesenseair.blob.core.windows.net/docs/publicerat/PSP126.pdf

# modified from 
# https://github.com/ndoornekamp/senseair_s8/blob/main/senseair_s8/senseair_s8.py
# and
# https://github.com/orgs/micropython/discussions/10409

import time
from machine import UART, Pin


class SenseairS8Exception(Exception):
    pass


class SenseairS8:
    """
    Interface for the Senseair S8 CO2 sensor over a serial connection.

    This class allows you to communicate with a Senseair S8 sensor to read CO2 concentration values in ppm.

    Example usage:

        from senseair_s8 import SenseairS8
        sensor = SenseairS8()
        co2 = sensor.co2()
        print(f"CO2 concentration: {co2} ppm")

    Args:
        port (str): Serial port device (default: "/dev/ttyS0").
        baudrate (int): Serial baudrate (default: 9600).
        timeout (float): Serial timeout in seconds (default: 0.5).
    """

    #def __init__(self, port: str = "/dev/ttyS0", baudrate: int = 9600, timeout: float = 0.5) -> None:
    #    self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    def __init__(self, uart, tx, rx, timeout: float = 0.5):
        self.uart = UART(uart, baudrate=9600, bits=8, parity=None, stop=1, tx = Pin(tx), rx = Pin(rx))

    def co2(self) -> int:
        """
        Returns the measured CO2 value in parts per million (ppm).

        Returns:
            int: The CO2 concentration in ppm.

        Raises:
            SenseairS8Exception: If reading from the sensor fails.
        """
        try:
            #self.uart.reset_input_buffer()
            self.uart.flush()
            #print("1")
            self.uart.write(b"\xfe\x04\x00\x03\x00\x01\xd5\xc5")
            #print("2")
            time.sleep(1)
            response = self.uart.read()
            #print(response)
            high = response[3]
            low = response[4]
            co2 = (high * 256) + low
        except Exception as e:
            raise SenseairS8Exception("Failed to read CO2 value") from e
        return co2