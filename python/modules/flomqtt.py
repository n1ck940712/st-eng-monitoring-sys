# =================================================================
# mqtt configurations
# =================================================================
from modules import encrypt, database
import paho.mqtt.client as mqtt 
import time, ssl, threading

def init(logger):
    try:
        global CERT_DIR, ADDRESS, PORT, USERNAME, PASSWORD, CHANNEL, log, CLIENT_ID, connected, cipher, IMG_RAW_DIR
        log = logger
        CLIENT_ID = 'radar_reader'
        CERT_DIR = "/home/pi/radar_level/certs/wqa600.pem"
        ADDRESS = "wqa600.flotech.io"
        PORT = 8883
        USERNAME = "flotech_mqtt"
        PASSWORD = "Flotechpassmqtt123!"
        CHANNEL = "flotechio/radar_level_monitoring"
        connected = False
        
        cipher = encrypt.init(log) # encryption
        IMG_RAW_DIR = '/home/pi/radar_level/images/raw/'
        log.info('init SUCCESS')
    except Exception as ex:
        log.info('init FAILED. %s' % ex)
    return


class mqtt_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log.info("Mqtt_thread started")
        global client
        global connected
        connected = False
        while(1):
            try:
                log.info("Connecting to MQTT broker")            
                client = mqtt.Client(client_id=CLIENT_ID)
                client.on_connect = self.on_connect
                client.on_disconnect = self.on_disconnect
                client.on_message = self.on_message
                client.username_pw_set(username=USERNAME,password=PASSWORD)
                client.tls_set(CERT_DIR, None, None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
                client.connect(ADDRESS, PORT, 10)
                client.loop_forever()
            except Exception as e:
                log.error("Mqtt_thread error. Reconnecting...\n"+str(e))    
            time.sleep(5)

    def on_disconnect(self, client, userdata, msg):
        global connected
        log.warning("Disonnected from MQTT broker. Reconnecting...")
        connected = False
        time.sleep(5)


    def on_connect(self, client, userdata, msg, rc):
        global connected
        log.info("Connected to MQTT broker")
        client.subscribe(CHANNEL+"/#")
        connected = True


    def on_message(self, client, userdata, msg):
        data = str(msg.payload.decode('utf-8'))
        try:
            if encrypt.PRIVATE_KEY_2 in data:
                data_decrypted = cipher.decrypt(bytes(data.replace(encrypt.PRIVATE_KEY_2,""),"utf-8")).decode("utf-8").split(',')
                data_type = data_decrypted[0]
                if data_type == 'settings':
                    high_alarm = data_decrypted[1]
                    high_high_alarm = data_decrypted[2]
                    sampling_interval = data_decrypted[3]
                    data_transmission_interval = data_decrypted[4]
                    cam_capture = data_decrypted[5]
                    database.query('local', 'update', 'UPDATE settings SET high_alarm=%s, high_high_alarm=%s, sampling_interval=%s, data_transmission_interval=%s, cam_capture=%s WHERE id=1' % (high_alarm, high_high_alarm, sampling_interval, data_transmission_interval, cam_capture))
                    log.info('%s received: msg(%s)' % (data_type, data_decrypted))
                elif data_type == 'reading':
                    pass
        except Exception as e:
            log.error('parse_message FAILED. %s' % e)
        return

def send_mqtt(mode, msg):
    global client
    if connected:
        try:
            if mode == 'reading':
                data ="%s,%s" % (mode, msg)
                data_encrypted = cipher.encrypt(bytes(data,"utf-8")).decode("utf-8")
                client.publish(CHANNEL, encrypt.PRIVATE_KEY_2+data_encrypted, qos=1)

            elif mode == 'image':
                file_name = msg
                image_data = open(IMG_RAW_DIR+file_name+'_image.txt', 'rb').read()
                data ="%s,%s,%s" % (mode, file_name, image_data)
                data_encrypted = cipher.encrypt(bytes(data,"utf-8")).decode("utf-8")
                client.publish(CHANNEL, encrypt.PRIVATE_KEY_2+data_encrypted, qos=1)

            elif mode == 'alarm':
                data ="%s,%s" % (mode, msg)
                data_encrypted = cipher.encrypt(bytes(data,"utf-8")).decode("utf-8")
                client.publish(CHANNEL, encrypt.PRIVATE_KEY_2+data_encrypted, qos=1)

            log.info("%s Sent: (%s)" % (mode, msg))
                
        except Exception as e:
            log.error("Send_mqtt error!\n"+str(e)) 
    return

        
def connect():
    mqtt_thread().start()
    return