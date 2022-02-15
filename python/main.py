#!/home/pi/monitoring_sys/env/bin/ python3
# -*- coding: utf-8 -*- 
# ================================================================
# ST Engineering remote monitoring system - main application script
# version 1.0
# last edit: 24/11/2021
# Flotech Controls
# ================================================================


from modules import database, logger, encrypt, buzzer
import os, subprocess, time, threading, json, websocket, report
from datetime import datetime, timedelta


# =================================================================
# global variables
# =================================================================
# pre production
pre_production_receive_input = False
pre_production_start_logging = False
deactivate_flow_pre_production = False

# production 1
production_1_receive_input = False
production_1_start_logging = False
change_heater_set_production_1 = False

# production 2
start_production_2 = False
production_2_receive_input = False
production_2_start_logging = False

# production 3
start_production_3 = False
production_3_receive_input = False
production_3_start_logging = False
release_vacuum_production_3 = False

# post production 1
post_production_1_receive_input = False
# post production 2
post_production_2_receive_input = False
# post production 3
post_production_3_receive_input = False


event = threading.Event()
recipient_ip = ''
dont_prompt_deviation_until = datetime(2000, 1, 1)
process_run = False

# =================================================================
# program functions
# =================================================================

def report_export_response(result):
    if (result == 0):
        success = True
        message = 'Report exported successfully'
    elif (result == 1):
        success = False
        message = 'Report failed to export'
    elif (result == 2):
        success = False
        message = 'No USB storage device found. Report failed to export.'
    else:
        success = False
        message = 'Report failed to export'
    data = {
        'message': {
            'success': success,
            'message': message,
            },
        'message_type': 'export response',
    }
    websocket_send(data)
    return

def delete_report(message):
    try:
        database.query('local', 'update', 'DELETE FROM app_report WHERE file_name="%s"' % message['file_name'])
        subprocess.run(['sudo', 'rm', "/home/pi/monitoring_sys/core/static/assets/reports/%s.pdf" % message['file_name']])
        success = True
        message = 'Report deleted successfully.'
    except:
        success = False
        message = 'Failed to delete report.'
    data = {
        'message': {
            'success': success,
            'message': message,
            },
        'message_type': 'report delete response',
    }
    websocket_send(data)
    return


def update_report(message):
    variable_list = []
    for variable in message['variable_list']:
        if variable['variable'] == 'edit report name':
            edit_report_name = variable['value']
        else:
            variable_list.append(variable)

    batch_id = database.query('local', 'get', 'SELECT id FROM app_report WHERE file_name="%s"' % edit_report_name)[0][0]
    report_edit_fault = report.generate(log, batch_id, variable_list)
    if not report_edit_fault:
        success = True
    else:
        success = False
    data = {
        'message': {
            'success': success
        },
        'message_type': 'report edit',
    }
    websocket_send(data)
    return

def trigger_alarm(state='on'):
    if state == 'on':
        buzzer.turn_on()
    elif state == 'off':
        buzzer.turn_off()
    data = {
            'message': state,
            'message_type': 'trigger alarm',
        }
    websocket_send(data)
    return

