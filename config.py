class backup_settings:

    # settings used by backup.py
    BACKUP_DEVICE_LIST={"m-cba-nsw-bellavista-sbc01":"10.10.1.13","m-cba-nsw-bellavista-sbc02":"10.10.1.13","m-cba-nsw-bellavista-sbc03":"10.10.1.13"}  
    SFTP_USER_NAME= 'sftp'
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

class reports_settings:
    REPORT_LOG_FILE_PATH="logs/reports.log"
    REPORT_LOG_SIZE=1024*1024
    REPORT_LOG_FILES=10
    REPORT_DEVICE_LIST=['m-cba-nsw-bellavista-sbc01_m-cba-nsw-bellavista-sbc02','m-cba-nsw-bellavista-sbc03','m-cba-nsw-bellavista-sbc04','m-cba-nsw-burwood-sbc01_m-cba-nsw-burwood-sbc02','m-cba-nsw-burwood-sbc03','m-cba-nsw-burwood-sbc04']
    REPORT_LOCAL_FILE_PATH='K:\REPORTS\\'
    HDR_LOCAL_PATH='K:\HDR\\'
    DAYS_TO_KEEP_REPORTS=60
    DAYS_TO_KEEP_HDR=365
    LOG_TO_CONSOLE=True
