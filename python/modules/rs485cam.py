import time, binascii
from hexbytes import HexBytes

def init(logger, ser_cam):
    global log, ser, IMG_RAW_DIR, IMG_DIR
    log = logger
    ser = ser_cam
    IMG_RAW_DIR = '/home/pi/radar_level/images/raw/'
    IMG_DIR = '/home/pi/radar_level/images/'

def set_osd(timestamp):
    try:
        OSD_Timestamp = timestamp.encode('utf-8').hex()
        OSD_Extra = str(' (Station 1)').encode('utf-8').hex()
        OSD_Length = hex(int(len(OSD_Extra)/2+25))[2:]
        OSD_Timestamp_Hex = '90 EB 01 52 '+str(OSD_Length)+' 00 06 00 08 00 0A '+str(OSD_Timestamp)+str(OSD_Extra)+' C1 C2'
        OSD_Timestamp_Hex = bytes(HexBytes(OSD_Timestamp_Hex.replace(' ','')))
        ser.write(OSD_Timestamp_Hex)
        while ser.in_waiting == 0:
            time.sleep(0.1)
        if ser.readline():
            log.debug('Setting OSD Successful!')
        else:
            log.error('Settings OSD Failed!')
    except Exception as e:
        log.error('write osd FAILED. %s' % e)
    return

def retrieve(file_name):
    try:
        log.debug('Receiving image')
        imgdata = ''
        packet_start_add = '00 00 00 00'
        packet_length = 'ff ff'
        for i in range(2):
            get_image_hex = '90 EB 01 48 06 00 %s %s C1 C2' % (packet_start_add, packet_length)
            Get_Image_Hex = bytes(HexBytes(get_image_hex.replace(' ','')))
            ser.write(Get_Image_Hex)
            time.sleep(0.1)
            while ser.in_waiting>0:
                imgdata += ser.readall().hex()[12:-4]
            packet_start_add = int(packet_length.replace(' ', ''), 16) + int(packet_start_add.replace(' ', ''), 16)
            packet_start_add = '{:08x}'.format(packet_start_add)
            packet_start_add = packet_start_add[-4:]+packet_start_add[0:4]

        raw_file_name = raw_file_name = IMG_RAW_DIR + file_name + "_image.txt"
        with open(raw_file_name, 'w+') as file:
            file.write(imgdata)
    except Exception as e:
        log.error("Receiving image from camera failed...%s" % e)
    return


def convert_raw(file_name):
    try:
        log.debug('converting image')
        raw_file_name = IMG_RAW_DIR + file_name + "_image.txt"
        image_file_name = IMG_DIR + file_name + "_image.jpg"
        data_read = open(str(raw_file_name),'r')
        data = binascii.a2b_hex(data_read.read().strip().replace(' ', '').replace('\n', ''))
        data_read.close()
        with open(str(image_file_name), 'wb') as image_file:
            image_file.write(data)
    except Exception as e:
        log.error("Converting image FAILED. %s" % e)
    return


def snapshot():
    Capture_Hex = bytes(HexBytes('90 EB 01 40 04 00 00 02 05 01 C1 C2'.replace(' ','')))
    ser.write(Capture_Hex)
    while ser.in_waiting == 0:
        time.sleep(0.1)
    if ser.readall():
        log.debug('Capture image Successful!')
    else:
        log.error('Capture image Failed!')
    return