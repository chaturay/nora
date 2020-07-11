import os
import time
import logging
import calendar
import datetime
import pandas as pd
from common import setup_logger,cleanup
import argparse
import json

# set values for the parameters used in this module.
REPORT_LOG_FILE_PATH="logs/reports.log"
REPORT_LOG_SIZE=1024*1024
REPORT_LOG_FILES=10
REPORT_DEVICE_LIST=['m-cba-nsw-bellavista-sbc01_m-cba-nsw-bellavista-sbc02','m-cba-nsw-bellavista-sbc03','m-cba-nsw-bellavista-sbc04','m-cba-nsw-burwood-sbc01_m-cba-nsw-burwood-sbc02','m-cba-nsw-burwood-sbc03','m-cba-nsw-burwood-sbc04']
REPORT_LOCAL_FILE_PATH='K:\REPORTS\\'
HDR_LOCAL_PATH='K:\HDR\\'
DAYS_TO_KEEP_REPORTS=60
DAYS_TO_KEEP_HDR=365
LOG_TO_CONSOLE=True

def reports(begin_datetime,end_datetime,device_name):

    begin_epoch=begin_datetime.timestamp()
    end_epoch=end_datetime.timestamp()

    timestr = time.strftime("%Y-%m-%d-%H%M%S-")
    report_path=REPORT_LOCAL_FILE_PATH+timestr+f"{device_name}.csv"
    hdr_path=HDR_LOCAL_PATH+f"{device_name}\system"  
        
    logger=logging.getLogger("REPORTS")
    logger.info("search for file(s) between %s - %s for %s",begin_datetime,end_datetime,hdr_path)
    file_count=0
    file_list=[]

    try:
        for root, dirs, files in os.walk(hdr_path, topdown=False):
            for file in files:
                full_path = os.path.join(root, file)
                stat = os.stat(full_path)
                if ((stat.st_mtime <= end_epoch) & (stat.st_mtime >= begin_epoch)):
                        file_list.append(full_path)
                        
    except Exceptionn:
         logger.exception("!!!! Exception Occured !!!!")
         

    else:
        file_count=len(file_list)

        if file_count > 0:
            logger.info("found %s file(s)",file_count)
    
            try:
                logger.info("loading file(s) starting ")
                df=pd.concat((pd.read_csv(file,usecols=['TimeStamp','CPU Utilization','Memory Utilization','Signaling Sessions']) for file in file_list))
                logger.info("loaded %s file(s) ",len(file_list))

                tic = time.perf_counter()
                logger.info("processing data... this may take a while")
                df['TimeStamp']=pd.DatetimeIndex(pd.to_datetime(df['TimeStamp'],unit='s')).tz_localize('UTC').tz_convert('Australia/Sydney')
                df['Date'] = df['TimeStamp'].dt.strftime('%d/%m/%y')
                df=df.groupby(['Date'])[['CPU Utilization','Memory Utilization','Signaling Sessions']].max()

                df.rename(columns = {'CPU Utilization':'CPU Utilization Max', 'Memory Utilization':'Memory Utilization Max','Signaling Sessions':'Signaling Sessions Max'}, inplace = True) 
                
                
            except:
                 logger.exception("!!!! Exception Occured !!!!")

            else:
                toc = time.perf_counter()
                logger.info(f"processing data complete.operation took {toc-tic:0.4f} seconds")
            try:
                logger.info("writing report to file - %s",report_path)
                df.to_csv(report_path)
                    
            except:
                 logger.exception("!!!! Exception Occured !!!!")
                 
            else:
                logger.info("report writing completed\n")
        else:
            logger.info("no files found matching the date range for %s \n",hdr_path)

def main(b_date,e_date):
        
    try:
        # initialize logger
        logger_reports=setup_logger("REPORTS",REPORT_LOG_FILE_PATH,REPORT_LOG_SIZE,REPORT_LOG_FILES,LOG_TO_CONSOLE)      
        logger_reports.info("**** reports script started ****")



        if ((b_date==None) or (e_date==None)):
            today=datetime.date.today()
            num_days=calendar.monthrange(today.year, today.month)[-1]
            first_day=datetime.datetime(today.year,today.month,1)
            last_day=datetime.datetime(today.year,today.month,num_days)

        else:
            first_day=b_date
            last_day=e_date

              
        for name in REPORT_DEVICE_LIST:
            reports(first_day,last_day,name)

        # purge old reports
        cleanup(DAYS_TO_KEEP_REPORTS,REPORT_LOCAL_FILE_PATH,"REPORTS","Reports")

        #purge old HDR files
        cleanup(DAYS_TO_KEEP_HDR,HDR_LOCAL_PATH,"REPORTS","HDR")

    except Exception:
        logger_reports.exception("!!! Exception Occured !!!!")

    else:
        logger_reports.info("**** report script finished ****\n")

    finally:
        logger_reports.handlers.pop()
        
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", type=datetime.datetime.fromisoformat, help="start date and time in YYYY-MM-DD HH:MM format")
    parser.add_argument("-e", type=datetime.datetime.fromisoformat, help="end date and time in YYYY-MM-DD HH:MM format")
    args = parser.parse_args()
    
    main(args.b,args.e)

     
