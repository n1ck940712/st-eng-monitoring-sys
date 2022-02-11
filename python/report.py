from modules import database, logger
from fpdf import Template
from pathlib import Path
import os, subprocess

# return definition
# 0: ok
# 1: error
# 2: no usb drive found

def export_usb(log, files=[]):
    try:
        os.putenv('FOO', ' '.join(files))
        result = subprocess.Popen("bash /home/pi/monitoring_sys/python/export_usb.sh", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        if result == '0':
            log.info('%s report(s) exported' % len(files))
            return 0    
        elif result == '1':
            log.error('no USB driver found')
            return 2
        else:
            return 1
    except Exception as e:
        log.error('Export USB ERROR. %s' % e)
        return 1
        
# variable received from report edit modal fields
def fill_in_fields(f, variable_list):
    for variable in variable_list:
        if variable['value'] != '': 
            f[variable['variable']] = str(variable['value'])
    return

def generate(log, batch_id, variable_list=None):
    report = database.query('local', 'get', 'SELECT type, time_completed FROM app_report WHERE id="%s"' % batch_id)
    if len(report) > 0: 
        process_name = report[0][0]
        process_date = report[0][1]
        process_date_input = process_date.strftime("%-d %b %Y")
        
        if process_name == 'pre production': 
            row = database.query('local', 'get', 'SELECT flow, timestamp FROM app_logdata WHERE batch="%s" ORDER BY timestamp DESC' % batch_id)
            if len(row) == 2:
                valid_data = True
                start_purge_time = row[1][1].strftime("%H:%M:%S")
                start_n2_flow_rate = row[1][0]
                end_purge_time = row[0][1].strftime("%H:%M:%S")
                end_n2_flow_rate = row[0][0]
                
                f = Template(format="A4", elements=get_pre_production_format(), title="Report")
                f.add_page()
                page_number = 1
                f['process-start-date'] = str(process_date_input)
                f['start-purge-time'] = str(start_purge_time)
                f['end-purge-time'] = str(end_purge_time)
                f['start-n2-flow-rate'] = str(start_n2_flow_rate)
                f['end-n2-flow-rate'] = str(end_n2_flow_rate)
                f['page-number'] = page_number

                if variable_list != None:
                    fill_in_fields(f, variable_list)
                
                report_name = "pre_production_%s" % (process_date.strftime("%-d%b%Y"))
            else:
                log.error('invalid log data')
                valid_data = False

        elif process_name == 'production': 
            rows = database.query('local', 'get', 'SELECT type, flow, flow_unit, temperature, temperature_unit, heater_set, heater_set_unit, pressure, pressure_unit, timestamp FROM app_logdata WHERE batch="%s" ORDER BY timestamp ASC' % batch_id)
            if len(rows) > 0:
                valid_data = True
                elements=get_production_format()
                f = Template(format="A4", elements=elements, title="Report")
                f.add_page()
                page_number = 2
                f['process-start-date'] = str(process_date_input)
                f['page-number'] = page_number
                if variable_list != None:
                    fill_in_fields(f, variable_list)

                table_row_num = 0
                table_row_x = 70.5
                for row in rows:
                    table_row_num += 1
                    table_row_x += 9
                    process_type = row[0].replace('production ', '')

                    if process_type == 'part 1':
                        process_type = '1'
                    elif process_type == 'part 2':
                        process_type = '1'
                    elif process_type == 'part 3':
                        process_type = '2'
                    
                    flow = row[1]
                    flow_unit = row[2]
                    temperature = row[3]
                    temperature_unit = row[4]
                    heater_set = row[5]
                    heater_set_unit = row[6]
                    pressure = row[7]
                    pressure_unit = row[8]
                    timestamp = row[9].strftime("%H:%M:%S")
                    if table_row_num > 19:
                        f.add_page()
                        page_number += 1
                        f['page-number'] = page_number
                        f['process-start-date'] = str(process_date_input)
                        if variable_list != None:
                            fill_in_fields(f, variable_list)
                        table_row_num = 0
                        table_row_x = 70.5
                    f['section-5-table-data-row-%s-type' % table_row_num] = process_type
                    f['section-5-table-data-row-%s-timestamp' % table_row_num] = str(timestamp)
                    f['section-5-table-data-row-%s-pressure' % table_row_num] = '%s %s' % (pressure, pressure_unit)
                    f['section-5-table-data-row-%s-temperature' % table_row_num] = '%s %s' % (temperature, temperature_unit)
                    f['section-5-table-data-row-%s-heater' % table_row_num] = '%s %s' % (heater_set, heater_set_unit)
                    f['section-5-table-data-row-%s-flow' % table_row_num] = '%s %s' % (flow, flow_unit)
                report_name = "production_%s" % (process_date.strftime("%-d%b%Y"))
            else:
                valid_data = False
                log.error('invalid log data')

        elif process_name == 'post production': 
            day_1_start_datetime = database.query('local', 'get', 'SELECT timestamp FROM app_logdata WHERE batch="%s" AND type="post production day 1" ORDER BY timestamp ASC LIMIT 1' % batch_id)[0][0]
            day_1_end_datetime = database.query('local', 'get', 'SELECT timestamp FROM app_logdata WHERE batch="%s" AND type="post production day 1" ORDER BY timestamp DESC LIMIT 1' % batch_id)[0][0]
            day_2_start_datetime = database.query('local', 'get', 'SELECT timestamp FROM app_logdata WHERE batch="%s" AND type="post production day 2" ORDER BY timestamp ASC LIMIT 1' % batch_id)[0][0]
            day_2_end_datetime = database.query('local', 'get', 'SELECT timestamp FROM app_logdata WHERE batch="%s" AND type="post production day 2" ORDER BY timestamp DESC LIMIT 1' % batch_id)[0][0]
            day_3_start_datetime = database.query('local', 'get', 'SELECT timestamp FROM app_logdata WHERE batch="%s" AND type="post production day 3" ORDER BY timestamp ASC LIMIT 1' % batch_id)[0][0]
            day_3_end_datetime = database.query('local', 'get', 'SELECT timestamp FROM app_logdata WHERE batch="%s" AND type="post production day 3" ORDER BY timestamp DESC LIMIT 1' % batch_id)[0][0]
            rows = database.query('local', 'get', 'SELECT type, temperature, temperature_unit, heater_set, heater_set_unit, timestamp FROM app_logdata WHERE batch="%s" ORDER BY timestamp ASC' % batch_id)
            if len(rows) > 0:
                valid_data = True
                elements=get_post_production_format()
                f = Template(format="A4", elements=elements, title="Report")
                f.add_page()
                page_number = 1
                f['process-start-date'] = str(process_date_input)
                f['page-number'] = page_number
                f['section-1-date-input'] = day_1_start_datetime.strftime('%-d %b %Y')
                f['section-1-start-time-input'] = day_1_start_datetime.strftime("%H:%M:%S")
                f['section-1-end-time-input'] = day_1_end_datetime.strftime("%H:%M:%S")
                
                f['section-2-date-input'] = day_2_start_datetime.strftime('%-d %b %Y')
                f['section-2-start-time-input'] = day_2_start_datetime.strftime("%H:%M:%S")
                f['section-2-end-time-input'] = day_2_end_datetime.strftime("%H:%M:%S")

                f['section-3-date-input'] = day_3_start_datetime.strftime('%-d %b %Y')
                f['section-3-start-time-input'] = day_3_start_datetime.strftime("%H:%M:%S")
                f['section-3-end-time-input'] = day_3_end_datetime.strftime("%H:%M:%S")

                if variable_list != None:
                    fill_in_fields(f, variable_list)

                table_row_num = 0
                process_day = 1
                first_row = True
                for row in rows:
                    table_row_num += 1
                    if process_day <= 3 and table_row_num <= 10:
                        process_type = row[0]
                        temperature = row[1]
                        temperature_unit = row[2]
                        heater_set = row[3]
                        heater_set_unit = row[4]
                        timestamp = row[5].strftime("%H:%M:%S")
                        if first_row:
                            process_type_name = process_type
                            first_row = False
                        
                        if process_type_name != process_type:
                            process_type_name = process_type
                            table_row_num = 1
                            process_day += 1

                        f['day-%s-table-row-%s-col-1-input' % (process_day, table_row_num)] = timestamp
                        f['day-%s-table-row-%s-col-2-input' % (process_day, table_row_num)] = '%s %s' % (temperature, temperature_unit)
                report_name = "post_production_%s" % (process_date.strftime("%-d%b%Y"))
            else:
                valid_data = False
                log.error('invalid log data')

        # check for valid data before generating pdf
        if valid_data:
            if variable_list:
                report_name_query = database.query('local', 'get', 'SELECT file_name FROM app_report WHERE id=%s' % batch_id)
                if len(report_name_query) > 0:
                    report_name = report_name_query[0][0]
                    file_path = "/home/pi/monitoring_sys/core/static/assets/reports/%s.pdf" % report_name
                    subprocess.run(['sudo', 'rm', file_path])
                    f.render(file_path)
                    log.info('Report edited: %s' % report_name)
            else:
                file_path = Path("/home/pi/monitoring_sys/core/static/assets/reports/%s.pdf" % report_name)
                while file_path.is_file():
                    log.debug('Report file name exist')
                    report_name += '(1)'
                    file_path = Path("/home/pi/monitoring_sys/core/static/assets/reports/%s.pdf" % report_name)
                    
                f.render(file_path)
                log.info('Report generated: %s' % report_name)
                database.query('local', 'update', 'UPDATE app_report SET file_name="%s" WHERE id=%s' % (report_name, batch_id))
            return 0
    else:
        log.error('Trying to generate report but no report data found.')
    return 1


def get_pre_production_format():
    elements = [
        { 'name': 'form-number', 'type': 'T', 'x1': 145, 'y1': 5, 'x2': 202.0, 'y2': 8.0, 'font': 'Arial', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'FORM 382-130001-Z-PROC-02 REV 01', 'priority': 2},
        
        { 'name': 'page-border', 'type': 'B', 'x1': 8.0, 'y1': 8.0, 'x2': 202, 'y2': 289.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-border', 'type': 'B', 'x1': 10.0, 'y1': 147.5, 'x2': 127, 'y2': 184.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line-1', 'type': 'L', 'x1': 10.0, 'y1': 156.5, 'x2': 127, 'y2': 156.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line-2', 'type': 'L', 'x1': 10.0, 'y1': 165.5, 'x2': 127, 'y2': 165.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line-3', 'type': 'L', 'x1': 10.0, 'y1': 174.5, 'x2': 127, 'y2': 174.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line-4', 'type': 'L', 'x1': 80.0, 'y1': 147.5, 'x2': 80, 'y2': 184.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'line-1', 'type': 'L', 'x1': 8.0, 'y1': 42.5, 'x2': 202.0, 'y2': 42.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'line-2', 'type': 'L', 'x1': 8.0, 'y1': 81.5, 'x2': 202.0, 'y2': 81.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'line-3', 'type': 'L', 'x1': 8.0, 'y1': 113.5, 'x2': 202.0, 'y2': 113.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'line-4', 'type': 'L', 'x1': 8.0, 'y1': 130.5, 'x2': 202.0, 'y2': 130.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },

        { 'name': 'page-title', 'type': 'T', 'x1': 84, 'y1': 13.0, 'x2': 115.0, 'y2': 13.0, 'font': 'Arial', 'size': 10.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'PRODUCTION FORM', 'priority': 2, },
        { 'name': 'section-1-row-1', 'type': 'T', 'x1': 13, 'y1': 20.0, 'x2': 115.0, 'y2': 20.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Material: HTPB', 'priority': 2, },
        { 'name': 'section-1-row-2', 'type': 'T', 'x1': 13, 'y1': 27.5, 'x2': 115.0, 'y2': 27.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Lot number/Drum number:', 'priority': 2, },
        { 'name': 'section-1-row-2-input-underline', 'type': 'T', 'x1': 51, 'y1': 27.5, 'x2': 115.0, 'y2': 27.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'lot or drum number', 'type': 'T', 'x1': 53, 'y1': 27.5, 'x2': 115.0, 'y2': 27.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'section-1-row-3', 'type': 'T', 'x1': 13, 'y1': 35.0, 'x2': 115.0, 'y2': 35.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Date:', 'priority': 2, },
        { 'name': 'section-1-row-3-input-underline', 'type': 'T', 'x1': 21, 'y1': 35.3, 'x2': 115.0, 'y2': 35.3, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'process-start-date', 'type': 'T', 'x1': 23, 'y1': 35.0, 'x2': 115.0, 'y2': 35.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },

        { 'name': 'section-2-header', 'type': 'T', 'x1': 13, 'y1': 46.5, 'x2': 115.0, 'y2': 46.5, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Nitrogen gas supply', 'priority': 2, },
        { 'name': 'section-2-row-1-col-1', 'type': 'T', 'x1': 13, 'y1': 54.0, 'x2': 115.0, 'y2': 54.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Pre-operation check', 'priority': 2, },
        { 'name': 'section-2-row-2-col-1', 'type': 'T', 'x1': 13, 'y1': 61.5, 'x2': 115.0, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Pressure of nitrogen pallet in use:', 'priority': 2, },
        { 'name': 'section-2-row-2-col-1-input', 'type': 'T', 'x1': 61, 'y1': 61.5, 'x2': 115.0, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'pre operation n2 pallet pressure', 'type': 'T', 'x1': 63, 'y1': 61.5, 'x2': 115.0, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'section-2-row-2-col-1-unit', 'type': 'T', 'x1': 78, 'y1': 61.5, 'x2': 115.0, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'bar', 'priority': 2, },
        { 'name': 'section-2-row-3-col-1', 'type': 'T', 'x1': 13, 'y1': 69.0, 'x2': 115.0, 'y2': 69.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'If less than 120 bar,', 'priority': 2, },
        { 'name': 'section-2-row-4-col-1', 'type': 'T', 'x1': 13, 'y1': 76.5, 'x2': 115.0, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Pressure of second nitrogen pallet:', 'priority': 2, },
        { 'name': 'section-2-row-4-col-1-input', 'type': 'T', 'x1': 63, 'y1': 76.5, 'x2': 62, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'pre operation 2nd n2 pallet pressure', 'type': 'T', 'x1': 65, 'y1': 76.5, 'x2': 62, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'section-2-row-4-col-1-unit', 'type': 'T', 'x1': 80, 'y1': 76.5, 'x2': 77, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'bar', 'priority': 2, },
        { 'name': 'section-2-row-1-col-2', 'type': 'T', 'x1': 108, 'y1': 54.0, 'x2': 115.0, 'y2': 54.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'After operation check', 'priority': 2, },
        { 'name': 'section-2-row-2-col-2', 'type': 'T', 'x1': 108, 'y1': 61.5, 'x2': 115.0, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Pressure of nitrogen pallet in use:', 'priority': 2, },
        { 'name': 'section-2-row-2-col-2-input', 'type': 'T', 'x1': 156, 'y1': 61.5, 'x2': 156, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'after operation n2 pallet pressure', 'type': 'T', 'x1': 158, 'y1': 61.5, 'x2': 156, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'section-2-row-2-col-2-unit', 'type': 'T', 'x1': 173, 'y1': 61.5, 'x2': 171, 'y2': 61.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'bar', 'priority': 2, },
        { 'name': 'section-2-row-4-col-2', 'type': 'T', 'x1': 108, 'y1': 76.5, 'x2': 115.0, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Pressure of second nitrogen pallet:', 'priority': 2, },
        { 'name': 'section-2-row-4-col-2-input', 'type': 'T', 'x1': 158, 'y1': 76.5, 'x2': 158, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'after operation 2nd n2 pallet pressure', 'type': 'T', 'x1': 160, 'y1': 76.5, 'x2': 158, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                  ', 'priority': 2, },
        { 'name': 'section-2-row-4-col-2-unit', 'type': 'T', 'x1': 175, 'y1': 76.5, 'x2': 1173, 'y2': 76.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'bar', 'priority': 2, },

        { 'name': 'section-3-header', 'type': 'T', 'x1': 13, 'y1': 85.5, 'x2': 115.0, 'y2': 85.5, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Transferring HTPB to vessel - Purging of Nitrogen for 5 minutes', 'priority': 2, },
        { 'name': 'section-3-row-1-col-1', 'type': 'T', 'x1': 13, 'y1': 93.0, 'x2': 115.0, 'y2': 93.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Start', 'priority': 2, },
        { 'name': 'section-3-row-2-col-1', 'type': 'T', 'x1': 13, 'y1': 100.5, 'x2': 115.0, 'y2': 100.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time: ', 'priority': 2, },
        { 'name': 'section-3-row-2-col-1-input', 'type': 'T', 'x1': 22, 'y1': 100.5, 'x2': 115.0, 'y2': 100.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'start-purge-time', 'type': 'T', 'x1': 27, 'y1': 100.1, 'x2': 115.0, 'y2': 100.1, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'section-3-row-3-col-1', 'type': 'T', 'x1': 13, 'y1': 108.0, 'x2': 115.0, 'y2': 108.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Nitrogen flow rate:', 'priority': 2, },
        { 'name': 'section-3-row-3-col-1-input', 'type': 'T', 'x1': 39, 'y1': 108.0, 'x2': 115.0, 'y2': 108.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                      ', 'priority': 2, },
        { 'name': 'start-n2-flow-rate', 'type': 'T', 'x1': 44, 'y1': 107.6, 'x2': 115.0, 'y2': 107.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                      ', 'priority': 2, },
        { 'name': 'section-3-row-3-col-1-unit', 'type': 'T', 'x1': 60, 'y1': 108.0, 'x2': 115.0, 'y2': 108.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'L/min', 'priority': 2, },
        { 'name': 'section-3-row-1-col-2', 'type': 'T', 'x1': 108, 'y1': 93.0, 'x2': 115.0, 'y2': 93.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'End', 'priority': 2, },
        { 'name': 'section-3-row-2-col-2', 'type': 'T', 'x1': 108, 'y1': 100.5, 'x2': 115.0, 'y2': 100.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time:', 'priority': 2, },
        { 'name': 'section-3-row-2-col-2-input', 'type': 'T', 'x1': 117, 'y1': 100.5, 'x2': 115.0, 'y2': 100.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'end-purge-time', 'type': 'T', 'x1': 122, 'y1': 100.1, 'x2': 115.0, 'y2': 100.1, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'section-3-row-3-col-2', 'type': 'T', 'x1': 108, 'y1': 108.0, 'x2': 115.0, 'y2': 108.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Nitrogen flow rate:', 'priority': 2, },
        { 'name': 'section-3-row-3-col-2-input', 'type': 'T', 'x1': 134, 'y1': 108.0, 'x2': 115.0, 'y2': 108.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                      ', 'priority': 2, },
        { 'name': 'end-n2-flow-rate', 'type': 'T', 'x1': 139, 'y1': 107.6, 'x2': 115.0, 'y2': 107.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                      ', 'priority': 2, },
        { 'name': 'section-3-row-3-col-2-unit', 'type': 'T', 'x1': 155, 'y1': 108.0, 'x2': 115.0, 'y2': 108.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'L/min', 'priority': 2, },

        { 'name': 'section-4-header', 'type': 'T', 'x1': 13, 'y1': 117.5, 'x2': 115.0, 'y2': 117.5, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vacuum Pump', 'priority': 2, },
        { 'name': 'section-4-row-1', 'type': 'T', 'x1': 13, 'y1': 125.0, 'x2': 115.0, 'y2': 125.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vacuum pump used: Vacuum pump', 'priority': 2, },
        { 'name': 'section-4-row-1', 'type': 'T', 'x1': 64, 'y1': 125.0, 'x2': 115.0, 'y2': 125.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'vacuum pump', 'type': 'T', 'x1': 66, 'y1': 125.0, 'x2': 115.0, 'y2': 125.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },

        { 'name': 'section-5-header', 'type': 'T', 'x1': 13, 'y1': 134.5, 'x2': 115.0, 'y2': 134.5, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Weight of HTPB, Treated', 'priority': 2, },
        { 'name': 'section-5-row-1', 'type': 'T', 'x1': 13, 'y1': 142.0, 'x2': 115.0, 'y2': 142.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Weighing Balance S/No:', 'priority': 2, },
        { 'name': 'section-5-row-1-input', 'type': 'T', 'x1': 48, 'y1': 142.0, 'x2': 115.0, 'y2': 142.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'weighing balance serial no', 'type': 'T', 'x1': 50, 'y1': 142.0, 'x2': 115.0, 'y2': 142.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },

        { 'name': 'section-5-table-row-1-header', 'type': 'T', 'x1': 97, 'y1': 151.0, 'x2': 150.0, 'y2': 151.0, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Weight (kg)', 'priority': 2, },
        { 'name': 'section-5-table-row-2-col-1', 'type': 'T', 'x1': 13, 'y1': 160.0, 'x2': 115.0, 'y2': 160.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Empty 220-L drum', 'priority': 2, },
        { 'name': 'empty 220L drum', 'type': 'T', 'x1': 87, 'y1': 160.0, 'x2': 115.0, 'y2': 160.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
        { 'name': 'section-5-table-row-3-col-1', 'type': 'T', 'x1': 13, 'y1': 169.0, 'x2': 115.0, 'y2': 169.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Filled 220-L drum with HTPB, Treated', 'priority': 2, },
        { 'name': 'filled 220L drum with HTPB, Treated', 'type': 'T', 'x1': 87, 'y1': 169.0, 'x2': 115.0, 'y2': 169.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
        { 'name': 'section-5-table-row-4-col-1', 'type': 'T', 'x1': 13, 'y1': 178.0, 'x2': 115.0, 'y2': 178.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Amount of HTPB, Treated collected', 'priority': 2, },
        { 'name': 'amount of HTPB, Treated collected', 'type': 'T', 'x1': 87, 'y1': 178.0, 'x2': 115.0, 'y2': 178.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },

        { 'name': 'done-by', 'type': 'T', 'x1': 13, 'y1': 215.0, 'x2': 115.0, 'y2': 215.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Done by:', 'priority': 2, },
        { 'name': 'checked-by', 'type': 'T', 'x1': 13, 'y1': 240.0, 'x2': 115.0, 'y2': 240.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Checked by:', 'priority': 2, },
        { 'name': 'page-number', 'type': 'T', 'x1': 194, 'y1': 281.0, 'x2': 194.0, 'y2': 281.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },

    ]
    return elements

def get_production_format():
    elements = [
        { 'name': 'form-number', 'type': 'T', 'x1': 145, 'y1': 5, 'x2': 202.0, 'y2': 8.0, 'font': 'Arial', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'FORM 382-130001-Z-PROC-02 REV 01', 'priority': 2},
        
        { 'name': 'page-border', 'type': 'B', 'x1': 8.0, 'y1': 8.0, 'x2': 202, 'y2': 289.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'line-1', 'type': 'L', 'x1': 8.0, 'y1': 42.5, 'x2': 202.0, 'y2': 42.5, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'table-border', 'type': 'B', 'x1': 10.0, 'y1': 52.0, 'x2': 200, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 75.0, 'x2': 200, 'y2': 75.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 84.0, 'x2': 200, 'y2': 84.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 93.0, 'x2': 200, 'y2': 93.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 102.0, 'x2': 200, 'y2': 102.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 111.0, 'x2': 200, 'y2': 111.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 120.0, 'x2': 200, 'y2': 120.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 129.0, 'x2': 200, 'y2': 129.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 138.0, 'x2': 200, 'y2': 138.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 147.0, 'x2': 200, 'y2': 147.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 156.0, 'x2': 200, 'y2': 156.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 165.0, 'x2': 200, 'y2': 165.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 174.0, 'x2': 200, 'y2': 174.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 183.0, 'x2': 200, 'y2': 183.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 192.0, 'x2': 200, 'y2': 192.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 201.0, 'x2': 200, 'y2': 201.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 210.0, 'x2': 200, 'y2': 210.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 219.0, 'x2': 200, 'y2': 219.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 228.0, 'x2': 200, 'y2': 228.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 10.0, 'y1': 237.0, 'x2': 200, 'y2': 237.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 23.0, 'y1': 52.0, 'x2': 23, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 42.0, 'y1': 52.0, 'x2': 42, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 75.0, 'y1': 52.0, 'x2': 75, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 108.0, 'y1': 52.0, 'x2': 108, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 141.0, 'y1': 52.0, 'x2': 141, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'table-line', 'type': 'L', 'x1': 174.0, 'y1': 52.0, 'x2': 174, 'y2': 246.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },

        { 'name': 'page-title', 'type': 'T', 'x1': 84, 'y1': 13.0, 'x2': 115.0, 'y2': 13.0, 'font': 'Arial', 'size': 10.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'PRODUCTION FORM', 'priority': 2, },
        { 'name': 'section-1-row-1', 'type': 'T', 'x1': 13, 'y1': 20.0, 'x2': 115.0, 'y2': 20.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Material: HTPB', 'priority': 2, },
        { 'name': 'section-1-row-2', 'type': 'T', 'x1': 13, 'y1': 27.5, 'x2': 115.0, 'y2': 27.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Lot number/Drum number:', 'priority': 2, },
        { 'name': 'section-1-row-2-input', 'type': 'T', 'x1': 51, 'y1': 27.5, 'x2': 115.0, 'y2': 27.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'lot or drum number', 'type': 'T', 'x1': 53, 'y1': 27.5, 'x2': 115.0, 'y2': 27.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
        { 'name': 'section-1-row-3', 'type': 'T', 'x1': 13, 'y1': 35.0, 'x2': 115.0, 'y2': 35.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Date:', 'priority': 2, },
        { 'name': 'section-1-row-3-input', 'type': 'T', 'x1': 21, 'y1': 35.3, 'x2': 115.0, 'y2': 35.3, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        { 'name': 'process-start-date', 'type': 'T', 'x1': 23, 'y1': 35.0, 'x2': 115.0, 'y2': 35.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '                                    ', 'priority': 2, },
        
        { 'name': 'section-2-header', 'type': 'T', 'x1': 13, 'y1': 46.5, 'x2': 115.0, 'y2': 46.5, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Purification Process', 'priority': 2, },
        
        { 'name': 'section-2-table-row-1-col-1', 'type': 'T', 'x1': 12, 'y1': 55, 'x2': 12, 'y2': 55, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Stage', 'priority': 2, },
        { 'name': 'section-2-table-row-1-col-2', 'type': 'T', 'x1': 29, 'y1': 55, 'x2': 29, 'y2': 55, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2, },
        { 'name': 'section-2-table-row-1-col-3', 'type': 'T', 'x1': 46, 'y1': 53, 'x2': 73, 'y2': 58, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vacuum Pressure (mbar) (S/No: _____________)', 'priority': 2, 'multiline': True},
        { 'name': 'vacuum pressure serial no', 'type': 'T', 'x1': 47, 'y1': 82, 'x2': 73, 'y2': 58, 'font': 'Arial', 'size': 8, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2},
        { 'name': 'section-2-table-row-1-col-4', 'type': 'T', 'x1': 79, 'y1': 53, 'x2': 107, 'y2': 58, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)                               (S/No: _____________)', 'priority': 2, 'multiline': True},
        { 'name': 'vessel temp serial no', 'type': 'T', 'x1': 80, 'y1': 82, 'x2': 107, 'y2': 58, 'font': 'Arial', 'size': 8, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2},
        { 'name': 'section-2-table-row-1-col-5', 'type': 'T', 'x1': 111, 'y1': 53, 'x2': 143.5, 'y2': 58, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Heater Set (°C)                                    (S/No: _____________)', 'priority': 2, 'multiline': True},
        { 'name': 'heater set serial no', 'type': 'T', 'x1': 112, 'y1': 82, 'x2': 143.5, 'y2': 58, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2},
        { 'name': 'section-2-table-row-1-col-6', 'type': 'T', 'x1': 144, 'y1': 53, 'x2': 173.5, 'y2': 58, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Nitrogen Flow (L/min)           (S/No: _____________)', 'priority': 2, 'multiline': True},
        { 'name': 'nitrogen flow serial no', 'type': 'T', 'x1': 145, 'y1': 82, 'x2': 173.5, 'y2': 58, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2},
        { 'name': 'section-2-table-row-1-col-7', 'type': 'T', 'x1': 182, 'y1': 55, 'x2': 182.0, 'y2': 55, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Notes', 'priority': 2, },

        
        { 'name': 'done-by', 'type': 'T', 'x1': 13, 'y1': 250.0, 'x2': 115.0, 'y2': 250.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Done by:', 'priority': 2, },
        { 'name': 'checked-by', 'type': 'T', 'x1': 13, 'y1': 269.0, 'x2': 115.0, 'y2': 269.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Checked by:', 'priority': 2, },
        { 'name': 'page-number', 'type': 'T', 'x1': 194, 'y1': 281.0, 'x2': 194.0, 'y2': 281.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
        
        # data
        {'name': 'section-5-table-data-row-1-type', 'type': 'T', 'x1': 12, 'y1': 79.5, 'x2': 150.0, 'y2': 79.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-1-timestamp', 'type': 'T', 'x1': 26, 'y1': 79.5, 'x2': 150.0, 'y2': 79.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-1-pressure', 'type': 'T', 'x1': 46, 'y1': 79.5, 'x2': 150.0, 'y2': 79.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-1-temperature', 'type': 'T', 'x1': 79, 'y1': 79.5, 'x2': 150.0, 'y2': 79.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-1-heater', 'type': 'T', 'x1': 111, 'y1': 79.5, 'x2': 150.0, 'y2': 79.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-1-flow', 'type': 'T', 'x1': 144, 'y1': 79.5, 'x2': 150.0, 'y2': 79.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-2-type', 'type': 'T', 'x1': 12, 'y1': 88.5, 'x2': 150.0, 'y2': 88.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-2-timestamp', 'type': 'T', 'x1': 26, 'y1': 88.5, 'x2': 150.0, 'y2': 88.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-2-pressure', 'type': 'T', 'x1': 46, 'y1': 88.5, 'x2': 150.0, 'y2': 88.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-2-temperature', 'type': 'T', 'x1': 79, 'y1': 88.5, 'x2': 150.0, 'y2': 88.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-2-heater', 'type': 'T', 'x1': 111, 'y1': 88.5, 'x2': 150.0, 'y2': 88.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-2-flow', 'type': 'T', 'x1': 144, 'y1': 88.5, 'x2': 150.0, 'y2': 88.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-3-type', 'type': 'T', 'x1': 12, 'y1': 97.5, 'x2': 150.0, 'y2': 97.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-3-timestamp', 'type': 'T', 'x1': 26, 'y1': 97.5, 'x2': 150.0, 'y2': 97.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-3-pressure', 'type': 'T', 'x1': 46, 'y1': 97.5, 'x2': 150.0, 'y2': 97.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-3-temperature', 'type': 'T', 'x1': 79, 'y1': 97.5, 'x2': 150.0, 'y2': 97.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-3-heater', 'type': 'T', 'x1': 111, 'y1': 97.5, 'x2': 150.0, 'y2': 97.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-3-flow', 'type': 'T', 'x1': 144, 'y1': 97.5, 'x2': 150.0, 'y2': 97.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-4-type', 'type': 'T', 'x1': 12, 'y1': 106.5, 'x2': 150.0, 'y2': 106.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-4-timestamp', 'type': 'T', 'x1': 26, 'y1': 106.5, 'x2': 150.0, 'y2': 106.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-4-pressure', 'type': 'T', 'x1': 46, 'y1': 106.5, 'x2': 150.0, 'y2': 106.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-4-temperature', 'type': 'T', 'x1': 79, 'y1': 106.5, 'x2': 150.0, 'y2': 106.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-4-heater', 'type': 'T', 'x1': 111, 'y1': 106.5, 'x2': 150.0, 'y2': 106.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-4-flow', 'type': 'T', 'x1': 144, 'y1': 106.5, 'x2': 150.0, 'y2': 106.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-5-type', 'type': 'T', 'x1': 12, 'y1': 115.5, 'x2': 150.0, 'y2': 115.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-5-timestamp', 'type': 'T', 'x1': 26, 'y1': 115.5, 'x2': 150.0, 'y2': 115.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-5-pressure', 'type': 'T', 'x1': 46, 'y1': 115.5, 'x2': 150.0, 'y2': 115.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-5-temperature', 'type': 'T', 'x1': 79, 'y1': 115.5, 'x2': 150.0, 'y2': 115.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-5-heater', 'type': 'T', 'x1': 111, 'y1': 115.5, 'x2': 150.0, 'y2': 115.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-5-flow', 'type': 'T', 'x1': 144, 'y1': 115.5, 'x2': 150.0, 'y2': 115.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-6-type', 'type': 'T', 'x1': 12, 'y1': 124.5, 'x2': 150.0, 'y2': 124.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-6-timestamp', 'type': 'T', 'x1': 26, 'y1': 124.5, 'x2': 150.0, 'y2': 124.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-6-pressure', 'type': 'T', 'x1': 46, 'y1': 124.5, 'x2': 150.0, 'y2': 124.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-6-temperature', 'type': 'T', 'x1': 79, 'y1': 124.5, 'x2': 150.0, 'y2': 124.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-6-heater', 'type': 'T', 'x1': 111, 'y1': 124.5, 'x2': 150.0, 'y2': 124.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-6-flow', 'type': 'T', 'x1': 144, 'y1': 124.5, 'x2': 150.0, 'y2': 124.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-7-type', 'type': 'T', 'x1': 12, 'y1': 133.5, 'x2': 150.0, 'y2': 133.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-7-timestamp', 'type': 'T', 'x1': 26, 'y1': 133.5, 'x2': 150.0, 'y2': 133.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-7-pressure', 'type': 'T', 'x1': 46, 'y1': 133.5, 'x2': 150.0, 'y2': 133.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-7-temperature', 'type': 'T', 'x1': 79, 'y1': 133.5, 'x2': 150.0, 'y2': 133.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-7-heater', 'type': 'T', 'x1': 111, 'y1': 133.5, 'x2': 150.0, 'y2': 133.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-7-flow', 'type': 'T', 'x1': 144, 'y1': 133.5, 'x2': 150.0, 'y2': 133.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-8-type', 'type': 'T', 'x1': 12, 'y1': 142.5, 'x2': 150.0, 'y2': 142.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-8-timestamp', 'type': 'T', 'x1': 26, 'y1': 142.5, 'x2': 150.0, 'y2': 142.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-8-pressure', 'type': 'T', 'x1': 46, 'y1': 142.5, 'x2': 150.0, 'y2': 142.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-8-temperature', 'type': 'T', 'x1': 79, 'y1': 142.5, 'x2': 150.0, 'y2': 142.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-8-heater', 'type': 'T', 'x1': 111, 'y1': 142.5, 'x2': 150.0, 'y2': 142.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-8-flow', 'type': 'T', 'x1': 144, 'y1': 142.5, 'x2': 150.0, 'y2': 142.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-9-type', 'type': 'T', 'x1': 12, 'y1': 151.5, 'x2': 150.0, 'y2': 151.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-9-timestamp', 'type': 'T', 'x1': 26, 'y1': 151.5, 'x2': 150.0, 'y2': 151.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-9-pressure', 'type': 'T', 'x1': 46, 'y1': 151.5, 'x2': 150.0, 'y2': 151.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-9-temperature', 'type': 'T', 'x1': 79, 'y1': 151.5, 'x2': 150.0, 'y2': 151.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-9-heater', 'type': 'T', 'x1': 111, 'y1': 151.5, 'x2': 150.0, 'y2': 151.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-9-flow', 'type': 'T', 'x1': 144, 'y1': 151.5, 'x2': 150.0, 'y2': 151.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-10-type', 'type': 'T', 'x1': 12, 'y1': 160.5, 'x2': 150.0, 'y2': 160.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-10-timestamp', 'type': 'T', 'x1': 26, 'y1': 160.5, 'x2': 150.0, 'y2': 160.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-10-pressure', 'type': 'T', 'x1': 46, 'y1': 160.5, 'x2': 150.0, 'y2': 160.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-10-temperature', 'type': 'T', 'x1': 79, 'y1': 160.5, 'x2': 150.0, 'y2': 160.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-10-heater', 'type': 'T', 'x1': 111, 'y1': 160.5, 'x2': 150.0, 'y2': 160.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-10-flow', 'type': 'T', 'x1': 144, 'y1': 160.5, 'x2': 150.0, 'y2': 160.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-11-type', 'type': 'T', 'x1': 12, 'y1': 169.5, 'x2': 150.0, 'y2': 169.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-11-timestamp', 'type': 'T', 'x1': 26, 'y1': 169.5, 'x2': 150.0, 'y2': 169.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-11-pressure', 'type': 'T', 'x1': 46, 'y1': 169.5, 'x2': 150.0, 'y2': 169.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-11-temperature', 'type': 'T', 'x1': 79, 'y1': 169.5, 'x2': 150.0, 'y2': 169.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-11-heater', 'type': 'T', 'x1': 111, 'y1': 169.5, 'x2': 150.0, 'y2': 169.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-11-flow', 'type': 'T', 'x1': 144, 'y1': 169.5, 'x2': 150.0, 'y2': 169.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-12-type', 'type': 'T', 'x1': 12, 'y1': 178.5, 'x2': 150.0, 'y2': 178.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-12-timestamp', 'type': 'T', 'x1': 26, 'y1': 178.5, 'x2': 150.0, 'y2': 178.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-12-pressure', 'type': 'T', 'x1': 46, 'y1': 178.5, 'x2': 150.0, 'y2': 178.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-12-temperature', 'type': 'T', 'x1': 79, 'y1': 178.5, 'x2': 150.0, 'y2': 178.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-12-heater', 'type': 'T', 'x1': 111, 'y1': 178.5, 'x2': 150.0, 'y2': 178.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-12-flow', 'type': 'T', 'x1': 144, 'y1': 178.5, 'x2': 150.0, 'y2': 178.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-13-type', 'type': 'T', 'x1': 12, 'y1': 187.5, 'x2': 150.0, 'y2': 187.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-13-timestamp', 'type': 'T', 'x1': 26, 'y1': 187.5, 'x2': 150.0, 'y2': 187.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-13-pressure', 'type': 'T', 'x1': 46, 'y1': 187.5, 'x2': 150.0, 'y2': 187.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-13-temperature', 'type': 'T', 'x1': 79, 'y1': 187.5, 'x2': 150.0, 'y2': 187.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-13-heater', 'type': 'T', 'x1': 111, 'y1': 187.5, 'x2': 150.0, 'y2': 187.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-13-flow', 'type': 'T', 'x1': 144, 'y1': 187.5, 'x2': 150.0, 'y2': 187.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-14-type', 'type': 'T', 'x1': 12, 'y1': 196.5, 'x2': 150.0, 'y2': 196.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-14-timestamp', 'type': 'T', 'x1': 26, 'y1': 196.5, 'x2': 150.0, 'y2': 196.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-14-pressure', 'type': 'T', 'x1': 46, 'y1': 196.5, 'x2': 150.0, 'y2': 196.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-14-temperature', 'type': 'T', 'x1': 79, 'y1': 196.5, 'x2': 150.0, 'y2': 196.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-14-heater', 'type': 'T', 'x1': 111, 'y1': 196.5, 'x2': 150.0, 'y2': 196.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-14-flow', 'type': 'T', 'x1': 144, 'y1': 196.5, 'x2': 150.0, 'y2': 196.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-15-type', 'type': 'T', 'x1': 12, 'y1': 205.5, 'x2': 150.0, 'y2': 205.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-15-timestamp', 'type': 'T', 'x1': 26, 'y1': 205.5, 'x2': 150.0, 'y2': 205.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-15-pressure', 'type': 'T', 'x1': 46, 'y1': 205.5, 'x2': 150.0, 'y2': 205.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-15-temperature', 'type': 'T', 'x1': 79, 'y1': 205.5, 'x2': 150.0, 'y2': 205.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-15-heater', 'type': 'T', 'x1': 111, 'y1': 205.5, 'x2': 150.0, 'y2': 205.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-15-flow', 'type': 'T', 'x1': 144, 'y1': 205.5, 'x2': 150.0, 'y2': 205.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-16-type', 'type': 'T', 'x1': 12, 'y1': 214.5, 'x2': 150.0, 'y2': 214.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-16-timestamp', 'type': 'T', 'x1': 26, 'y1': 214.5, 'x2': 150.0, 'y2': 214.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-16-pressure', 'type': 'T', 'x1': 46, 'y1': 214.5, 'x2': 150.0, 'y2': 214.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-16-temperature', 'type': 'T', 'x1': 79, 'y1': 214.5, 'x2': 150.0, 'y2': 214.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-16-heater', 'type': 'T', 'x1': 111, 'y1': 214.5, 'x2': 150.0, 'y2': 214.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-16-flow', 'type': 'T', 'x1': 144, 'y1': 214.5, 'x2': 150.0, 'y2': 214.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-17-type', 'type': 'T', 'x1': 12, 'y1': 223.5, 'x2': 150.0, 'y2': 223.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-17-timestamp', 'type': 'T', 'x1': 26, 'y1': 223.5, 'x2': 150.0, 'y2': 223.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-17-pressure', 'type': 'T', 'x1': 46, 'y1': 223.5, 'x2': 150.0, 'y2': 223.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-17-temperature', 'type': 'T', 'x1': 79, 'y1': 223.5, 'x2': 150.0, 'y2': 223.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-17-heater', 'type': 'T', 'x1': 111, 'y1': 223.5, 'x2': 150.0, 'y2': 223.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-17-flow', 'type': 'T', 'x1': 144, 'y1': 223.5, 'x2': 150.0, 'y2': 223.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-18-type', 'type': 'T', 'x1': 12, 'y1': 232.5, 'x2': 150.0, 'y2': 232.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-18-timestamp', 'type': 'T', 'x1': 26, 'y1': 232.5, 'x2': 150.0, 'y2': 232.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-18-pressure', 'type': 'T', 'x1': 46, 'y1': 232.5, 'x2': 150.0, 'y2': 232.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-18-temperature', 'type': 'T', 'x1': 79, 'y1': 232.5, 'x2': 150.0, 'y2': 232.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-18-heater', 'type': 'T', 'x1': 111, 'y1': 232.5, 'x2': 150.0, 'y2': 232.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-18-flow', 'type': 'T', 'x1': 144, 'y1': 232.5, 'x2': 150.0, 'y2': 232.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-19-type', 'type': 'T', 'x1': 12, 'y1': 241.5, 'x2': 150.0, 'y2': 241.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-19-timestamp', 'type': 'T', 'x1': 26, 'y1': 241.5, 'x2': 150.0, 'y2': 241.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-19-pressure', 'type': 'T', 'x1': 46, 'y1': 241.5, 'x2': 150.0, 'y2': 241.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-19-temperature', 'type': 'T', 'x1': 79, 'y1': 241.5, 'x2': 150.0, 'y2': 241.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-19-heater', 'type': 'T', 'x1': 111, 'y1': 241.5, 'x2': 150.0, 'y2': 241.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        {'name': 'section-5-table-data-row-19-flow', 'type': 'T', 'x1': 144, 'y1': 241.5, 'x2': 150.0, 'y2': 241.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2},
        
    ]
    return elements

def get_post_production_format():
    elements = [

        { 'name': 'form-number', 'type': 'T', 'x1': 145, 'y1': 5, 'x2': 202.0, 'y2': 8.0, 'font': 'Arial', 'size': 8, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'FORM 382-130001-Z-PROC-01 REV 00', 'priority': 2},
        
        { 'name': 'page-border', 'type': 'B', 'x1': 8.0, 'y1': 8.0, 'x2': 202, 'y2': 289.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'page-title', 'type': 'T', 'x1': 84, 'y1': 13.0, 'x2': 115.0, 'y2': 13.0, 'font': 'Arial', 'size': 10.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'CLEANING FORM', 'priority': 2, },
        { 'name': 'line-1', 'type': 'L', 'x1': 8.0, 'y1': 19.0, 'x2': 202.0, 'y2': 19.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'line-1', 'type': 'L', 'x1': 8.0, 'y1': 99.0, 'x2': 202.0, 'y2': 99.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'line-1', 'type': 'L', 'x1': 8.0, 'y1': 179.0, 'x2': 202.0, 'y2': 179.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
        { 'name': 'section-1-header', 'type': 'T', 'x1': 13, 'y1': 23.0, 'x2': 150.0, 'y2': 23.0, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Day 1 Cleaning', 'priority': 2}, 
        { 'name': 'section-1-date', 'type': 'T', 'x1': 13, 'y1': 30.0, 'x2': 150.0, 'y2': 30.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Date: _____________', 'priority': 2}, 
        { 'name': 'section-1-tset', 'type': 'T', 'x1': 13, 'y1': 37.0, 'x2': 150.0, 'y2': 37.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'T set point: _____________', 'priority': 2}, 
        { 'name': 'section-1-start-time', 'type': 'T', 'x1': 73, 'y1': 37.0, 'x2': 150.0, 'y2': 37.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Start time: _____________', 'priority': 2}, 
        { 'name': 'section-1-end-time', 'type': 'T', 'x1': 133, 'y1': 37.0, 'x2': 150.0, 'y2': 37.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'End time: _____________', 'priority': 2}, 
        { 'name': 'section-1-date-input', 'type': 'T', 'x1': 24, 'y1': 29.6, 'x2': 150.0, 'y2': 29.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day 1 cleaning temp set point', 'type': 'T', 'x1': 32, 'y1': 36.6, 'x2': 150.0, 'y2': 36.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'section-1-start-time-input', 'type': 'T', 'x1': 92, 'y1': 36.6, 'x2': 150.0, 'y2': 36.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'section-1-end-time-input', 'type': 'T', 'x1': 150, 'y1': 36.6, 'x2': 150.0, 'y2': 36.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 

        { 'name': 'section-2-header', 'type': 'T', 'x1': 13, 'y1': 103.0, 'x2': 150.0, 'y2': 103.0, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Day 2 Cleaning', 'priority': 2}, 
        { 'name': 'section-2-date', 'type': 'T', 'x1': 13, 'y1': 110.0, 'x2': 150.0, 'y2': 110.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Date: _____________', 'priority': 2}, 
        { 'name': 'section-2-tset', 'type': 'T', 'x1': 13, 'y1': 117.0, 'x2': 150.0, 'y2': 117.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'T set point: _____________', 'priority': 2}, 
        { 'name': 'section-2-start-time', 'type': 'T', 'x1': 73, 'y1': 117.0, 'x2': 150.0, 'y2': 117.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Start time: _____________', 'priority': 2}, 
        { 'name': 'section-2-end-time', 'type': 'T', 'x1': 133, 'y1': 117.0, 'x2': 150.0, 'y2': 117.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'End time: _____________', 'priority': 2}, 
        { 'name': 'section-2-date-input', 'type': 'T', 'x1': 24, 'y1': 109.6, 'x2': 150.0, 'y2': 109.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day 2 cleaning temp set point', 'type': 'T', 'x1': 32, 'y1': 116.6, 'x2': 150.0, 'y2': 116.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'section-2-start-time-input', 'type': 'T', 'x1': 92, 'y1': 116.6, 'x2': 150.0, 'y2': 116.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'section-2-end-time-input', 'type': 'T', 'x1': 150, 'y1': 116.6, 'x2': 150.0, 'y2': 116.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        
        { 'name': 'section-3-header', 'type': 'T', 'x1': 13, 'y1': 183.0, 'x2': 150.0, 'y2': 183.0, 'font': 'Arial', 'size': 9, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Day 3 Drying', 'priority': 2}, 
        { 'name': 'section-3-date', 'type': 'T', 'x1': 13, 'y1': 190.0, 'x2': 150.0, 'y2': 190.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Date: _____________', 'priority': 2}, 
        { 'name': 'section-3-tset', 'type': 'T', 'x1': 13, 'y1': 197.0, 'x2': 150.0, 'y2': 197.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'T set point: _____________', 'priority': 2}, 
        { 'name': 'section-3-start-time', 'type': 'T', 'x1': 73, 'y1': 197.0, 'x2': 150.0, 'y2': 197.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Start time: _____________', 'priority': 2}, 
        { 'name': 'section-3-end-time', 'type': 'T', 'x1': 133, 'y1': 197.0, 'x2': 150.0, 'y2': 197.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'End time: _____________', 'priority': 2}, 
        { 'name': 'section-3-date-input', 'type': 'T', 'x1': 24, 'y1': 189.6, 'x2': 150.0, 'y2': 189.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day 3 drying temp set point', 'type': 'T', 'x1': 32, 'y1': 196.6, 'x2': 150.0, 'y2': 196.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'section-3-start-time-input', 'type': 'T', 'x1': 92, 'y1': 196.6, 'x2': 150.0, 'y2': 196.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'section-3-end-time-input', 'type': 'T', 'x1': 150, 'y1': 196.6, 'x2': 150.0, 'y2': 196.6, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 

        
        { 'name': 'day-1-table-border', 'type': 'B', 'x1': 12.0, 'y1': 44.0, 'x2': 90, 'y2': 92.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-line', 'type': 'L', 'x1': 12.0, 'y1': 52.0, 'x2': 90, 'y2': 52.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-line', 'type': 'L', 'x1': 12.0, 'y1': 60.0, 'x2': 90, 'y2': 60.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-line', 'type': 'L', 'x1': 12.0, 'y1': 68.0, 'x2': 90, 'y2': 68.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-line', 'type': 'L', 'x1': 12.0, 'y1': 76.0, 'x2': 90, 'y2': 76.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-line', 'type': 'L', 'x1': 12.0, 'y1': 84.0, 'x2': 90, 'y2': 84.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-line', 'type': 'L', 'x1': 43.0, 'y1': 44.0, 'x2': 43, 'y2': 92.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-1-table-header', 'type': 'T', 'x1': 23, 'y1': 48.5, 'x2': 150.0, 'y2': 48.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2}, 
        { 'name': 'day-1-table-header', 'type': 'T', 'x1': 54.5, 'y1': 48.5, 'x2': 150.0, 'y2': 48.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)', 'priority': 2}, 


        # { 'name': 'day-1-table-border', 'type': 'B', 'x1': 97.0, 'y1': 44.0, 'x2': 175, 'y2': 92.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-line', 'type': 'L', 'x1': 97.0, 'y1': 52.0, 'x2': 175, 'y2': 52.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-line', 'type': 'L', 'x1': 97.0, 'y1': 60.0, 'x2': 175, 'y2': 60.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-line', 'type': 'L', 'x1': 97.0, 'y1': 68.0, 'x2': 175, 'y2': 68.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-line', 'type': 'L', 'x1': 97.0, 'y1': 76.0, 'x2': 175, 'y2': 76.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-line', 'type': 'L', 'x1': 97.0, 'y1': 84.0, 'x2': 175, 'y2': 84.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-line', 'type': 'L', 'x1': 128.0, 'y1': 44.0, 'x2': 128, 'y2': 92.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-1-table-header', 'type': 'T', 'x1': 108, 'y1': 48.5, 'x2': 150.0, 'y2': 48.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2}, 
        # { 'name': 'day-1-table-header', 'type': 'T', 'x1': 139.5, 'y1': 48.5, 'x2': 150.0, 'y2': 48.5, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)', 'priority': 2}, 
        { 'name': 'day-1-table-row-1-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 56.0, 'x2': 150.0, 'y2': 56.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-1-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 56.0, 'x2': 150.0, 'y2': 56.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-2-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 64.0, 'x2': 150.0, 'y2': 64.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-2-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 64.0, 'x2': 150.0, 'y2': 64.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-3-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 72.0, 'x2': 150.0, 'y2': 72.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-3-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 72.0, 'x2': 150.0, 'y2': 72.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-4-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 80.0, 'x2': 150.0, 'y2': 80.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-4-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 80.0, 'x2': 150.0, 'y2': 80.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-5-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 88.0, 'x2': 150.0, 'y2': 88.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-1-table-row-5-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 88.0, 'x2': 150.0, 'y2': 88.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-6-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 56.0, 'x2': 150.0, 'y2': 56.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-6-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 56.0, 'x2': 150.0, 'y2': 56.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-7-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 64.0, 'x2': 150.0, 'y2': 64.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-7-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 64.0, 'x2': 150.0, 'y2': 64.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-8-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 72.0, 'x2': 150.0, 'y2': 72.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-8-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 72.0, 'x2': 150.0, 'y2': 72.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-9-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 80.0, 'x2': 150.0, 'y2': 80.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-9-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 80.0, 'x2': 150.0, 'y2': 80.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-10-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 88.0, 'x2': 150.0, 'y2': 88.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-1-table-row-10-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 88.0, 'x2': 150.0, 'y2': 88.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 

        { 'name': 'day-2-table-border', 'type': 'B', 'x1': 12.0, 'y1': 124.0, 'x2': 90, 'y2': 172.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-line', 'type': 'L', 'x1': 12.0, 'y1': 132.0, 'x2': 90, 'y2': 132.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-line', 'type': 'L', 'x1': 12.0, 'y1': 140.0, 'x2': 90, 'y2': 140.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-line', 'type': 'L', 'x1': 12.0, 'y1': 148.0, 'x2': 90, 'y2': 148.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-line', 'type': 'L', 'x1': 12.0, 'y1': 156.0, 'x2': 90, 'y2': 156.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-line', 'type': 'L', 'x1': 12.0, 'y1': 164.0, 'x2': 90, 'y2': 164.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-line', 'type': 'L', 'x1': 43.0, 'y1': 124.0, 'x2': 43, 'y2': 172.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-2-table-header', 'type': 'T', 'x1': 23, 'y1': 128.0, 'x2': 150.0, 'y2': 128.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2}, 
        { 'name': 'day-2-table-header', 'type': 'T', 'x1': 54.5, 'y1': 128.0, 'x2': 150.0, 'y2': 128.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)', 'priority': 2}, 

        
        # { 'name': 'day-2-table-border', 'type': 'B', 'x1': 97.0, 'y1': 124.0, 'x2': 175, 'y2': 172.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-line', 'type': 'L', 'x1': 97.0, 'y1': 132.0, 'x2': 175, 'y2': 132.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-line', 'type': 'L', 'x1': 97.0, 'y1': 140.0, 'x2': 175, 'y2': 140.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-line', 'type': 'L', 'x1': 97.0, 'y1': 148.0, 'x2': 175, 'y2': 148.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-line', 'type': 'L', 'x1': 97.0, 'y1': 156.0, 'x2': 175, 'y2': 156.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-line', 'type': 'L', 'x1': 97.0, 'y1': 164.0, 'x2': 175, 'y2': 164.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-line', 'type': 'L', 'x1': 128.0, 'y1': 124.0, 'x2': 128, 'y2': 172.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-2-table-header', 'type': 'T', 'x1': 108, 'y1': 128.0, 'x2': 150.0, 'y2': 128.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2}, 
        # { 'name': 'day-2-table-header', 'type': 'T', 'x1': 139.5, 'y1': 128.0, 'x2': 150.0, 'y2': 128.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)', 'priority': 2}, 
        { 'name': 'day-2-table-row-1-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 136.0, 'x2': 150.0, 'y2': 136.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-1-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 136.0, 'x2': 150.0, 'y2': 136.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-2-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 144.0, 'x2': 150.0, 'y2': 144.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-2-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 144.0, 'x2': 150.0, 'y2': 144.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-3-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 152.0, 'x2': 150.0, 'y2': 152.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-3-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 152.0, 'x2': 150.0, 'y2': 152.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-4-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 160.0, 'x2': 150.0, 'y2': 160.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-4-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 160.0, 'x2': 150.0, 'y2': 160.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-5-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 168.0, 'x2': 150.0, 'y2': 168.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-2-table-row-5-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 168.0, 'x2': 150.0, 'y2': 168.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-6-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 136.0, 'x2': 150.0, 'y2': 136.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-6-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 136.0, 'x2': 150.0, 'y2': 136.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-7-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 144.0, 'x2': 150.0, 'y2': 144.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-7-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 144.0, 'x2': 150.0, 'y2': 144.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-8-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 152.0, 'x2': 150.0, 'y2': 152.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-8-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 152.0, 'x2': 150.0, 'y2': 152.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-9-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 160.0, 'x2': 150.0, 'y2': 160.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-9-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 160.0, 'x2': 150.0, 'y2': 160.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-10-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 168.0, 'x2': 150.0, 'y2': 168.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-2-table-row-10-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 168.0, 'x2': 150.0, 'y2': 168.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 


        { 'name': 'day-3-table-border', 'type': 'B', 'x1': 12.0, 'y1': 204.0, 'x2': 90, 'y2': 252.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-line', 'type': 'L', 'x1': 12.0, 'y1': 212.0, 'x2': 90, 'y2': 212.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-line', 'type': 'L', 'x1': 12.0, 'y1': 220.0, 'x2': 90, 'y2': 220.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-line', 'type': 'L', 'x1': 12.0, 'y1': 228.0, 'x2': 90, 'y2': 228.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-line', 'type': 'L', 'x1': 12.0, 'y1': 236.0, 'x2': 90, 'y2': 236.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-line', 'type': 'L', 'x1': 12.0, 'y1': 244.0, 'x2': 90, 'y2': 244.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-line', 'type': 'L', 'x1': 43.0, 'y1': 204.0, 'x2': 43, 'y2': 252.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        { 'name': 'day-3-table-header', 'type': 'T', 'x1': 23, 'y1': 208.0, 'x2': 150.0, 'y2': 208.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2}, 
        { 'name': 'day-3-table-header', 'type': 'T', 'x1': 54.5, 'y1': 208.0, 'x2': 150.0, 'y2': 208.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)', 'priority': 2}, 

        # { 'name': 'day-3-table-border', 'type': 'B', 'x1': 97.0, 'y1': 204.0, 'x2': 175, 'y2': 252.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-line', 'type': 'L', 'x1': 97.0, 'y1': 212.0, 'x2': 175, 'y2': 212.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-line', 'type': 'L', 'x1': 97.0, 'y1': 220.0, 'x2': 175, 'y2': 220.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-line', 'type': 'L', 'x1': 97.0, 'y1': 228.0, 'x2': 175, 'y2': 228.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-line', 'type': 'L', 'x1': 97.0, 'y1': 236.0, 'x2': 175, 'y2': 236.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-line', 'type': 'L', 'x1': 97.0, 'y1': 244.0, 'x2': 175, 'y2': 244.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-line', 'type': 'L', 'x1': 128.0, 'y1': 204.0, 'x2': 128, 'y2': 252.0, 'font': 'Arial', 'size': 0.3, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
        # { 'name': 'day-3-table-header', 'type': 'T', 'x1': 108, 'y1': 208.0, 'x2': 150.0, 'y2': 208.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Time', 'priority': 2}, 
        # { 'name': 'day-3-table-header', 'type': 'T', 'x1': 139.5, 'y1': 208.0, 'x2': 150.0, 'y2': 208.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Vessel Temp (°C)', 'priority': 2}, 
        { 'name': 'day-3-table-row-1-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 216.0, 'x2': 150.0, 'y2': 216.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-1-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 216.0, 'x2': 150.0, 'y2': 216.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-2-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 224.0, 'x2': 150.0, 'y2': 224.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-2-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 224.0, 'x2': 150.0, 'y2': 224.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-3-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 232.0, 'x2': 150.0, 'y2': 232.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-3-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 232.0, 'x2': 150.0, 'y2': 232.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-4-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 240.0, 'x2': 150.0, 'y2': 240.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-4-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 240.0, 'x2': 150.0, 'y2': 240.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-5-col-1-input', 'type': 'T', 'x1': 16.0, 'y1': 248.0, 'x2': 150.0, 'y2': 248.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        { 'name': 'day-3-table-row-5-col-2-input', 'type': 'T', 'x1': 58.0, 'y1': 248.0, 'x2': 150.0, 'y2': 248.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-6-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 216.0, 'x2': 150.0, 'y2': 216.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-6-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 216.0, 'x2': 150.0, 'y2': 216.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-7-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 224.0, 'x2': 150.0, 'y2': 224.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-7-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 224.0, 'x2': 150.0, 'y2': 224.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-8-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 232.0, 'x2': 150.0, 'y2': 232.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-8-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 232.0, 'x2': 150.0, 'y2': 232.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-9-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 240.0, 'x2': 150.0, 'y2': 240.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-9-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 240.0, 'x2': 150.0, 'y2': 240.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-10-col-1-input', 'type': 'T', 'x1': 100.0, 'y1': 248.0, 'x2': 150.0, 'y2': 248.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 
        # { 'name': 'day-3-table-row-10-col-2-input', 'type': 'T', 'x1': 145.0, 'y1': 248.0, 'x2': 150.0, 'y2': 248.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2}, 

        { 'name': 'done-by', 'type': 'T', 'x1': 13.0, 'y1': 268.0, 'x2': 150.0, 'y2': 268.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Done by: ___________________', 'priority': 2}, 
        { 'name': 'checked-by', 'type': 'T', 'x1': 87.0, 'y1': 268.0, 'x2': 150.0, 'y2': 268.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'Checked by: ___________________', 'priority': 2}, 
        { 'name': 'page-number', 'type': 'T', 'x1': 194, 'y1': 281.0, 'x2': 194.0, 'y2': 281.0, 'font': 'Arial', 'size': 9, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },

    ]

    return elements


if __name__ == '__main__':
    log = logger.init(os.path.abspath(__file__), '') # logging
    database.init(log) # database
    generate(log, 104)