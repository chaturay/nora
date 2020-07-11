import logging
import time
import os
import sys
from logging.handlers import RotatingFileHandler


FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] [%(funcName)s]  %(message)s")

def setup_logger(name, log_file,file_size,file_count,log_to_console=False,level=logging.INFO):

    file_handler = RotatingFileHandler(log_file,maxBytes=file_size,backupCount=file_count)
    
    file_handler.setFormatter(FORMATTER)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    # if log_to_console is True, then enable logging to stdout as well
    if log_to_console:
        stream_handler=logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(FORMATTER)
        logger.addHandler(stream_handler)
        
    return logger

def cleanup (number_of_days,root_path,logger_name,prefix=""):

        time_in_secs = time.time()-(number_of_days * 24 * 60 * 60)
        count=0
        
        logger=logging.getLogger(logger_name)
        logger.info("**** %s file cleanup starting ****",prefix)
        tic = time.perf_counter()
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
            toc = time.perf_counter()
            logger.info("sucessfully deleted %s file(s),",count)
            logger.info(f"cleanup took {toc-tic:0.4f} seconds")
            logger.info("**** %s file cleanup finished ****\n",prefix)
            
