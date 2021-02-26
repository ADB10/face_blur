import threading
#from main import App
from deface.centerface import CenterFace
from multiprocessing import Value
from deface.deface import *
import logging
from datetime import datetime
import time #a supprimer

class SharedMemory:
    def __init__(self):
        self.deface_executing = False # floutage en cours ?
        self.deface_finish = False # le floutage vient de se terminer ?
        self.progress = 0.0 # progress bar en %

logging.basicConfig(filename='logs.log', level=logging.DEBUG) #Create our logging file

def deface_file(self, video_path, output_folder, name, shared_mem):
    main_deface([video_path],output_folder,name, shared_mem)

class ThreadVideo : 
    def __init__(self, files_path,folder_path,folder_path_destination,name_blur,shared_mem ):
        self.files_path = files_path
        self.shared_mem = shared_mem
        self.folder_path = folder_path
        self.folder_path_destination = folder_path_destination
        self.name_blur = name_blur
        self.shared_memory = shared_mem

    def run_multiple(self) :
        self.shared_memory.deface_executing = True 
        nbthreads = len(self.files_path)
        threads = list()
        for index in range(nbthreads) :
            logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Creation d"un thread')
            self.files_path[index] = self.folder_path + '/' + self.files_path[index]
            x = threading.Thread(target=deface_file, args=(self,self.files_path[index],self.folder_path_destination, self.name_blur, self.shared_mem))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()
            logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Fin d"un thread')
        self.deface_finish()

    def run_simple(self) :
        self.shared_memory.deface_executing = True
        logging.info(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Creation d"un thread')
        x = threading.Thread(target=deface_file, args=(self,self.files_path,self.folder_path_destination, self.name_blur, self.shared_mem))
        x.start() #lancement du thread
        x.join() #attente fin du thread
        logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Fin d"un thread')
        self.deface_finish()

    def deface_finish(self):
        self.shared_memory.deface_executing = False
        self.shared_memory.deface_finish = True
        self.shared_memory.progress = 0.0
        