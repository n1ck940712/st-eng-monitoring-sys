# =================================================================
# encryption
# =================================================================

def init(logger):
    try:
        from cryptography.fernet import Fernet
        global PUBLIC_KEY, PRIVATE_KEY, PRIVATE_KEY_2,cipher, log
        log = logger
        PUBLIC_KEY = "#@!Od1jeksAV6ipAxk68PuBUhROCwuNC7Jo!@#!"
        PRIVATE_KEY_2 = "(T_T)FL0T3cH-WQ@MQTTPuBPRFLP2-Pr1v@t3KeY(-_*)|"
        PRIVATE_KEY = b'qzW-hqnBgh5aLuohWSYzcPe1rjdy6xlTzDlZP1oXCs8='
        log.info('encrypt.init SUCCESS')
        return Fernet(PRIVATE_KEY)
    except Exception as ex:
        log.error('encrypt.init FAILED. %s' % ex)
    return
