import logging
import time
import os
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] [%(funcName)s]  %(message)s")

def setup_logger(name, log_file,file_size,file_count,level=logging.INFO):

    file_handler = RotatingFileHandler(log_file,maxBytes=file_size,backupCount=file_count)        
    file_handler.setFormatter(FORMATTER)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    return logger

def cleanup (number_of_days,root_path,logger_name):

        time_in_secs = time.time()-(number_of_days * 24 * 60 * 60)
        count=0
        
        logger=logging.getLogger(logger_name)
        logger.info("**** file cleanup starting ****")

        try:
            for root, dirs, files in os.walk(root_path, topdown=False):
                for file in files:
                    full_path = os.path.join(root, file)
                    stat = os.stat(full_path)
                    if stat.st_mtime <= time_in_secs:
                        os.remove(full_path)
                        count+=1
                            
            
        except Exception:
            logger.exception("!!!! Exception Occured !!!!")
           
        else:
            logger.info("sucessfully deleted %s file(s)",count)
            logger.info("**** file cleanup finished ****\n")
