import os
import time
import logging
import configparser

def cleanup (number_of_days,root_path):

        time_in_secs = time.time()-(number_of_days * 24 * 60 * 60)

        for root, dirs, files in os.walk(root_path, topdown=False):
                for file_ in files:
                        full_path = os.path.join(root, file_)
                        stat = os.stat(full_path)
                        if stat.st_mtime <= time_in_secs:
                                os.remove(full_path)
                                print ("Removed file " +  file_ +" sucessfully")

def logger(file_name,message):    
        logging.basicConfig(filename=file_name,filemode='a',format='%(asctime)s,%(name)s %(levelname)s %(message)s',level=logging.DEBUG)
        logging.info(message)



if __name__ == '__main__':

        logger("test.log","This is a a test")
