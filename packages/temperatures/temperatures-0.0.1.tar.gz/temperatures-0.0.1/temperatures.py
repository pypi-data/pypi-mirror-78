#! /usr/bin/python3

import collections
import re
import socket


__version__ = "0.0.1"


HOST = "localhost"
PORT = 7634


def netcat(host, port):
    with socket.create_connection((HOST, PORT), 2) as sock:
        chunk = sock.recv(1024)
        while chunk:
            yield chunk
            chunk = sock.recv(1024)


HddTempRecord = collections.namedtuple("HddTempRecord", "device, model, temperature")


def parse_hddtempd_output(output):
    """
        >>> output = (
        ...     "|/dev/sdc|WDC WD20EFRX-68EUZN0|29|C|"
        ...     "|/dev/sdd|WDC WD20EFRX-68EUZN0|31|C|"
        ...     "|/dev/sde|WDC WD20EFRX-68EUZN0|28|C|"
        ... )
        >>> for record in parse_hddtempd_output(output):
        ...     print(repr(record))
        HddTempRecord(device='/dev/sdc', model='WDC WD20EFRX-68EUZN0', temperature=29)
        HddTempRecord(device='/dev/sdd', model='WDC WD20EFRX-68EUZN0', temperature=31)
        HddTempRecord(device='/dev/sde', model='WDC WD20EFRX-68EUZN0', temperature=28)

    """
    pattern = \
        r'\|(?P<device>/dev/[^\|]+)\|(?P<model>[^\|]+)\|(?P<temperature>[0-9]+)\|C\|'
    for match in re.finditer(pattern, output):
        yield HddTempRecord(
            device=match.group("device"),
            model=match.group("model"),
            temperature=int(match.group("temperature"))
        )


def format_records(records):
    return " | ".join(
        f"{r.device.split('/')[-1]} {r.temperature}°C"
        for r in records
    )


def main():
    try:
        data = b''.join(netcat(HOST, PORT)).decode('utf-8')
        records = parse_hddtempd_output(data)
        print(format_records(records))
    except Exception as ex:
        print("Error:", ex.message, file=sys.stderr)

if __name__ == '__main__':
    main()
