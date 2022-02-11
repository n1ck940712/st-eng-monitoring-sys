# =================================================================
# logging configuration
# =================================================================

def init(file_dir, log_level=''):
    import logging, os
    from logging.handlers import TimedRotatingFileHandler
    level = {
        '': logging.NOTSET,
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    try:
        global logger
        logger = logging.getLogger('')
        logger.setLevel(level[log_level])
        FILE_DIR, FILENAME = os.path.split(file_dir)
        FILENAME = FILENAME.split('.')[0]
        FILE_PATH = FILE_DIR + '/logs/' + FILENAME + '/' + FILENAME
        if not os.path.exists(FILE_DIR + '/logs/' + FILENAME):
            os.makedirs(FILE_DIR + '/logs/' + FILENAME)
            print('created directory: %s' % FILE_DIR + '/logs/' + FILENAME)
        fh = TimedRotatingFileHandler(FILE_PATH, when = 'midnight', interval = 1)
        fh.suffix = "%Y%m%d"
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger
        logger.info('logger.init SUCCESS')
    except Exception as ex:
        logger.error('logger.init FAILED. %s' % ex)
    return 