
# PMS7003 MicroPython

Python driver to interface with the PMS7003 particulate matter sensor via UART. It reads particulate matter (PM1.0, PM2.5, PM10) and returns the data in a readable format.

## Requirements
- Microcontroller with UART support (e.g., ESP32, Raspberry Pi Pico).
- PMS7003 sensor.

## Installation
1. Clone or download the repository.
2. Import the `PMS7003` class into your project.

## Example Usage

```python
from machine import Pin, UART
from pms7003 import PMS7003
import time

# UART configuration
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Initialize PMS7003 sensor
pms_init = PMS7003(uart1)

# Main loop
while True:
    try:
        pm_data = pms_init.read_data()
        if pm_data:
            print(pm_data)  # Print sensor data
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
```

## Data Returned
- **FRAME_LENGTH**: Length of the data frame.
- **PM1.0_CF1, PM2.5_CF1, PM10.0_CF1**: Concentration of PM particles (µg/m³).
- **PM_CNT_UM**: Particle counts in various size ranges.