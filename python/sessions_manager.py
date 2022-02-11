#!/home/pi/monitoring_sys/env/bin/ python3
# -*- coding: utf-8 -*- 
# ================================================================
# ST Engineering remote monitoring system - main application script
# version 1.0
# last edit: 24/11/2021
# Flotech Controls
# ================================================================


from modules import database, logger, encrypt, buzzer
import time, threading, os, json, websocket, report
from datetime import datetime, timedelta


# =================================================================
# global variables
# =================================================================
sessions_list = {}

# =================================================================
# program functions
# =================================================================
def websocket_send(data, ip_address):
    return

def force_logout(ip_address):
    global ws
    log.debug('<SESSION MANAGER> force logout: %s' % (ip_address))
    data = {
        'message': {},
        'message_type': 'force logout',
        'recipient_ip': ip_address,
    }
    time.sleep(0.2)
    ws.send(json.dumps({
        'data': data,
        'sender': 'python',
    }))
    time.sleep(0.2)
    return


# =================================================================
# threads
# =================================================================

class connection_thread(threading.Thread):
    def __init__(self, websocket):
        threading.Thread.__init__(self)
        self.websocket = websocket

    def run(self):
        global ws
        log.info("connection_thread started")
        while 1:
            try:
                    # ws_url = "ws://localhost:8009/ws/socket/" # development
                    ws_url = "ws://0.0.0.0:8001/ws/socket/" # production
                    ws = self.websocket.WebSocketApp(ws_url,
                                    on_open = self.on_open,
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
                    ws.run_forever()
            except Exception as e:
                log.error('connection_thread ERROR. %s' % e)
            time.sleep(10)

    def on_open(self, ws):
        global websocket_connected
        websocket_connected = True

    def on_error(self, ws, error):
        log.debug('on_error. %s' % (error))

    def on_close(self, ws, close_status_code, close_msg):
        global websocket_connected
        websocket_connected = False
        log.debug('on_close. %s. %s' % (close_status_code, close_msg))

    def on_message(self, ws, data):
        decoded_data = json.loads(data)
        if decoded_data['data']['message_type'] == 'sessions':
            log.debug('<SESSIONS MANAGER>: ---> %s' % (data))
            ip_address = decoded_data['data']['ip_address']
            username = decoded_data['data']['username']
            if username != 'guest':
                if username not in sessions_list:
                    sessions_list[username] = ip_address
                    print(sessions_list)
                else:
                    force_logout(sessions_list[username])
                    sessions_list[username] = ip_address
                    print(sessions_list)
        return


# =================================================================
# MAIN PROGRAM
# =================================================================

if __name__ == "__main__":
    # init modules
    log = logger.init(os.path.abspath(__file__), '') # logging
    database.init(log) # database
    cipher = encrypt.init(log) # encryption
    buzzer.init()
    # end init
    log.info("Modules Initiation DONE...")
    log.info("===============================\n")
    log.info("%s RUNNING..." % os.path.splitext(os.path.basename(__file__))[0])
    
    # main program
    connection_thread(websocket).start()
    