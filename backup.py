import time
import pysftp
import logging
from common import setup_logger 

BACKUP_DEVICE_LIST={"m-cba-nsw-bellavista-sbc01":"10.10.1.13","m-cba-nsw-bellavista-sbc02":"10.10.1.13","m-cba-nsw-bellavista-sbc03":"10.10.1.13"}
SBC_SFTP_USER='sftp'
LOG_FILE_PATH="logs/backup.log"
MAIN_LOG_SIZE=1024*1024
MAIN_LOG_FILES=10
PRIVATE_KEY_PATH="C:\ProgramData\ssh\ssh_host_rsa_key"
REMOTE_FILE_PATH='/code/gzConfig/dataDoc.gz'
LOCAL_FILE_PATH='K:\\'

def backup():

    logger=logging.getLogger("BACKUP")
    logger.info("starting SBC backups ")
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

def main():
    try:
        logger_main=setup_logger("BACKUP",LOG_FILE_PATH,MAIN_LOG_SIZE,MAIN_LOG_FILES)      
        logger_main.info("backup script started")

        backup()
        
    except:
        logger_main.exception("An Exception Occured")

    else:
        logger_main.info("backup script finished")

    finally:
        logger_main.handlers.pop()
        

if __name__ == '__main__':
        main()       
