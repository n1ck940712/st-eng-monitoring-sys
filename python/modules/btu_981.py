import time
from modules import modbus as mb
  
def init(port, device_id):
    btu_981_client = mb.init(9600, 'N', port)
    return btu_981_client, device_id

def get_temperature(client):
    return mb.read(client[0], client[1], 5, 2, '32bit float')

def get_pressure(client):
    return mb.read(client[0], client[1], 7, 2, '32bit float')



if __name__ == '__main__':
    pass
#     c = init('/dev/ttySC0', 1)
#     print(c[0])
#     print(c[1])
#     print(get_setpoint(c))
