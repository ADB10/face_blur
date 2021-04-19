import threading
from deface.centerface import CenterFace
from multiprocessing import Value, Process, Pipe
from multiprocessing import shared_memory, cpu_count
from deface.deface import *
import logging
from datetime import datetime
import os 
from multiprocessing import Pool

def cam_read_iter(reader):
    while True:
        yield reader.get_next_data()

def rotate_frame(frame, rotate):
    if(rotate == 90):
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif(rotate == -90) or (rotate == 270):
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif(rotate == 180):
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    return frame

def save_video(name,opath,ipath,rotate,extension,fps,shared_mem):
    shared_mem[0]=True
    root, ext = os.path.splitext(ipath) 
    osef, namepath = os.path.split(ipath)
    namepath,ext = os.path.splitext(namepath)
    ffmpeg_config = {'codec': 'libx264'}    

    if(name==None):
        if(extension==None):
            opath = opath + "/" + namepath + "_anonymized" + ext
        else:
            opath = opath + "/" + namepath + "_anonymized" + extension
    else:
        if(extension==None):
            opath = opath + "/" + name + ext
        else:
            opath = opath + "/" + name + extension

    if fps is None : #si les fps ne sont pas précisés 
        reader: imageio.plugins.ffmpeg.FfmpegFormat.Reader = imageio.get_reader(ipath) #on lit la video
        fps2 = reader.get_meta_data()['fps'] #on recup les fps
        reader: imageio.plugins.ffmpeg.FfmpegFormat.Reader = imageio.get_reader(ipath,fps=fps2) #on lit notre video en fps2, soit les fps normaux
    else : # si les fps sont précisés
        reader: imageio.plugins.ffmpeg.FfmpegFormat.Reader = imageio.get_reader(ipath)  #on lit la video
        fps2 = reader.get_meta_data()['fps'] #on recup les fps
        if(fps>int(fps2)): # si nb de fps specifié superieur a nb de fps de base
            reader: imageio.plugins.ffmpeg.FfmpegFormat.Reader = imageio.get_reader(ipath,fps=fps2) # on remets le nb de fps de base
        else:
            reader: imageio.plugins.ffmpeg.FfmpegFormat.Reader = imageio.get_reader(ipath,fps=fps) # sinon cest ok

    meta = reader.get_meta_data()
    nframes = reader.count_frames()

    if fps is None : #si les fps ne sont pas précisés 
        writer: imageio.plugins.ffmpeg.FfmpegFormat.Writer = imageio.get_writer(
                opath, format='FFMPEG', mode='I', fps=meta['fps'], **ffmpeg_config
            ) #on crée un fichier avec les fps par defaut
    else :
        if(fps>int(fps2)): # si nb de fps specifié superieur a nb de fps de base
            writer: imageio.plugins.ffmpeg.FfmpegFormat.Writer = imageio.get_writer(
                opath, format='FFMPEG', mode='I', fps=fps2, **ffmpeg_config
            ) #on crée un fichier avec les fps par defaut soit fp1
        else:
            writer: imageio.plugins.ffmpeg.FfmpegFormat.Writer = imageio.get_writer(
                opath, format='FFMPEG', mode='I', fps=fps, **ffmpeg_config
            )#sinon on crée un fichier avec les fps par voulu

    for frame in reader:
        frame = rotate_frame(frame,rotate) #on rotate s'il le faut
        writer.append_data(frame) # on met les images dans la video
        shared_mem[2] += (1/nframes)*100
    writer.close()

    shared_mem[0]= False
    shared_mem[1]=True
    shared_mem[2]=0.0
    shared_mem[4]=1
    shared_mem[3]=1

    return True

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

logging.basicConfig(filename=resource_path('logs.log'), level=logging.DEBUG) #Create our logging file

def deface_file(self, video_path, output_folder, name, extension, shared_mem):
    main_deface([video_path],output_folder,name, extension, shared_mem)

class ThreadVideo : 
    def __init__(self, files_path,folder_path,folder_path_destination,name_blur,extension,shared_mem):
        self.files_path = files_path
        self.folder_path = resource_path(folder_path)
        self.folder_path_destination = folder_path_destination
        self.name_blur = name_blur
        self.extension = extension
        self.shared_mem = shared_mem

    def run_multiple(self) :
        self.shared_mem[0]=True
        nbthreads = len(self.files_path)
        threads = list()
        procs = list()
        pool = multiprocessing.Pool()
        for index in range(nbthreads) :
            logging.info('Thread : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Creation d"un thread')
            self.files_path[index] = self.folder_path + '/' + self.files_path[index]
            proc = Process(target=deface_file, args=(self,self.files_path[index],self.folder_path_destination, self.name_blur, self.extension, self.shared_mem))
            procs.append(proc)
            proc.start()

        for index, proc in enumerate(procs):
            proc.join()
            logging.info('Process : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Fin d"un process')
        self.deface_finish()

    def run_simple(self) :
        self.shared_mem[0]=True
        logging.info(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Creation d"un process')
        p = Process(target=deface_file, args=(self,self.files_path,self.folder_path_destination, self.name_blur, self.extension, self.shared_mem))
        p.start() #lancement du process
        p.join() #attente fin du process
        logging.info('Process : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + 'Fin d"un process')
        self.deface_finish()

    def deface_finish(self):
        self.shared_mem[0]= False
        self.shared_mem[1]=True
        self.shared_mem[2]=0.0
        self.shared_mem[4]=1
        self.shared_mem[3]=1
        
