import os
import time
import logging
from logging.handlers import RotatingFileHandler
import configparser
import pysftp
import pandas as pd

FORMATTER = logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s  — %(message)s")

LOG_FILE_PATH="logs/main.log"
MAIN_LOG_SIZE=1024*1024
MAIN_LOG_FILES=10

PRIVATE_KEY_PATH="C:\ProgramData\ssh\ssh_host_rsa_key"

BACKUP_DEVICE_LIST={"m-cba-nsw-bellavista-sbc01":"10.10.1.13","m-cba-nsw-bellavista-sbc02":"10.10.1.13","m-cba-nsw-bellavista-sbc03":"10.10.1.13"}

REMOTE_FILE_PATH='/code/gzConfig/dataDoc.gz'
LOCAL_FILE_PATH='K:\\'
SBC_SFTP_USER='sftp'

def setup_logger(name, log_file,file_size,file_count,level=logging.INFO):

    file_handler = RotatingFileHandler(log_file,maxBytes=file_size,backupCount=file_count)        
    file_handler.setFormatter(FORMATTER)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    return logger

def cleanup (number_of_days,root_path):

        time_in_secs = time.time()-(number_of_days * 24 * 60 * 60)
        count=0
        
        logger=logging.getLogger("MAIN")
        logger.info("Log file cleanup starting ")

        try:
            for root, dirs, files in os.walk(root_path, topdown=False):
                for file in files:
                    full_path = os.path.join(root, file)
                    stat = os.stat(full_path)
                    if stat.st_mtime <= time_in_secs:
                            os.remove(full_path)
                            count+=1
            
        except:
            logger.exception("An Exception Occured")
           
        else:
            logger.info("Sucessfully deleted %s file(s)",count)
            logger.info("Log file cleanup finished.")

def backup():

    logger=logging.getLogger("MAIN")
    logger_backup=setup_logger("BACKUP",LOG_FILE_PATH,MAIN_LOG_SIZE,MAIN_LOG_FILES)
    
    logger.info("Starting SBC backups ")
    count=0
    timestr = time.strftime("%Y%m%d%H%M%S-")

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        for (device_name,ip_address) in BACKUP_DEVICE_LIST.items(): 
            sftp=pysftp.Connection(ip_address,username=SBC_SFTP_USER,private_key=PRIVATE_KEY_PATH,cnopts=cnopts)
            sftp.get(REMOTE_FILE_PATH,LOCAL_FILE_PATH+timestr+device_name+".gz")
            logger.info("Backup of %s completed",device_name)
            count+=1
            sftp.close()
            
    except:
         logger.exception("An Exception Occured")


    else:
        logger.info("Sucessfully backed up %s device(s)",count)
        logger.info("Backup finished.")
        
    finally:
        sftp.close()
    
        
def reports(begin_datetime,end_datetime,root_path):


    pattern = '%d/%m/%Y %H:%M:%S'
    begin_epoch = int(time.mktime(time.strptime(begin_datetime, pattern)))
    end_epoch = int(time.mktime(time.strptime(end_datetime, pattern)))
        
    logger=logging.getLogger("MAIN")
    logger.info("Search for file(s) starting ")
    count=0
    file_list=[]

    try:
        for root, dirs, files in os.walk(root_path, topdown=False):
            for file in files:
                full_path = os.path.join(root, file)
                stat = os.stat(full_path)
                if ((stat.st_mtime <= end_epoch) & (stat.st_mtime >= begin_epoch)):
                        file_list.append(full_path)
                        count+=1
    except:
         logger.exception("An Exception Occured")

    else:
        logger.info("Found %s file(s)",len(file_list))


    try:
        logger.info("Loading file(s) starting ")
        df=pd.concat((pd.read_csv(file,usecols=['TimeStamp','CPU Utilization']) for file in file_list))
        logger.info("Loaded %s file(s) ",len(file_list))
        
        df['TimeStamp']=pd.DatetimeIndex(pd.to_datetime(df['TimeStamp'],unit='s')).tz_localize('UTC').tz_convert('Australia/Sydney')
        df['Date'] = df['TimeStamp'].dt.strftime('%y/%d/%m')
        df.groupby('Date')
        
    except:
         logger.exception("An Exception Occured")

    else:
        print(df)
        logger.info("Loaded %s file(s) ",len(file_list))
        logger.info("Loading complete")
                          
def main():

    try:
        logger_main=setup_logger("MAIN",LOG_FILE_PATH,MAIN_LOG_SIZE,MAIN_LOG_FILES)      
        logger_main.info("Main script started")
        logger_main.info("Main Script finished")

        #cleanup(5,"c:\\temp\\")
        #backup()
        reports("15/05/2020 00:00:00","16/05/2020 00:15:00","K:\HDR\CY-SBC01\system\\")

    except:
        logger_main.exception("An Exception Occured")    

    finally:
        logger_main.handlers.pop()
        
if __name__ == '__main__':
        main()       
