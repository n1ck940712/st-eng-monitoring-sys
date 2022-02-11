from modules import database, logger
import report
import os

if __name__ == "__main__":
    # init modules
    log = logger.init(os.path.abspath(__file__), '') # logging
    database.init(log) # database
    # end init
    log.info("Modules Initiation DONE...")
    log.info("===============================\n")
    log.info("%s RUNNING..." % os.path.splitext(os.path.basename(__file__))[0])
    
    # main program
    report.generate(log, 89)