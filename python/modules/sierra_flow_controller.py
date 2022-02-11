import time
from modules import modbus as mb
  
def init(port, device_id):
    flow_controller_client = mb.init(19200, 'E', port)
    return flow_controller_client, device_id

def get_flow(client):
    return mb.read(client[0], client[1], 1, 2, '32bit float')

def set_setpoint(client, value):
    mb.write(client[0], client[1], 3, value, '32bit float')
    return

def get_setpoint(client):
    return mb.read(client[0], client[1], 3, 2, '32bit float')
    

if __name__ == '__main__':
    c = init('/dev/ttySC0', 1)
    print(c[0])
    print(c[1])
    print(get_setpoint(c))