# =================================================================
# databases
# =================================================================
import cymysql

def init(logger):
    try:
        global HOST, USERNAME, PASSWORD, DATABASE, USERNAME, log
        global HOST_REMOTE, USERNAME_REMOTE, PASSWORD_REMOTE, DATABASE_REMOTE
        log = logger
        #local mysql db 
        HOST = '127.0.0.1'
        USERNAME = 'pi'
        PASSWORD = 'FlotechP@$$787814'
        DATABASE = 'monitoring_sys'

        #  remote mysql db
        HOST_REMOTE = '127.0.0.1'
        USERNAME_REMOTE = 'pi'
        PASSWORD_REMOTE = 'FlotechP@$$787814'
        DATABASE_REMOTE = 'monitoring_sys'

        #  remote mysql db
        HOST_TEST = '127.0.0.1'
        USERNAME_TEST = 'pi'
        PASSWORD_TEST = 'FlotechP@$$787814'
        DATABASE_TEST = 'monitoring_sys'

        log.info('database.init SUCCESS. db (local): %s. db (remote): %s. db (test): %s' % (HOST, HOST_REMOTE, HOST_TEST))

    except Exception as ex:
        log.error('database.init FAILED. %s' % ex)
    return

def query(location, mode, sql):
    try:
        if location == 'local':
            conn = cymysql.connect(host=HOST, user=USERNAME, passwd=PASSWORD, db=DATABASE)
            cur = conn.cursor()   
            cur.execute(sql)
            if mode in ('insert', 'update'):
                conn.commit()
                cur.close()
                conn.close()
            elif mode == 'get':
                rows = cur.fetchall()
                cur.close()
                conn.close()
                return rows
        elif location == 'remote':
            conn_remote = cymysql.connect(host=HOST_REMOTE, user=USERNAME_REMOTE, passwd=PASSWORD_REMOTE, db=DATABASE_REMOTE)
            cur_remote=conn_remote.cursor()
            cur_remote.execute(sql)
            if mode in ('insert', 'update'):
                conn_remote.commit()
                cur_remote.close()
                conn_remote.close()
            elif mode == 'get':
                rows = cur_remote.fetchall()
                cur_remote.close()
                conn_remote.close()
                return rows
        elif location == 'test':
            conn_test = cymysql.connect(host=HOST_TEST, user=USERNAME_TEST, passwd=PASSWORD_TEST, db=DATABASE_TEST)
            cur_test=conn_test.cursor()
            cur_test.execute(sql)
            if mode in ('insert', 'update'):
                conn_test.commit()
                cur_test.close()
                conn_test.close()
            elif mode == 'get':
                rows = cur_test.fetchall()
                cur_test.close()
                conn_test.close()
                return rows
    except Exception as ex:
        log.error('mysql_query (%s, %s) FAILED.\n%s' %(location, mode, str(ex)))
    return
    