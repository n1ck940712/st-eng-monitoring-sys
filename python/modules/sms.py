# =================================================================
# sms module
# =================================================================

# Wavecell sms api
# alarm / sms alert
def init(logger):
    try:
        from wavecell import Wavecell
        global SOURCE, SOURCE, BODY, INTERVAL, ADMIN_NUM, log
        log = logger
        ACCOUNT_ID = "Flotech_0aAA0_hq"
        API_KEY = "0KgKGVlSKfxmh0RuZsXeOTOKqQjhqlYsReMBwscFN60"
        SOURCE = "FLOTECH IO"
        FOOTER = ",\nPlease login to view status: https://iot.flotech.io/rfid-monitoring/ \n\nBest Regards,\nFlotech Controls Pte Ltd"
        INTERVAL = 900 # 15 mins 
        ADMIN_NUM = "+6589395966"
        send_sms_flag = False
        log.info('sms.init SUCCESS')
        return Wavecell(sub_account_id=ACCOUNT_ID, api_key=API_KEY)
    except Exception as ex:
        log.error('sms module init FAILED. %s' % ex)

def send(message, number):
    try:
        body = message+"\nDear "+str(name)+str(FOOTER)
        p = {
            "source": str(SOURCE),
            "destination": str(number),
            "text": str(body)
            }
        wave.send_sms_single(param=p)
    except Exception as ex:
        log.error('sms.send FAILED. %s' % ex)
    return