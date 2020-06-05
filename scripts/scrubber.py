import os
import time

def cleanup (number_of_days,path):

        time_in_secs = time.time()-(number_of_days * 24 * 60 * 60)

        for root, dirs, files in os.walk(path, topdown=False):
                for file_ in files:
                        full_path = os.path.join(root, file_)
                        stat = os.stat(full_path)
                        if stat.st_mtime <= time_in_secs:
                                os.remove(full_path)
                                print ("Removed file " +  file_ +" sucessfully")




        
        
