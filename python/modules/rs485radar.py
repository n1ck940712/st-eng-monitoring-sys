from hexbytes import HexBytes
from modules import database
import struct

def init(logger, ser_radar):
    global log, ser
    log = logger
    ser = ser_radar

def hex_to_float(hex):
    # Float - Mid-Little Endian (CDAB)
    try:
        if len(hex) == 8:
            hex = hex[4:8] + hex[0:4]
            float = struct.unpack('!f', bytes.fromhex(hex))[0]
        else:
            log.error('hex_to_float failed. Lenght of hex string should be 8, but instead it is %s' % len(hex))
    except Exception as e:
        log.error('hex_to_float failed. %s' % e)
    return float


def read():
    global ser_radar
    try:
        log.info('Reading radar')
        read_radar_command = bytes(HexBytes('01 04 0A 0F 00 02 42 10'.replace(' ','')))
        ser.write(read_radar_command)
        response = ser.readall().hex()
        reading = round(hex_to_float(response[6:14]), 4)
        log.debug('Read Radar: %s' % reading)
        insert_reading(reading)
    except Exception as e:
        log.error('read_radar failed. %s' % e)
    return reading


def insert_reading(reading):
    try:
        database.query('remote', 'insert', "INSERT INTO radar_reading (id, level) VALUES (NULL, '%s')" % reading)
        log.debug('Reading inserted.')
    except Exception as e:
        log.error('insert_database failed. %s' % e)
    return
    