def generate_report(process_name):
    database.query('local', 'insert', 'INSERT INTO app_report (`type`, time_completed) VALUES ("%s", "%s")' % (process_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    batch_id = database.query('local', 'get', 'SELECT id FROM app_report ORDER BY id DESC LIMIT 1')[0][0]
    report.generate(log, batch_id)
    return


def check_deviation(process):
    pressure_deviated = False
    temperature_deviated = False
    n2_flow_rate_deviated = False
    param_dict = {}
    next_check_time = datetime(2000, 1, 1)

    while process_run:
        if datetime.now() > next_check_time:
            if process == 'production part 1':
                param_dict['set n2 flow rate'] = get_variable('n2 flow rate', 'production part 1')[0]
                param_dict['n2 flow rate tolerance'] = get_variable('n2 flow rate tolerance', 'production part 1')[0]
                param_dict['set pressure'] = get_variable('pressure', 'production part 1')[0]
                param_dict['pressure tolerance'] = get_variable('pressure tolerance', 'production part 1')[0]
            elif process == 'production part 2':
                param_dict['set n2 flow rate'] = get_variable('n2 flow rate', 'production part 2')[0]
                param_dict['n2 flow rate tolerance'] = get_variable('n2 flow rate tolerance', 'production part 2')[0]
                param_dict['set pressure'] = get_variable('pressure', 'production part 2')[0]
                param_dict['pressure tolerance'] = get_variable('pressure tolerance', 'production part 2')[0]
                param_dict['set temperature'] = get_variable('set temperature', 'production part 2')[0]
                param_dict['temperature tolerance'] = get_variable('temperature tolerance', 'production part 2')[0]
            elif process == 'production part 3':
                param_dict['set n2 flow rate'] = get_variable('n2 flow rate', 'production part 3')[0]
                param_dict['n2 flow rate tolerance'] = get_variable('n2 flow rate tolerance', 'production part 3')[0]
                param_dict['set pressure'] = get_variable('pressure', 'production part 3')[0]
                param_dict['pressure tolerance'] = get_variable('pressure tolerance', 'production part 3')[0]
                param_dict['set temperature'] = get_variable('set temperature', 'production part 3')[0]
                param_dict['temperature tolerance'] = get_variable('temperature tolerance', 'production part 3')[0]

            alert_message = ''
            if 'set pressure' in param_dict:
                current_pressure = read_pressure()[0]
                if abs(current_pressure - param_dict['set pressure']) > param_dict['pressure tolerance']:
                    alert_message += '&bull;pressure deviated (current: %skPa | set: %skPa | tolerance: %skPa)<br>' % (current_pressure, param_dict['set pressure'], param_dict['pressure tolerance']
                    )
                    pressure_deviated = True
                else:
                    pressure_deviated = False
                    
            if 'set n2 flow rate' in param_dict:
                current_flow = read_flow()[0]
                if abs(current_flow - param_dict['set n2 flow rate']) > param_dict['n2 flow rate tolerance']:
                    alert_message += '&bull;n2 flow rate deviated (current: %sL/min | set: %sL/min | tolerance: %sL/min)<br>' % (current_flow, param_dict['set n2 flow rate'], param_dict['n2 flow rate tolerance'])
                    n2_flow_rate_deviated = True
                else:
                    n2_flow_rate_deviated = False

            if 'set temperature' in param_dict:
                current_temperature = read_temperature()[0]
                if abs(current_temperature - param_dict['set temperature']) > param_dict['temperature tolerance']:
                    alert_message += '&bull;temperature deviated (current: %s°C | set: %s°C | tolerance: %s°C)' % (current_temperature, param_dict['set temperature'], param_dict['temperature tolerance'])
                    temperature_deviated = True
                else:
                    temperature_deviated = False

            if temperature_deviated or pressure_deviated or n2_flow_rate_deviated:
                if datetime.now() > dont_prompt_deviation_until:
                    show_deviation_prompt('Parameters deviated', '<span style="font-size:2rem">%s</span>' % alert_message)
                    trigger_alarm()
            else:
                close_prompt(['deviation prompt',])
            next_check_time = datetime.now() + timedelta(seconds=5)
    close_prompt(['deviation prompt',])
    return


def disable_prompt_deviation_until():
    global dont_prompt_deviation_until
    dont_prompt_deviation_until = datetime.now() + timedelta(minutes=1)
    close_prompt(['deviation prompt',])
    return
    

def logging_thread(process_name, logging_interval):
    last_log_time = datetime(2000,1,1)
    log_number = 0
    while process_run:
        if (datetime.now() - last_log_time).total_seconds() > logging_interval * 60:
            log_number += 1
            if process_name in ['production part 1', 'production part 2', 'production part 3', ]:
                production_read(log_number)
            elif process_name == 'post production':
                post_production_read(log_number)
            last_log_time = datetime.now()
        time.sleep(0.1)
    return


def get_variable(variable_name, process_name):
    row = database.query('local', 'get', 'SELECT value_set, `unit` FROM app_variabledefault WHERE name="%s" AND process="%s"' % (variable_name, process_name))[0]
    return (float(row[0]), row[1])


def determine_send_all(data):
    global recipient_ip
    message_type = data['message_type']

    # if message_type in ['trigger event', ]:
    #     return 'all'

    if message_type == 'prompt':
        message_text = data['message']['text']
        if message_text in ['Not authorised. Please log in.']:
            return recipient_ip
        
    elif message_type == 'prompt data check':
        return 'all'
        # return recipient_ip
        
    elif message_type == 'request input before process start':
        return 'all'
        # return recipient_ip
        
    elif message_type == 'prompt data check update':
        return 'all'
        # return recipient_ip
        
    elif message_type == 'confirm prompt':
        return recipient_ip
        
    # else:
    #     return recipient_ip
    return 'all'


def websocket_send(data):
    global ws
    recipient_ip = determine_send_all(data)
    time.sleep(0.2)
    data['recipient_ip'] = recipient_ip
    ws.send(json.dumps({
        'data': data,
        'sender': 'python',
    }))
    time.sleep(0.2)
    return


def update_database(message):
    for key in message:
        if key == 'start_process_name':
            process_name = message[key]
        else:
            variable_name = key.replace("_", ' ')
            variable_value = message[key] 
            database.query('local', 'update', 'UPDATE app_variabledefault SET value_set=%s WHERE name="%s" AND process="%s"' % (variable_value, variable_name, process_name))
    return


def show_prompt_data_check(text, wait_for_acknowledge, process_name='', parameters=[], button_text='Proceed'):
    title = '[INPUT TITLE HERE]'
    if process_name == 'pre production':
        global pre_production_start_logging
        parameters_list = []
        set_parameters_list = []
        for param in parameters:
            row = database.query('local', 'get', 'SELECT name, unit FROM app_variabledefault WHERE name="%s" AND process="%s"' % (param, process_name))[0]
            parameters_list.append({'name':row[0], 'unit':row[1]})
            row = database.query('local', 'get', 'SELECT name, value_set, `unit` FROM app_variabledefault WHERE process="%s" AND name="%s"' % (process_name, param))[0]
            set_parameters_list.append({'name':row[0], 'value':float(row[1]), 'unit':row[2]})
        data = {
            'message': {
                'title': text,
                'text': text,
                'parameters': parameters_list,
                'set_parameters': set_parameters_list,
                'wait_for_acknowledge': wait_for_acknowledge,
                'process_name': process_name,
                'button_text': button_text,
            },
            'message_type': 'prompt data check',
        }
        websocket_send(data)

        #update prompt
        flow_rate_tolerance = float(database.query('local', 'get', 'SELECT value_set FROM app_variabledefault WHERE process="%s" AND name="%s"' % (process_name, 'n2 flow rate tolerance'))[0][0])
        set_flow = float(database.query('local', 'get', 'SELECT value_set FROM app_variabledefault WHERE process="%s" AND name="%s"' % (process_name, 'n2 flow rate'))[0][0])
        current_flow = 0
        while (abs(current_flow - set_flow) > flow_rate_tolerance) and not pre_production_start_logging:
            current_flow = read_flow()[0]
            data = {
                'message': {
                    'n2 flow rate': current_flow,
                },
                'message_type': 'prompt data check update',
            }
            websocket_send(data)
            event.wait(5)
        if not pre_production_start_logging:
            close_prompt(['notification prompt',])
            show_prompt('Pre Production', 'Flow rate set point reached. Start logging.')
            pre_production_start_logging = True
            

    elif process_name == 'production part 1 logging':
        set_parameters_list = []
        rows = database.query('local', 'get', 'SELECT name, value_set, `unit` FROM app_variabledefault WHERE process="production part 1" AND name IN ("n2 flow rate")')
        for row in rows:
            set_parameters_list.append({'name':row[0], 'value':float(row[1]), 'unit':row[2]})

        rows = database.query('local', 'get', 'SELECT unit FROM app_sensorreading ORDER BY id ASC')
        data = {
            'message': {
                'text': text,
                'parameters': [
                    {'name': 'temperature', 'unit': rows[2][0]},
                    {'name': 'n2 flow rate', 'unit': rows[1][0]},
                    {'name': 'pressure', 'unit': rows[0][0]},
                ],
                'set_parameters': set_parameters_list,
                'wait_for_acknowledge': wait_for_acknowledge,
                'process_name': process_name,
                'button_text': button_text,
            },
            'message_type': 'prompt data check',
        }
        websocket_send(data)

        waiting = 'active'
        while waiting == 'active':
            waiting = database.query('local', 'get', 'SELECT status FROM app_processlist WHERE name="waiting to log" AND category="production_part_1"')[0][0]
            current_flow = read_flow()[0]
            current_temp = read_temperature()[0]
            current_pressure = read_pressure()[0]
            data = {
                'message': {
                    'n2 flow rate': current_flow,
                    'pressure': current_pressure,
                    'temperature': current_temp,
                },
                'message_type': 'prompt data check update',
            }
            websocket_send(data)
            event.wait(5)

    elif process_name == 'production part 2 logging':
        set_parameters_list = []
        rows = database.query('local', 'get', 'SELECT name, value_set, `unit` FROM app_variabledefault WHERE process="production part 2" AND name IN ("heater set point")')
        for row in rows:
            set_parameters_list.append({'name':row[0], 'value':float(row[1]), 'unit':row[2]})
        
        data = {
            'message': {
                'text': text,
                'parameters': [
                    {'name': 'temperature', 'unit': '°C'},
                    {'name': 'n2 flow rate', 'unit': 'L/min'},
                    {'name': 'pressure', 'unit': 'kPa'},
                ],
                'set_parameters': set_parameters_list,
                'wait_for_acknowledge': wait_for_acknowledge,
                'process_name': process_name,
                'button_text': button_text,
            },
            'message_type': 'prompt data check',
        }
        websocket_send(data)

        waiting = 'active'
        while waiting == 'active':
            waiting = database.query('local', 'get', 'SELECT status FROM app_processlist WHERE name="waiting to log" AND category="production_part_2"')[0][0]
            current_flow = read_flow()[0]
            current_temp = read_temperature()[0]
            current_pressure = read_pressure()[0]
            data = {
                'message': {
                    'n2 flow rate': current_flow,
                    'pressure': current_pressure,
                    'temperature': current_temp,
                },
                'message_type': 'prompt data check update',
            }
            websocket_send(data)
            event.wait(5)
            
    elif process_name == 'production part 3 logging':
        set_parameters_list = []
        rows = database.query('local', 'get', 'SELECT name, value_set, `unit` FROM app_variabledefault WHERE process="production part 3" AND name IN ("n2 flow rate")')
        for row in rows:
            set_parameters_list.append({'name':row[0], 'value':float(row[1]), 'unit':row[2]})
        
        data = {
            'message': {
                'text': text,
                'parameters': [
                    {'name': 'temperature', 'unit': '°C'},
                    {'name': 'n2 flow rate', 'unit': 'L/min'},
                    {'name': 'pressure', 'unit': 'kPa'},
                ],
                'set_parameters': set_parameters_list,
                'wait_for_acknowledge': wait_for_acknowledge,
                'process_name': process_name,
                'button_text': button_text,
            },
            'message_type': 'prompt data check',
        }
        websocket_send(data)

        waiting = 'active'
        while waiting == 'active':
            waiting = database.query('local', 'get', 'SELECT status FROM app_processlist WHERE name="waiting to log" AND category="production_part_3"')[0][0]
            current_flow = read_flow()[0]
            current_temp = read_temperature()[0]
            current_pressure = read_pressure()[0]
            data = {
                'message': {
                    'n2 flow rate': current_flow,
                    'pressure': current_pressure,
                    'temperature': current_temp,
                },
                'message_type': 'prompt data check update',
            }
            websocket_send(data)
            event.wait(5)

    elif process_name == 'production part 3 wait vacuum release':
        data = {
            'message': {
                'text': text,
                'parameters': [
                    {'name': 'pressure', 'unit': 'kPa'},
                ],
                'set_parameters': [],
                'wait_for_acknowledge': wait_for_acknowledge,
                'process_name': process_name,
                'button_text': button_text,
            },
            'message_type': 'prompt data check',
        }
        websocket_send(data)

        waiting = 'active'
        while waiting == 'active':
            waiting = database.query('local', 'get', 'SELECT status FROM app_processlist WHERE name="waiting to release vacuum" AND category="production_part_3"')[0][0]
            current_pressure = read_pressure()[0]
            data = {
                'message': {
                    'pressure': current_pressure,
                },
                'message_type': 'prompt data check update',
            }
            websocket_send(data)
            event.wait(5)
    return


def close_prompt(prompt=[]):
    if prompt == 'all':
        prompt = ['notification prompt', 'data input prompt', 'confirmation prompt', 'select process prompt', 'deviation prompt', 'select process modal']
    data = {
        'message': prompt,
        'message_type': 'close prompt',
    }
    websocket_send(data)
    return

def show_deviation_prompt(title, text):
    data = {
        'message': {
            'title': title,
            'text': text,
        },
        'message_type': 'deviation prompt',
    }
    websocket_send(data)
    return

def show_prompt(title, text, wait_for_acknowledge=False, process_name='', button_text='Proceed'):
    data = {
        'message': {
            'title': title,
            'text': text,
            'wait_for_acknowledge': wait_for_acknowledge,
            'process_name': process_name,
            'button_text': button_text,
        },
        'message_type': 'prompt',
    }
    websocket_send(data)
    return

def request_confirm(title, text, process_name=''):
    data = {
        'message': {
            'title': title,
            'text': text,
            'process_name': process_name,
        },
        'message_type': 'confirm prompt',
    }
    websocket_send(data)
    return


def process_list_manage(name, category):
    database.query('local', 'update', 'UPDATE app_processlist SET status="not active" WHERE name!="%s" OR category!="%s"' % (name, category))
    status = database.query('local', 'get', 'SELECT status FROM app_processlist WHERE name="%s" AND category="%s"' % (name, category))[0][0]
    if status == 'not active':
        database.query('local', 'update', 'UPDATE app_processlist SET status="active" WHERE name="%s" AND category="%s"' % (name, category))
    elif status == 'active':
        database.query('local', 'update', 'UPDATE app_processlist SET status="not active" WHERE name="%s" AND category="%s"' % (name, category))
    return


def get_batch_id():
    latest_batch_id = database.query('local', 'get', 'SELECT id FROM app_report ORDER BY id DESC LIMIT 1')
    if len(latest_batch_id) > 0:
        latest_batch_id = latest_batch_id[0][0]
    else:
        latest_batch_id = 0
    return int(latest_batch_id) + 1


def pre_production_read(log_number):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    batch_id = get_batch_id()
    flow, unit = read_flow()
    database.query('local', 'insert', 'INSERT INTO app_logdata (batch, type, flow, flow_unit, timestamp) VALUES ("%s", "%s", "%s", "%s", "%s")' % (batch_id, 'pre production', flow, unit, timestamp))
    if log_number == 'first':
        update_progress('pre production', 'Starting data point logged (%s%s).' % (flow, unit), 15.0)
        pass
    elif log_number == 'last':
        update_progress('pre production', 'End data point logged (%s%s).' % (flow, unit), 100.0)
        pass
    return

def production_read(log_number):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    batch_id = get_batch_id()
    flow, flow_unit = read_flow()
    pressure, pressure_unit = read_pressure()
    temperature, temperature_unit = read_temperature()
    current_process = database.query('local', 'get', 'SELECT category FROM app_processlist WHERE status="active" LIMIT 1')[0][0].replace('_', ' ')
    heater = database.query('local', 'get', 'SELECT value_set, unit FROM app_variabledefault WHERE name="heater set point" AND process="%s"' % (current_process))[0]
    heater_set = heater[0]
    heater_set_unit = heater[1]
    database.query('local', 'insert', 'INSERT INTO app_logdata (batch, type, flow, flow_unit, pressure, pressure_unit, temperature, temperature_unit, heater_set, heater_set_unit, timestamp) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (batch_id, current_process, flow, flow_unit, pressure, pressure_unit, temperature, temperature_unit, heater_set, heater_set_unit, timestamp))
    
    if log_number != 'last':
        update_progress(current_process, 'Logged data point #%s (flow: %s%s | pressure: %s%s | temperature: %s%s)' % (log_number, flow, flow_unit, pressure, pressure_unit, temperature, temperature_unit), None)
    else:
        update_progress(current_process, 'Logged last data point (flow: %s%s | pressure: %s%s | temperature: %s%s)' % (flow, flow_unit, pressure, pressure_unit, temperature, temperature_unit), 95)
    return

# track progress base on time
def progress_bar_update(start_percentage, end_percentage, process_duration):
    start_time = datetime.now()
    last_update = datetime(2000, 1, 1)
    while process_run:
        if (datetime.now() - last_update).total_seconds() > 10:
            time_elapsed_seconds = (datetime.now() - start_time).total_seconds()
            progress_made = time_elapsed_seconds / (process_duration*60)
            percentage = (end_percentage - start_percentage) * progress_made
            database.query('local', 'update', 'UPDATE app_progress SET percentage=%s' % (start_percentage + percentage))
            websocket_send(data = {
                'message':{
                    'process': '',
                    'description': '',
                    'percentage': start_percentage + percentage,
                    'timestamp': '',
                },
                'message_type': 'progress update'
            })
            last_update = datetime.now()
    return
# track progress base on temperature
def progress_bar_update_temp(start_percentage, end_percentage, target_temp):
    start_temp = read_temperature()[0]
    last_update = datetime(2000, 1, 1)
    while process_run:
        if (datetime.now() - last_update).total_seconds() > 10:
            if target_temp != start_temp:
                progress_made = read_temperature()[0] / (target_temp - start_temp)
            else:
                progress_made = 1
            percentage = (end_percentage - start_percentage) * progress_made
            websocket_send(data = {
                'message':{
                    'process': '',
                    'description': '',
                    'percentage': start_percentage + percentage,
                    'timestamp': '',
                },
                'message_type': 'progress update'
            })
            last_update = datetime.now()
    return

def post_production_read(log_number):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    batch_id = get_batch_id()
    flow, flow_unit = read_flow()
    pressure, pressure_unit = read_pressure()
    temperature, temperature_unit = read_temperature()
    current_process = database.query('local', 'get', 'SELECT category FROM app_processlist WHERE status="active" LIMIT 1')[0][0].replace('_', ' ')
    database.query('local', 'insert', 'INSERT INTO app_logdata (batch, type, flow, flow_unit, pressure, pressure_unit, temperature, temperature_unit, timestamp) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (batch_id, current_process, flow, flow_unit, pressure, pressure_unit, temperature, temperature_unit, timestamp))

    if log_number != 'last':
        update_progress(current_process, 'Logged data point #%s (temperature: %s%s)' % (log_number, temperature, temperature_unit), None)
    else:
        update_progress(current_process, 'Logged last data point (temperature: %s%s)' % (temperature, temperature_unit), 95)
    return

def read_temperature():
    row = database.query('local', 'get', 'SELECT value, `unit` FROM app_sensorreading WHERE name="temperature"')[0]
    value = float(row[0])
    unit = row[1]
    return value, unit


def read_flow():
    row = database.query('local', 'get', 'SELECT value, `unit` FROM app_sensorreading WHERE name="n2 flow rate"')[0]
    value = float(row[0])
    unit = row[1]
    return value, unit


def read_pressure():
    row = database.query('local', 'get', 'SELECT value, `unit` FROM app_sensorreading WHERE name="pressure"')[0]
    value = float(row[0])
    unit = row[1]
    return value, unit

def log_heater_set_point(value):
    unit = '°C'
    batch_id = get_batch_id()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    database.query('local', 'insert', 'INSERT INTO app_logdata (batch, type, value, unit, timestamp) VALUES ("%s", "%s", "%s", "%s", "%s")' % (batch_id, 'heater set point', value, unit, timestamp))
    return

def flow_control(set):
    database.query('local', 'update', 'UPDATE app_sensorreading SET set_point=%s, status="1" WHERE name="n2 flow rate"' % set)
    return


def trigger_event(event_name=''):
    data = {
        'message': {
            'event_name': event_name,
        },
        'message_type': 'trigger event',
    }
    websocket_send(data)
    return


def reaffirm_cancel_operation():
    request_confirm('', 'Confirm to cancel operation?', 'cancel operation')
    return
    
def reset_operation():
    global process_run
    report_generated = False
    latest_log = database.query('local', 'get', 'SELECT batch, type FROM app_logdata ORDER BY batch DESC LIMIT 1')
    if len(latest_log) > 0:
        latest_log_batch_id = latest_log[0][0]
        latest_log_type = latest_log[0][1]
        if latest_log_type == 'pre production':
            process_name = 'pre production'
        elif latest_log_type in ['production part 1', 'production part 2', 'production part 3']:
            process_name = 'production'
        elif latest_log_type in ['post production day 1', 'post production day 2', 'post production day 3']:
            process_name = 'post production'
    else:
        latest_log_batch_id = 0
    latest_report_batch_id = database.query('local', 'get', 'SELECT id FROM app_report ORDER BY id DESC LIMIT 1')
    if len(latest_report_batch_id) > 0:
        latest_report_batch_id = latest_report_batch_id[0][0]
    else:
        latest_report_batch_id = 0
    if latest_log_batch_id != latest_report_batch_id:
        generate_report(process_name)
        report_generated = True
    flow_control(0)
    close_prompt('all')
    trigger_alarm('off')
    database.query('local', 'update', 'UPDATE app_processlist SET status="not active"')
    process_run = False
    update_progress('', '', 0, True)
    time.sleep(0.5)
    trigger_event()
    if report_generated:
        show_prompt('', 'All process reset. Report is generated.')
    else:
        show_prompt('', 'All process reset')
    return

def show_prompt_data_input(title, text, parameter, process_name='', button_text='Proceed'):
    variables_list = []
    for param in parameter:
        par = database.query('local', 'get', 'SELECT name, value, unit FROM app_variabledefault WHERE process="%s" AND name="%s" ORDER BY name ASC' % (process_name, param))[0]
        variables_list.append({
            'name': par[0],
            'value': float(par[1]),
            'unit': par[2],
        })
    websocket_send(data = {
        'message': {
            'title': title,
            'text': text,
            'variables_list': variables_list,
            'process_name': process_name,
            'button_text': button_text,
        },
        'message_type': 'request input before process start',
        'recipient_ip': recipient_ip,
    })
    return


def update_progress(process, description, percentage, clear_progress=False):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_display = datetime.now().strftime('%I:%M:%S %p')

    if clear_progress:
        database.query('local' ,'update', 'DELETE FROM app_progress WHERE 1')

    if process != '':
        if percentage:
            database.query('local', 'insert', 'INSERT INTO app_progress (process, description, percentage, timestamp) VALUES ("%s", "%s", "%s", "%s")' % (process, description, percentage, timestamp))
        else:
            database.query('local', 'insert', 'INSERT INTO app_progress (process, description, percentage, timestamp) VALUES ("%s", "%s", NULL, "%s")' % (process, description, timestamp))
        
        websocket_send(data = {
            'message':{
                'process': process,
                'description': description,
                'percentage': percentage,
                'timestamp': timestamp_display,
            },
            'message_type': 'progress update'
        })
    return


# =============================================================================
# process functions
# =============================================================================

# pre production
class pre_production(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global pre_production_receive_input, pre_production_start_logging, process_run, deactivate_flow_pre_production
        process_run = True
        pre_production_receive_input = False
        pre_production_start_logging = False

        # start
        process_list_manage('data input', 'pre production')
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        show_prompt('Pre Production', 'Pre production has started')
        update_progress('pre production', 'Pre production has started', 10.0, True)
        time.sleep(3.1)

        # data input
        show_prompt_data_input('Pre production', 'Waiting to start purging process', ['n2 flow rate', 'purging duration'], 'pre production', 'Start purging')

        # wait submit data input
        while not pre_production_receive_input and process_run:
            event.wait(1)

        if not process_run:
            return
            
        process_list_manage('waiting to log', 'pre production')
        n2_flow = get_variable('n2 flow rate', 'pre production')[0]
        flow_control(n2_flow) # activate flow controller, wait for flow to reach set point or bypass by user
        threading.Thread(target=show_prompt_data_check, args=('Waiting to start logging', True, 'pre production', ['n2 flow rate',], 'Start Logging')).start()
        update_progress('pre production', 'Waiting to log.', 10.0)

        # start logging
        while not pre_production_start_logging:
            event.wait(0.1)

        pre_production_start_time = datetime.now()
        purging_duration = get_variable('purging duration', 'pre production')[0]
        process_list_manage('logging', 'pre production')
        update_progress('pre production', 'Logging started for %s minutes.' % purging_duration, 10.0)
        pre_production_read('first') # read flow at start of purging
        update_progress('pre production', 'Waiting for %s minutes to log end pressure.' % purging_duration, 15.0)
        threading.Thread(target=progress_bar_update, args=(15, 95, purging_duration)).start()
        while (datetime.now()-pre_production_start_time).total_seconds() < (purging_duration*60) and process_run:
            event.wait(0.1)
            
        if process_run:
            process_run = False
            pre_production_read('last') # read flow at end of purging
            process_list_manage('waiting to release vacuum', 'pre production')
            update_progress('pre production', 'Process duration reached.', 95.0)
            close_prompt('all')
            time.sleep(1)
            show_prompt('Pre Production', 'Purging duration reached. Waiting for deactivation of flow controller', True, 'pre production deactivate flow')
            time.sleep(1.5)
        else:
            return

        while not deactivate_flow_pre_production:
            event.wait(0.1)

        update_progress('pre production', 'Deactivating nitrogen flow controller.', 100)
        flow_control(0)
        process_list_manage('waiting to release vacuum', 'pre production')
        time.sleep(1.5)
        close_prompt('all')
        time.sleep(1)
        show_prompt('Pre Production', 'Pre production completed. Report generated.', True, 'end pre production')
        trigger_alarm()
        trigger_event()
        update_progress('', '', 0, True)
        generate_report('pre production')
        return



# production part 1
class production(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global process_run, production_1_receive_input, production_1_start_logging, change_heater_set_production_1, production_2_receive_input, production_2_start_logging, start_production_3, production_3_receive_input, production_3_start_logging, release_vacuum_production_3
        process_run = True
        production_1_receive_input = False
        production_1_start_logging = False
        change_heater_set_production_1 = False
        production_2_receive_input = False
        production_2_start_logging = False
        start_production_3 = False
        production_3_receive_input = False
        production_3_start_logging = False
        release_vacuum_production_3 = False

        # start
        process_list_manage('data input', 'production_part_1')
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        update_progress('production part 1', 'Production part 1 has started', 5.0, True)
        show_prompt('Production Part 1', 'Production part 1 has started')
        time.sleep(3.1)
        show_prompt_data_input('Production Part 1', '', ['n2 flow rate', 'target temperature', 'logging interval', 'heater set point'], 'production part 1', 'Start process part 1')

        # wait submit data input
        while not production_1_receive_input and process_run:
            event.wait(0.1)

        if not process_run:
            return
            
        process_list_manage('waiting to log', 'production_part_1')
        n2_flow = get_variable('n2 flow rate', 'production part 1')[0]
        flow_control(n2_flow) # activate flow controller, wait for manual input by user
        update_progress('production part 1', 'Waiting for user acknowledgement to start logging.', 5.0)
        time.sleep(1)
        threading.Thread(target=show_prompt_data_check, args=('Waiting to start logging', True, 'production part 1 logging', [], 'Start Logging')).start()

        # start logging
        while not production_1_start_logging:
            event.wait(0.1)
            
        part_1_start_time = datetime.now()
        process_list_manage('logging', 'production_part_1')
        logging_interval = get_variable('logging interval', 'production part 1')[0]
        target_temp = get_variable('target temperature', 'production part 1')[0]
        update_progress('production part 1', 'Logging started (log every %s min).' % logging_interval, 10.0)
        current_temp = 0
        _logging = threading.Thread(target=logging_thread, args=('production part 1', logging_interval))
        check_deviation_thread = threading.Thread(target=check_deviation, args=('production part 1',))
        _logging.start()
        check_deviation_thread.start()
        threading.Thread(target=progress_bar_update_temp, args=(10, 90, target_temp)).start()
        
        while (current_temp < target_temp) and process_run:
            current_temp = read_temperature()[0]
            event.wait(0.1)

        if process_run:
            process_run = False
            _logging.join()
            check_deviation_thread.join()
            update_progress('production part 1', 'Target temperature reached. Waiting for change of heater set point.', 90.0)
            show_prompt_data_input('Production Part 1', 'Target temperature reached. Waiting for change of heater set point.', ['heater set point',], 'production part 2', 'Heater set point changed')
            trigger_alarm()

            # wait change heater set point production part 1
            while not change_heater_set_production_1:
                event.wait(0.1)
                
            update_progress('production part 1', 'Heater set point changed', 95.0)
            production_read('last')
            process_list_manage('logging', 'production_part_1')
            time.sleep(1)
            trigger_alarm()
            update_progress('production part 1', 'Production part 1 completed.', 100)
            close_prompt('all')
            time.sleep(1)
            show_prompt('Production Part 1', 'Production part 1 completed.', True, 'start production part 2', 'Start process part 2')
        else:
            return

        # wait start production part 2
        process_run = True

        while not start_production_2:
            event.wait(0.1)
            
        process_list_manage('data input', 'production_part_2')
        update_progress('', '', 0, True)
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        update_progress('production part 2', 'Production part 2 started.', 5.0)
        show_prompt_data_input('Production Part 2', '',['logging interval', 'process duration', 'heater set point'], 'production part 2', 'start process part 2')

        # wait submit data input
        while not production_2_receive_input and process_run:
            event.wait(0.1)

        if not process_run:
            return

        process_list_manage('waiting to log', 'production_part_2')
        threading.Thread(target=show_prompt_data_check, args=('Waiting to start logging', True, 'production part 2 logging')).start()

        # start logging
        while not production_2_start_logging:
            event.wait(0.1)

        process_list_manage('logging', 'production_part_2')
        logging_interval = get_variable('logging interval', 'production part 2')[0]
        process_duration = get_variable('process duration', 'production part 2')[0]
        update_progress('production part 2', 'Logging started (log every %s min for %s min from start of process 1).' % (logging_interval, process_duration), 10.0)
        _logging = threading.Thread(target=logging_thread, args=('production part 2', logging_interval))
        check_deviation_thread = threading.Thread(target=check_deviation, args=('production part 2',))
        _logging.start()
        check_deviation_thread.start()
        threading.Thread(target=progress_bar_update, args=(10, 95, process_duration)).start()
        
        while ((datetime.now() - part_1_start_time).total_seconds() < process_duration * 60) and process_run:
            time.sleep(0.1)

        if process_run:
            process_run = False
            _logging.join()
            check_deviation_thread.join()
            production_read('last')
            process_list_manage('logging', 'production_part_2')
            update_progress('production part 2', 'Production part 2 completed.', 100)
            close_prompt('all')
            time.sleep(1)
            show_prompt('Production Part 2', 'Process part 2 completed.', True, 'start production part 3')
            trigger_alarm()
        else:
            return
        
        # wait to start production part 3
        process_run = True
        
        while not start_production_3:
            event.wait(0.1)

        process_list_manage('data input', 'production_part_3')
        update_progress('', '', 0, True)
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        update_progress('production part 3', 'Production part 3 started.', 5)
        show_prompt_data_input('Production Part 3', '', ['n2 flow rate', 'logging interval', 'process duration', 'heater set point'], 'production part 3', 'Start process part 3')
    
        # wait submit data input production part 3
        while not production_3_receive_input and process_run:
            event.wait(0.1)

        if not process_run:
            return

        process_list_manage('waiting to log', 'production_part_3')
        update_progress('production part 3', 'Waiting for user acknowledgement to start logging.', 5)
        flow_control(get_variable('n2 flow rate', 'production part 3')[0])
        threading.Thread(target=show_prompt_data_check, args=('Waiting to start logging', True, 'production part 3 logging', [], 'Start Logging')).start()

        # start logging production part 3
        while not production_3_start_logging:
            event.wait(0.1)

        part_3_start_time = datetime.now()
        process_list_manage('logging', 'production_part_3')
        logging_interval = get_variable('logging interval', 'production part 3')[0]
        process_duration = get_variable('process duration', 'production part 3')[0]
        update_progress('production part 3', 'Logging started (log every %smin for %smin).' % (logging_interval, process_duration), 10)
        _logging = threading.Thread(target=logging_thread, args=('production part 3', logging_interval))
        check_deviation_thread = threading.Thread(target=check_deviation, args=('production part 3',))
        _logging.start()
        check_deviation_thread.start()
        threading.Thread(target=progress_bar_update, args=(10, 95, process_duration)).start()
        
        while ((datetime.now() - part_3_start_time).total_seconds() < process_duration * 60) and process_run:
            time.sleep(0.1)

        if process_run:
            process_run = False
            check_deviation_thread.join()
            _logging.join()
            production_read('last')
            process_list_manage('waiting to release vacuum', 'production_part_3')
            update_progress('production part 3', 'Process part 3 completed. Waiting for release of vacuum.', 95)
            close_prompt('all')
            time.sleep(1)
            threading.Thread(target=show_prompt_data_check, args=('Process part 3 completed. Waiting for release of vacuum.', True, 'production part 3 wait vacuum release', ['pressure',], 'Vacuum Released. Deactivate  N2 flow')).start()
            trigger_alarm()
        else:
            return
            
        # end production
        while not release_vacuum_production_3:
            event.wait(0.1)

        update_progress('production part 3', 'Vacuum released. Deactivating nitrogen flow controller.', 100)
        flow_control(0)
        process_list_manage('waiting to release vacuum', 'production_part_3')
        time.sleep(1.5)
        trigger_alarm()
        close_prompt('all')
        time.sleep(1)
        show_prompt('Production', 'Production completed. Report generated.', True, 'end production')
        trigger_event()
        generate_report('production')
        update_progress('', '', 0, True)
            
        return



# post production

class post_production_1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global process_run, post_production_1_receive_input
        process_run = True
        post_production_1_receive_input = False

        # start
        process_list_manage('data input', 'post_production_day_1')
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        update_progress('post production day 1', 'Post production day 1 has started', 5.0)
        show_prompt('Post Production Day 1', 'Post Production Day 1 has started')
        time.sleep(3.1)
        # data input
        show_prompt_data_input('Post Production Day 1', '', ['process duration', 'logging interval'], 'post production day 1', 'Start day 1 cleaning')

        # wait submit data input
        while not post_production_1_receive_input and process_run:
            event.wait(0.1)

        if not process_run:
            return

        post_production_day_1_start_time = datetime.now()
        process_list_manage('logging', 'post_production_day_1')
        logging_interval = get_variable('logging interval', 'post production day 1')[0]
        process_duration = get_variable('process duration', 'post production day 1')[0]
        update_progress('post production day 1', 'Logging started (log every %s min for %s min).' % (logging_interval, process_duration), 10.0)
        _logging = threading.Thread(target=logging_thread, args=('post production', logging_interval))
        _logging.start()
        threading.Thread(target=progress_bar_update, args=(10, 95, process_duration)).start()

        while ((datetime.now() - post_production_day_1_start_time).total_seconds() < process_duration * 60) and process_run:
            time.sleep(0.1)

        if process_run:
            process_run = False
            _logging.join()
            post_production_read('last')
            update_progress('post production day 1', 'Process duration reached.', 100.0)
            process_list_manage('waiting to start day 2', 'post_production_wait_day_2')
            time.sleep(0.5)
            trigger_event()
            update_progress('', '', 0, True)
            close_prompt('all')
            time.sleep(1)
            show_prompt('Post Production Day 1', 'Day 1 cleaning completed', True, '')
            trigger_alarm()
        else:
            return
        
        return

    
class post_production_2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global process_run, post_production_2_receive_input
        process_run = True
        post_production_2_receive_input = False

        # start
        process_list_manage('data input', 'post_production_day_2')
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        update_progress('post production day 2', 'Post production day 2 has started', 5.0)
        show_prompt('Post Production Day 2', 'Post production day 2 started.')
        time.sleep(3.1)

        # data input
        show_prompt_data_input('Post Production Day 2', '', ['process duration', 'logging interval'], 'post production day 2', 'Start day 2 cleaning')

        # wait submit data input
        while not post_production_2_receive_input and process_run:
            event.wait(0.1)

        if not process_run:
            return

        post_production_day_2_start_time = datetime.now()
        process_list_manage('logging', 'post_production_day_2')
        logging_interval = get_variable('logging interval', 'post production day 2')[0]
        process_duration = get_variable('process duration', 'post production day 2')[0]
        update_progress('post production day 2', 'Logging started (log every %s min for %s min).' % (logging_interval, process_duration), 5.0)
        _logging = threading.Thread(target=logging_thread, args=('post production', logging_interval))
        _logging.start()
        threading.Thread(target=progress_bar_update, args=(10, 95, process_duration)).start()

        while ((datetime.now() - post_production_day_2_start_time).total_seconds() < process_duration * 60) and process_run:
            time.sleep(0.1)

        if process_run:
            process_run = False
            _logging.join()
            post_production_read('last')
            update_progress('post production day 2', 'Process duration reached.', 100.0)
            process_list_manage('waiting to start day 3', 'post_production_wait_day_3')
            time.sleep(0.5)
            trigger_event()
            update_progress('', '', 0, True)
            close_prompt('all')
            time.sleep(1)
            show_prompt('Post Production Day 2', 'Day 2 cleaning completed', True, '')
            trigger_alarm()
        else:
            return
        
        return



class post_production_3(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global process_run, post_production_3_receive_input
        process_run = True
        post_production_3_receive_input = False

        # start
        process_list_manage('data input', 'post_production_day_3')
        time.sleep(0.5)
        trigger_event()
        time.sleep(0.5)
        update_progress('post production day 3', 'Post production day 3 has started', 5.0)
        show_prompt('Post Production Day 3', 'Post production day 3 started.')
        time.sleep(3.1)
        # data input
        show_prompt_data_input('Post Production Day 3', '', ['process duration', 'logging interval'], 'post production day 3', 'Start day 3 drying')

        # wait submit data input
        while not post_production_3_receive_input and process_run:
            event.wait(0.1)

        if not process_run:
            return

        post_production_day_3_start_time = datetime.now()
        process_list_manage('logging', 'post_production_day_3')
        logging_interval = get_variable('logging interval', 'post production day 3')[0]
        process_duration = get_variable('process duration', 'post production day 3')[0]
        update_progress('post production day 3', 'Logging started (log every %s min for %s min).' % (logging_interval, process_duration), 5.0)
        _logging = threading.Thread(target=logging_thread, args=('post production', logging_interval))
        _logging.start()
        threading.Thread(target=progress_bar_update, args=(10, 95, process_duration)).start()

        while ((datetime.now() - post_production_day_3_start_time).total_seconds() < process_duration * 60) and process_run:
            time.sleep(0.1)

        if process_run:
            process_run = False
            _logging.join()
            post_production_read('last')
            update_progress('post production day 3', 'Process duration reached.', 100.0)
            process_list_manage('logging', 'post_production_day_3')
            time.sleep(0.5)
            trigger_event()
            update_progress('', '', 0, True)
            close_prompt('all')
            time.sleep(1)
            show_prompt('Post Production Day 3', 'Day 3 cleaning completed. Report generated.', True, 'end post production')
            trigger_alarm()
            generate_report('post production')
        else:
            return
        
        return
        
 
# =================================================================
# threads
# =================================================================

class sensor_reading_update(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global ws
        while 1:
            try:
                data = {
                    'message': {
                        'n2_flow_rate': '%s' % (read_flow()[0]),
                        'pressure': '%s' % (read_pressure()[0]),
                        'temperature': '%s' % (read_temperature()[0]),
                    },
                    'message_type': 'sensor reading update',
                }
                websocket_send(data)
            except Exception as e:
                log.error('sensor_reading_update FAILED. %s' % e)
            time.sleep(5)

class connection_thread(threading.Thread):
    def __init__(self, websocket):
        threading.Thread.__init__(self)
        self.websocket = websocket

    def run(self):
        global ws
        while 1:
            try:
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
        log.error('on_error. %s' % (error))

    def on_close(self, ws, close_status_code, close_msg):
        global websocket_connected
        websocket_connected = False

    def on_message(self, ws, data):
        decoded_data = json.loads(data)
        message_type = decoded_data['data']['message_type']
        
        if message_type != 'sessions':
            global recipient_ip, pre_production_receive_input, production_1_receive_input, production_1_start_logging, change_heater_set_production_1, start_production_2, production_2_receive_input, production_2_start_logging, start_production_3, production_3_receive_input, production_3_start_logging, release_vacuum_production_3, post_production_1_receive_input, post_production_2_receive_input, post_production_3_receive_input, deactivate_flow_pre_production
            recipient_ip = decoded_data['data']['sender_ip']
            user_role = decoded_data['data']['user_role']
            message = decoded_data['data']['message']

            if message_type == 'process select':
                if user_role in ['Engineer', 'Super Admin', 'Guest', 'Technician']:
                    close_prompt(['select process prompt'], )
                    if message == 'pre production':
                        pre_production().start()
                    elif message == 'production':
                        production().start()
                    elif message == 'post production':
                        post_production_1().start()
                    elif message == 'post production day 2':
                        post_production_2().start()
                    elif message == 'post production day 3':
                        post_production_3().start()
                else:
                    show_prompt('', 'Not authorised. Please log in.')

            elif message_type == 'prompt data input submit':
                close_prompt(['data input prompt'], )
                update_database(message)
                if message['start_process_name'] == 'pre production':
                    pre_production_receive_input = True
                elif message['start_process_name'] == 'production part 1':
                    production_1_receive_input = True
                elif message['start_process_name'] == 'production part 2':
                    if ('heater_set_point' in message) and ('logging_interval' in message) and ('process_duration' in message):
                        production_2_receive_input = True
                    elif 'heater_set_point' in message:
                        trigger_alarm('off')
                        change_heater_set_production_1 = True
                elif message['start_process_name'] == 'production part 3':
                    production_3_receive_input = True
                elif message['start_process_name'] == 'post production day 1':
                    post_production_1_receive_input = True
                elif message['start_process_name'] == 'post production day 2':
                    post_production_2_receive_input = True
                elif message['start_process_name'] == 'post production day 3':
                    post_production_3_receive_input = True

            elif message_type == 'waiting prompt acknowledged':
                trigger_alarm('off')
                close_prompt(['notification prompt',])
                if message['process_name'] == 'pre production':
                    global pre_production_start_logging
                    pre_production_start_logging = True
                elif message['process_name'] == 'pre production deactivate flow':
                    deactivate_flow_pre_production = True
                elif message['process_name'] == 'production part 1 logging':
                    production_1_start_logging = True
                elif message['process_name'] == 'start production part 2':
                    start_production_2 = True
                elif message['process_name'] == 'production part 2 logging':
                    production_2_start_logging = True
                elif message['process_name'] == 'start production part 3':
                    start_production_3 = True
                elif message['process_name'] == 'production part 3 logging':
                    production_3_start_logging = True
                elif message['process_name'] == 'production part 3 wait vacuum release':
                    release_vacuum_production_3 = True
                elif message['process_name'] == 'end post production':
                    pass

            elif message_type == 'cancel operation':
                reaffirm_cancel_operation()

            elif message_type == 'confirm':
                if user_role in ['Engineer', 'Super Admin', 'Guest', 'Technician']:
                    if message['process_name'] == 'cancel operation':
                        reset_operation()
                else:
                    show_prompt('', 'Not authorised. Please log in.')

            elif message_type == 'request export':
                if user_role in ['Engineer', 'Super Admin', 'Guest', 'Technician']:
                    if len(message) > 0:
                        result = report.export_usb(log, message)
                        report_export_response(result)
                else:
                    show_prompt('', 'Not authorised. Please log in.')

            elif message_type == 'deviation':
                trigger_alarm('off')
                disable_prompt_deviation_until()
            
            elif message_type == 'edit report':
                update_report(message)
            
            elif message_type == 'delete report':
                delete_report(message)
            
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
    sensor_reading_update().start()
    