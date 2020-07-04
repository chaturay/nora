import logging
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] [%(funcName)s]  %(message)s")

def setup_logger(name, log_file,file_size,file_count,level=logging.INFO):

    file_handler = RotatingFileHandler(log_file,maxBytes=file_size,backupCount=file_count)        
    file_handler.setFormatter(FORMATTER)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    return logger

