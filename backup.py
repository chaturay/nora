import time
import pysftp
import logging
from common import setup_logger

# set values for the parameters used in this module.
BACKUP_DEVICE_LIST={"m-cba-nsw-bellavista-sbc01":"10.10.1.13","m-cba-nsw-bellavista-sbc02":"10.10.1.13","m-cba-nsw-bellavista-sbc03":"10.10.1.13"}  
SBC_SFTP_USER= 'sftp'
BKUP_LOG_FILE_PATH="logs/backup.log"
BKUP_LOG_FILE_SIZE=1024*1024
BKUP_LOG_FILE_MAX=10
ARCH_LOG_FILE_PATH="logs/archive.log"
ARCH_LOG_FILE_SIZE=1024*1024
ARCH_LOG_FILE_MAX=10
PRIVATE_KEY_PATH="C:\ProgramData\ssh\ssh_host_rsa_key"
REMOTE_FILE_PATH='/code/gzConfig/dataDoc.gz'
LOCAL_FILE_PATH='K:\\'

def main():
    
    try:
        logger_backup=setup_logger("BACKUP",BKUP_LOG_FILE_PATH,BKUP_LOG_FILE_SIZE,BKUP_LOG_FILE_MAX)
        logger_archive=setup_logger("ARCHIVE",ARCH_LOG_FILE_PATH,ARCH_LOG_FILE_SIZE,ARCH_LOG_FILE_MAX)
        
        logger_backup.info("backup script started")
        logger_backup.info("starting device backups")
        
        count=0
        timestr = time.strftime("%Y%m%d%H%M%S-")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        
        for (device_name,ip_address) in BACKUP_DEVICE_LIST.items(): 
            sftp=pysftp.Connection(ip_address,username=SBC_SFTP_USER,private_key=PRIVATE_KEY_PATH,cnopts=cnopts)
            sftp.get(REMOTE_FILE_PATH,LOCAL_FILE_PATH+timestr+device_name+".gz")
            logger_backup.info("backup of %s completed",device_name)
            logger_archive.info("backup of %s completed sucessfully",device_name)
            count+=1
            

        logger_backup.info("backup script finished.")
        
    except:
        logger_backup.exception("Exception Occured")

    else:
        logger_backup.info("sucessfully backed up %s device(s)",count)
        logger_backup.info("backup script finished")
        

    finally:
        logger_backup.handlers.pop()
        logger_archive.handlers.pop()
        sftp.close()
        
if __name__ == '__main__':
        main()       
