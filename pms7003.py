import struct
import utime

class PMSError(Exception):
    pass

class PMS7003:
    PMS_FRAME_LENGTH = 0
    PMS_PM1_0 = 1
    PMS_PM2_5 = 2
    PMS_PM10_0 = 3
    PMS_PM1_0_ATM = 4
    PMS_PM2_5_ATM = 5
    PMS_PM10_0_ATM = 6
    PMS_PCNT_0_3 = 7
    PMS_PCNT_0_5 = 8
    PMS_PCNT_1_0 = 9
    PMS_PCNT_2_5 = 10
    PMS_PCNT_5_0 = 11
    PMS_PCNT_10_0 = 12

    def __init__(self, uart):
        self.uart = uart
        self.timeout = 1000  # Timeout in milliseconds

    def __check_uart_bytes(self):
        start_time = utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(), start_time) < self.timeout:
            if self.uart.any():
                if self.uart.read(1) == b'B':
                    if self.uart.any():
                        if self.uart.read(1) == b'M':
                            return True
        raise PMSError("(2) BM header not found or timeout during reception")

    def __read_data(self):
        data = bytearray()
        start_time = utime.ticks_ms()
        while len(data) < 30 and utime.ticks_diff(utime.ticks_ms(), start_time) < self.timeout:
            if self.uart.any():
                data.extend(self.uart.read(min(self.uart.any(), 30 - len(data)))) # Read up to the remaining bytes
        if len(data) != 30:
            raise PMSError("(3) Not all 30 bytes received (Received: {}) Timeout".format(len(data)))
        return data

    def __checksum(self, data):
        checksum = struct.unpack('>H', data[28:30])[0]
        calculated_checksum = sum(bytearray(b'BM') + data[:28]) & 0xFFFF
        if checksum != calculated_checksum:
            raise PMSError("(4) Checksum error. Calculated: {}, Received: {}".format(calculated_checksum, checksum))
        return True

    def read_data(self):
        try:
            if self.__check_uart_bytes():
                data = self.__read_data()
                if self.__checksum(data):
                    values_data = struct.unpack(">HHHHHHHHHHHHH", data[:28])
                    return {
                        "FRAME_LENGTH": values_data[self.PMS_FRAME_LENGTH],
                        "PM1.0_CF1": values_data[self.PMS_PM1_0],
                        "PM2.5_CF1": values_data[self.PMS_PM2_5],
                        "PM10.0_CF1": values_data[self.PMS_PM10_0],
                        "PM1.0_ATM": values_data[self.PMS_PM1_0_ATM],
                        "PM2.5_ATM": values_data[self.PMS_PM2_5_ATM],
                        "PM10.0_ATM": values_data[self.PMS_PM10_0_ATM],
                        "PM_CNT_0_3UM": values_data[self.PMS_PCNT_0_3],
                        "PM_CNT_0_5UM": values_data[self.PMS_PCNT_0_5],
                        "PM_CNT_1_0UM": values_data[self.PMS_PCNT_1_0],
                        "PM_CNT_2_5UM": values_data[self.PMS_PCNT_2_5],
                        "PM_CNT_5_0UM": values_data[self.PMS_PCNT_5_0],
                        "PM_CNT_10_0UM": values_data[self.PMS_PCNT_10_0]
                    }
                else:
                    return None
            else:
                return None
        except PMSError as e:
            print(e)
            return None
