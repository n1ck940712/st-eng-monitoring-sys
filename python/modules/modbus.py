import time
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def init(baudrate, parity, port):
    client = ModbusClient(method='rtu', port=port, baudrate=baudrate, parity=parity, timeout=1)
    return client

def read(client, device_id, register_address, number_of_register, data_format):
    register_address-=1
    try:
        client.connect()
        read=client.read_holding_registers(address=register_address ,count=number_of_register, unit=device_id)
        if data_format == '32bit float':
            decoder = BinaryPayloadDecoder.fromRegisters(read.registers, Endian.Big, wordorder=Endian.Little)
            result = decoder.decode_32bit_float()
        elif data_format == '16bit int':
            result = read.registers[0]
        client.close()
    except Exception as e:
        result = 0
        print('failed to read %s' % e)
    return result

def write(client, device_id, register_address, value, data_format):
    register_address-=1
    try:
        client.connect()
        if data_format == '32bit float':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            builder.add_32bit_float(value)
            registers = builder.to_registers()
            print('modbus write float:%s ' % registers)
            client.write_registers(register_address, registers, unit=device_id)
        elif data_format == '16bit int':
            client.write_register(register_address, value, unit=device_id)
    except Exception as e:
        print('failed to write %s' % e)
    return
    


# temperature = init(9600, 'N', '/dev/ttySC0')
# pressure = init(9600, 'N', '/dev/ttySC0')
# flow_controller = init(19200, 'E', '/dev/ttySC0')
# 
# write(flow_controller, 1, 35, 1, '16bit int')
# result = read(flow_controller, 1, 35, 1, '16bit int')
 
# while 1:
#     
#     result = read(temperature, 3, 5, 2, '32bit float')
#     print('\ntemperature: %s Celsius' % result)
#     
#     result = read(pressure, 2, 7, 2, '32bit float')
#     print('pressure: %s kPa' % result)
# 
#     result = read(flow_controller, 1, 3, 2, '32bit float')
#     print('flow: %s ' % result)
#     
#     
#     time.sleep(1)