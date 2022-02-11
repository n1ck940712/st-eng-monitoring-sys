#!/home/pi/monitoring_sys/env/bin/ python3
# -*- coding: utf-8 -*- 
# ================================================================
# ST Engineering remote monitoring system 
# version 1.0
# last edit: 19/11/2021
# Flotech Controls
# ================================================================
from modules import database, logger
from modules import sierra_flow_controller as flow_ctrl
from modules import btu_981
import time, threading, os


# =================================================================
# functions
# =================================================================

def update_database(_type, value):
    database.query('local', 'update', 'UPDATE app_sensorreading SET value=%s WHERE name="%s"' % (value, _type))
    return


# =================================================================
# threads
# =================================================================

class update_reading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global flow_controller, pressure, temperature
        log.info("update_reading started")
        while 1:
            flow = flow_ctrl.get_flow(flow_controller)
#             print(flow) # NL/min
            update_database('n2 flow rate', flow)
            pres = btu_981.get_pressure(pressure)
#             print(pres) # kpa
            update_database('pressure', pres)
            temp = btu_981.get_temperature(temperature)
#             print(temp)  #celsius
            update_database('temperature', temp)
            
            row = database.query('local', 'get', 'SELECT status, set_point FROM app_sensorreading WHERE name="n2 flow rate"')[0]
            if row[0] == '1':
                flow_ctrl.set_setpoint(flow_controller, float(row[1]))
                log.info('flow rate setpoint: %s L/min' % row[1])
                database.query('local', 'update', 'UPDATE app_sensorreading SET status="0" WHERE name="n2 flow rate"')
            
            time.sleep(1)



# =================================================================
# MAIN PROGRAM
# =================================================================

if __name__ == '__main__':
    log = logger.init(os.path.abspath(__file__), 'info') # logging
    database.init(log) # database
    # end init
    log.info("Modules Initiation DONE...")
    log.info("===============================\n")
    log.info("%s RUNNING..." % os.path.splitext(os.path.basename(__file__))[0])
    
    # main program
    flow_controller = flow_ctrl.init('/dev/ttySC0', 1)
    temperature = btu_981.init('/dev/ttySC0', 3)
    pressure = btu_981.init('/dev/ttySC0', 2)
    update_reading().start()