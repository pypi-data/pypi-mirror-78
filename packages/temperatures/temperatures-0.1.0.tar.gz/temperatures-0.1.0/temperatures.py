#! /usr/bin/python3

import collections
import json
import re
import socket
import subprocess


__version__ = "0.1.0"


HDDTEMP_ADDR = ("localhost", 7634)


# Run `sensors -jA` in a terminal and pick the paths
# to the temperatures of interest
SENSORS_OUTPUT_SELECTORS = [
    # (device name, path to temperature value in sensors JSON output)
    ("cpu", ("k10temp-pci-00c3", "Tdie", "temp1_input")),
    ("gpu", ("amdgpu-pci-0800", "temp1", "temp1_input")),
]


def netcat(addr):
    with socket.create_connection(addr, 2) as sock:
        chunk = sock.recv(1024)
        while chunk:
            yield chunk
            chunk = sock.recv(1024)


def parse_hddtemp_output(output):
    """
        >>> output = (
        ...     "|/dev/sdc|WDC WD20EFRX-68EUZN0|29|C|"
        ...     "|/dev/sdd|WDC WD20EFRX-68EUZN0|31|C|"
        ...     "|/dev/sde|WDC WD20EFRX-68EUZN0|28|C|"
        ... )
        >>> for device, temperature in parse_hddtemp_output(output):
        ...     print(device, temperature)
        /dev/sdc 29
        /dev/sdd 31
        /dev/sde 28

    """
    pattern = \
        r'\|(?P<device>/dev/[^\|]+)\|(?P<model>[^\|]+)\|(?P<temperature>[0-9]+)\|C\|'
    for match in re.finditer(pattern, output):
        yield match.group("device"), int(match.group("temperature"))


def extract_tree_value(data, path):
    for key in path:
        if not key in data:
            return None
        data = data[key]
    return data    


def parse_sensors_output(data):
    data = json.loads(data)
    for device, path in SENSORS_OUTPUT_SELECTORS:
        temperature = extract_tree_value(data, path)
        if temperature is not None:
            yield device, int(temperature)


def format_output(temperatures):
    return "     ".join(
        f"{device.split('/')[-1]} {temperature}°C"
        for device, temperature in temperatures
    )


def main():
    temperatures = []
    try:
        data = b''.join(netcat(HDDTEMP_ADDR)).decode('utf-8')
        temperatures.extend(parse_hddtemp_output(data))
    except Exception as ex:
        print("Error:", ex.message, file=sys.stderr)
    try:
        data = subprocess.check_output(["sensors", "-j", "-A"])
        temperatures.extend(parse_sensors_output(data))
    except Exception as ex:
        print("Error:", ex.message, file=sys.stderr)
    print(format_output(temperatures))


if __name__ == '__main__':
    main()
