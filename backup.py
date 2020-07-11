import time
import pysftp
import logging
from common import setup_logger,cleanup

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
LOCAL_FILE_PATH='K:\BACKUP\\'
DAYS_TO_KEEP_BACKUPS=30
LOG_TO_CONSOLE=True

def backup(logger_name):
    
    try:
        logger_backup=logging.getLogger(logger_name)
        logger_archive=setup_logger("ARCHIVE",ARCH_LOG_FILE_PATH,ARCH_LOG_FILE_SIZE,ARCH_LOG_FILE_MAX)
        
        logger_backup.info("**** backup script started *****")
        logger_backup.info("starting backup of %s device(s)",len(BACKUP_DEVICE_LIST))
        
        bkup_sucessfull=0
        bkup_failed=0
        timestr = time.strftime("%Y%m%d%H%M%S-")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        sftp = None
       
        for (device_name,ip_address) in BACKUP_DEVICE_LIST.items():
            try:
                sftp=pysftp.Connection(ip_address,username=SBC_SFTP_USER,private_key=PRIVATE_KEY_PATH,cnopts=cnopts)
                
            except Exception:
                logger_backup.exception("!!!! Exception Occured !!!!")
                logger_backup.error("unable to connect to device %s ",device_name)
                logger_archive.error("backup of %s failed",device_name)
                bkup_failed+=1
                pass

            else:
                try:
                    sftp.get(REMOTE_FILE_PATH,LOCAL_FILE_PATH+timestr+device_name+".gz")
                    logger_backup.info("backup of %s completed",device_name)
                    logger_archive.info("backup of %s completed sucessfully to %s",device_name,LOCAL_FILE_PATH+timestr+device_name+".gz")
                    bkup_sucessfull+=1
                    
                except:
                    logger_backup.exception("!!!! Exception Occured !!!!")
                    logger_backup.error("unable to retrive backup file from device %s ",device_name)
                    bkup_failed+=1
                    pass
                    
            finally:
                sftp.close()
                
                
               
    except Exception:
        logger_backup.exception("Exception Occured")
        

    else:
        logger_backup.info("backed up %s device(s) sucessfully. %s device(s) failed",bkup_sucessfull,bkup_failed)
        logger_backup.info("**** backup script finished ****\n")
        

    finally:
        logger_archive.handlers.pop()
     
        
if __name__ == '__main__':

    try:
        logger_main=setup_logger("BACKUP",BKUP_LOG_FILE_PATH,BKUP_LOG_FILE_SIZE,BKUP_LOG_FILE_MAX,LOG_TO_CONSOLE)
            
    except Exception:
        logger_main.exception("!!!! Exception Occured !!!!")
        logger_main.exception("unable to setup logger")

    else:
        backup("BACKUP")
        cleanup(DAYS_TO_KEEP_BACKUPS,LOCAL_FILE_PATH,"BACKUP")
        
    finally:
        logger_main.handlers.pop()
        
