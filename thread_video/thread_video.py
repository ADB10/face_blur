import threading
#from main import App
from deface.centerface import CenterFace
from multiprocessing import Value
from deface.deface import *
import logging
from datetime import datetime

import time #a supprimer

logging.basicConfig(filename='logs.log', level=logging.DEBUG) #Create our logging file

def deface_file(self,video_path,output_folder,name):
    main_deface([video_path],output_folder,name)

class ThreadVideo : 
    def __init__(self, files_path,folder_path,folder_path_destination,name_blur,shared_mem ):
        self.files_path = files_path
        self.shared_mem = shared_mem
        self.folder_path = folder_path
        self.folder_path_destination = folder_path_destination
        self.name_blur = name_blur
        self.existing_shm = shared_mem

    def run_multiple(self) :
        self.existing_shm.value = 1 #variable partagé à vrai
        nbthreads = len(self.files_path)
        threads = list()
        for index in range(nbthreads) :
            logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Creation d"un thread')
            self.files_path[index] = self.folder_path + '/' + self.files_path[index]
            x = threading.Thread(target=deface_file, args=(self,self.files_path[index],self.folder_path_destination, self.name_blur))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()
            logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Fin d"un thread')
        self.existing_shm.value = 0 #variable partagé à faux

    def run_simple(self) :
        self.existing_shm.value = 1 #variable partagé à vrai
        logging.info(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Creation d"un thread')
        x = threading.Thread(target=deface_file, args=(self,self.files_path,self.folder_path_destination, self.name_blur))
        x.start() #lancement du thread
        x.join() #attente fin du thread
        logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Fin d"un thread')
        self.existing_shm.value = 0 #variable partagé à 0
        