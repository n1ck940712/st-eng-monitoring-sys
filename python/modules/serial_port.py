import serial

def init(logger):
    global log
    log = logger
    global ser_radar, ser_cam
    try:
        Comm_Port = '/dev/ttySC0'
        Baud_Rate = 9600
        ser_radar = serial.Serial(Comm_Port, Baud_Rate, timeout = 1)
    except Exception as e:
        log.error('%s init FAILED. %s' % (Comm_Port, e))
    try:
        Comm_Port = '/dev/ttySC1'
        Baud_Rate = 115200
        ser_cam = serial.Serial(Comm_Port, Baud_Rate, timeout = 1)
    except Exception as e:
        log.error('%s init FAILED. %s' % (Comm_Port, e))

    return ser_radar, ser_cam