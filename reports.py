import os
import time
import logging
import pandas as pd
from common import setup_logger

REPORT_LOG_FILE_PATH="logs/main.log"
REPORT_LOG_SIZE=1024*1024
REPORT_LOG_FILES=10
REPORT_DEVICE_LIST=['m-cba-nsw-bellavista-sbc01_m-cba-nsw-bellavista-sbc02','m-cba-nsw-bellavista-sbc03','m-cba-nsw-bellavista-sbc04','m-cba-nsw-burwood-sbc01_m-cba-nsw-burwood-sbc02','m-cba-nsw-burwood-sbc03','m-cba-nsw-burwood-sbc04']
REPORT_LOCAL_FILE_PATH='K:\HDR'

def reports(begin_datetime,end_datetime,root_path,device_name):

    pattern = '%d/%m/%Y %H:%M:%S'
    begin_epoch = int(time.mktime(time.strptime(begin_datetime, pattern)))
    end_epoch = int(time.mktime(time.strptime(end_datetime, pattern)))
        
    logger_main=setup_logger("MAIN",LOG_FILE_PATH,MAIN_LOG_SIZE,MAIN_LOG_FILES)      
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
        df=pd.concat((pd.read_csv(file,usecols=['TimeStamp','CPU Utilization','Memory Utilization','Signaling Sessions']) for file in file_list))
        logger.info("Loaded %s file(s) ",len(file_list))

        tic = time.perf_counter()
        logger.info("processing data... this may take a while")
        df['TimeStamp']=pd.DatetimeIndex(pd.to_datetime(df['TimeStamp'],unit='s')).tz_localize('UTC').tz_convert('Australia/Sydney')
        df['Date'] = df['TimeStamp'].dt.strftime('%d/%m/%y')
        df=df.groupby(['Date'])[['CPU Utilization','Memory Utilization','Signaling Sessions']].max()

        df.rename(columns = {'CPU Utilization':'CPU Utilization Max', 'Memory Utilization':'Memory Utilization Max','Signaling Sessions':'Signaling Sessions Max'}, inplace = True) 
        
        
    except:
         logger.exception("An Exception Occured")

    else:
        toc = time.perf_counter()
        logger.info(f"processing data complete. Operation took {toc-tic:0.4f} seconds")

    try:
        logger.info("Writing report to file - %s",device_name)
        df.to_csv(device_name)
            
    except:
         logger.exception("An Exception Occured")
         
    else:
        logger.info("Report writing completed")

  
if __name__ == '__main__':
        reports()       
