import PySimpleGUI as sg
import os
import sys
import threading
import time
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import cv2
import logging
from thread_video.thread_video import ThreadVideo, SharedMemory
from datetime import datetime
from multiprocessing import Value
import json

from deface.centerface import CenterFace
from deface.deface import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

logging.basicConfig(filename=resource_path('logs.log'), level=logging.DEBUG) #Create our logging file
SHARED_MEMORY = SharedMemory()

class App:

    def __init__(self, folder_path_destination = None):

        DARK_BG = '#111'
        LIGHT_DARK_BG = '#333'
        WHITE_TEXT = '#fff'
        background = '#F0F0F0'
        background_not_usable = '#FF0000'

        image_pause = resource_path('./interface/ButtonGraphics/pause.png')
        image_restart = resource_path('./interface/ButtonGraphics/restart.png')
        image_next = resource_path('./interface/ButtonGraphics/next.png')
        image_previous = resource_path('./interface/ButtonGraphics/previous.png')
        image_rotate = resource_path('./interface/ButtonGraphics/rotate.png')

        deface_path = resource_path('./deface/deface.py')

        # ------ App states ------ #
        self.play = False  # Is the video currently playing?
        self.delay = 0.023  # Delay between frames - not sure what it should be, not accurate playback
        self.frame = 1  # Current frame
        self.frames = None  # Number of frames
        # ------ Other vars ------ #
        with open(resource_path('cache.json')) as json_file:
            self.cache = json.load(json_file)
        self.vid = None
        self.photo = None
        self.next = "1"
        self.video_path = None
        self.folder_path = self.cache["current_folder"]
        self.folder_path_destination = self.cache["destination_folder"]
        self.name_blur = None
        self.files_path = None # tous les path des videos du fichier
        self.blur_executing = False
        self.rotate_degree = 0
        self.app_starting = True
        self.extension = None

        # --------------------------------- Define Layout ---------------------------------

        # First the window layout 2 columns

        left_col = [
            [sg.FolderBrowse(button_text="Choisir le dossier des vidéos", target='-FOLDER_PATH-', initial_folder=self.cache["current_folder"],  button_color=(WHITE_TEXT, LIGHT_DARK_BG))],
            [sg.In(size=(60,1), default_text=self.cache["current_folder"], enable_events=True, background_color=LIGHT_DARK_BG, text_color=WHITE_TEXT, border_width=0, key='-FOLDER_PATH-')],
            [sg.Text('', size=(15, 2), background_color=DARK_BG)],
            [sg.Listbox(values=[], enable_events=True, size=(58,20), key='-FILE_LIST-')],
            [sg.Text('', size=(15, 2), background_color=DARK_BG)],
            [sg.FolderBrowse(button_text="Choisir le dossier de destination", target='-OUTPUT_FOLDER_PATH-', initial_folder=self.cache["destination_folder"], button_color=(WHITE_TEXT, LIGHT_DARK_BG))],
            [sg.In(size=(60,1), default_text=self.cache["destination_folder"], enable_events=True, background_color=LIGHT_DARK_BG, text_color=WHITE_TEXT, border_width=0, key='-OUTPUT_FOLDER_PATH-')],
            [sg.Text('', size=(15, 2), background_color=DARK_BG)],
            [sg.Text('Nom du fichier', size=(15, 1), background_color=DARK_BG, text_color=WHITE_TEXT), sg.InputText(size=(43,1))],
            [
                sg.Radio('avi', "1", enable_events=True, key='-AVI-',background_color=DARK_BG), 
                sg.Radio('mkv', "1", enable_events=True, key='-MKV-',background_color=DARK_BG),
                sg.Radio('mov', "1", enable_events=True, key='-MOV-',background_color=DARK_BG), 
                sg.Radio('mp4', "1", enable_events=True, key='-MP4-',background_color=DARK_BG)
            ],
            [sg.Text('', size=(15, 2), background_color=DARK_BG)],
            [
                sg.Button('Flouter la vidéo', enable_events=True, button_color=(WHITE_TEXT, LIGHT_DARK_BG), border_width=-1, key='-BLUR_VIDEO_BUTTON-'),
                sg.Button('Flouter le dossier', enable_events=True, button_color=(WHITE_TEXT, LIGHT_DARK_BG), border_width=-1, key='-BLUR_VIDEO_FOLDER_BUTTON-')
            ],
            [
                sg.Text('Il faut choisir une vidéo à flouter.', text_color="#AA0000", size=(60,1), background_color=DARK_BG, visible=False, key='-WARNING_VIDEO_PATH-'),
                sg.Text('Il faut choisir un dossier de destination.', text_color="#AA0000", size=(60,1), background_color=DARK_BG, visible=False, key='-WARNING_OUTPUT_FOLDER-'),
                sg.ProgressBar(100, orientation='h', size=(20, 20), visible=False, key='-PROGRESS_BAR-'),
                sg.Text(text='En cours de floutage... | 0%', text_color="#AA0000", size=(60,1), background_color=DARK_BG, visible=True, key='-LOADING_BLUR_VIDEO-')
            ]
        ]

        videos_col = [
            # [sg.Text(size=(15, 2), key='output')],
            [sg.Canvas(size=(500, 500), key="canvas", background_color="black")],
            [sg.Slider(size=(40, 20), range=(0, 100), resolution=1, key="slider", orientation="h", enable_events=True, background_color=(LIGHT_DARK_BG), border_width=0), sg.Text("", key="counter", background_color=DARK_BG, size=(10, 1))],
            [
                sg.Button(button_color=(WHITE_TEXT,DARK_BG), image_filename=image_previous, image_size=(50, 50), image_subsample=2, border_width=0, key='PREVIOUS_FRAME'),
                sg.Button(button_color=(WHITE_TEXT,DARK_BG), image_filename=image_restart, image_size=(50, 50), image_subsample=2, border_width=0, key='PLAY_BUTTON'),
                sg.Button(button_color=(WHITE_TEXT,DARK_BG), image_filename=image_next, image_size=(50, 50), image_subsample=2, border_width=0, key='NEXT_FRAME'),
                sg.Button(button_color=(WHITE_TEXT,DARK_BG), image_filename=image_rotate, image_size=(50, 50), image_subsample=2, border_width=0, key='ROTATE_VIDEO')
            ]
        ]

        # ----- Full layout -----
        layout = [[sg.Column(left_col, background_color=DARK_BG), sg.Column(videos_col, element_justification='c', background_color=DARK_BG)]]

        # --------------------------------- Create Window ---------------------------------
        self.window = sg.Window('BlurFace - Floutage de vidéo automatique', layout, resizable=True, background_color=DARK_BG).Finalize()

        # set return_keyboard_events=True to make hotkeys for video playback
        # Get the tkinter canvas for displaying the video
        canvas = self.window.Element("canvas")
        self.canvas = canvas.TKCanvas

        # Start video display thread
        self.load_video()

        # --------------------------------- Event Loop ---------------------------------
        while True:

            if SHARED_MEMORY.deface_executing:
                text_progress = "En cours de floutage... " + str(SHARED_MEMORY.file_being_blur) + "/"+ str(SHARED_MEMORY.files_to_blur) + " | " + str(round(SHARED_MEMORY.progress, 2)) + "%"
                self.window.Element("-LOADING_BLUR_VIDEO-").Update(visible=True)
                self.window.Element("-PROGRESS_BAR-").Update(visible=True, current_count=SHARED_MEMORY.progress)
                self.window.Element("-LOADING_BLUR_VIDEO-").Update(text_progress)
            else:
                if self.app_starting and self.folder_path != None: # affiche directement la liste des fichiers si presente dans le cache
                    self.define_files_list(None)
                if SHARED_MEMORY.deface_finish: # dans le cas ou une video vient de se faire flouter et quil faut actualiser le dossier courant
                    self.define_files_list(None)
                    SHARED_MEMORY.deface_finish = False 
                self.app_starting = False
                self.window.Element("-LOADING_BLUR_VIDEO-").Update(visible=False)
                self.window.Element("-PROGRESS_BAR-").Update(visible=False, current_count=0)
                self.window.Element("-BLUR_VIDEO_FOLDER_BUTTON-").Update(disabled=False)
                self.window.Element("-BLUR_VIDEO_BUTTON-").Update(disabled=False)
            
            event, values = self.window.Read(100)

            if event == sg.WIN_CLOSED or event == 'Exit':
                with open(resource_path('cache.json'), 'w') as outfile:
                    json.dump(self.cache, outfile)
                break

            if len(values[0]) > 0:
                self.name_blur = values[0]


            if event == '-FOLDER_PATH-':                         # Folder name was filled in, make a list of files in the folder
                self.define_files_list(values)

            if event == '-OUTPUT_FOLDER_PATH-':
                self.folder_path_destination = values['-OUTPUT_FOLDER_PATH-']
                self.cache["destination_folder"] = self.folder_path_destination

            if event == '-FILE_LIST-':    # A file was chosen from the listbox
                self.video_path = None
                try:
                    self.video_path =os.path.join(self.folder_path, values['-FILE_LIST-'][0])
                except AttributeError:
                    print("no video selected, doing nothing")
                if self.video_path:
                    # Initialize video
                    self.vid = MyVideoCapture(self.video_path)
                    # Calculate new video dimensions
                    self.vid_width = 960
                    self.vid_height = int(self.vid_width * self.vid.height / self.vid.width)
                    self.frames = int(self.vid.frames)
                    # Update slider to match amount of frames
                    self.window.Element("slider").Update(range=(0, int(self.frames)), value=0)
                    # Update right side of counter
                    self.window.Element("counter").Update("0/%i" % self.frames)
                    # change canvas size approx to video size
                    self.canvas.config(width=self.vid_width, height=self.vid_height)
                    # Reset frame count
                    self.frame = 0
                    self.delay = 1 / self.vid.fps
                    # Update the video path text field
                    self.window.Element("-FOLDER_PATH-").Update(self.video_path)
            

            if event == "-BLUR_VIDEO_BUTTON-":
                if self.video_path != None:
                    if self.folder_path_destination != None:
                        #Lance le deface dans un thread particulier
                        logging.info('Main : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' : Creation de l\'objet thread pour le floutage d\'une video, dans le main')
                        curr_thread = ThreadVideo(self.video_path,self.folder_path,self.folder_path_destination,self.name_blur,SHARED_MEMORY, self.extension) #création de l'objet
                        x = threading.Thread(target=curr_thread.run_simple, args=()) #creation du thread executant la fonction run de notre objet
                        x.start() #excution du thread
                        self.window.Element("-BLUR_VIDEO_BUTTON-").Update(disabled=True) #update les boutons
                        self.window.Element("-BLUR_VIDEO_FOLDER_BUTTON-").Update(disabled=True) 
                        self.window.Element("-WARNING_OUTPUT_FOLDER-").Update(visible=False)
                        self.window.Element("-WARNING_VIDEO_PATH-").Update(visible=False)
                    else:
                        self.window.Element("-WARNING_OUTPUT_FOLDER-").Update(visible=True)
                        self.window.Element("-WARNING_VIDEO_PATH-").Update(visible=False)
                else:
                    self.window.Element("-WARNING_VIDEO_PATH-").Update(visible=True)
            
            if event == "-BLUR_VIDEO_FOLDER_BUTTON-" and not self.blur_executing:
                if self.files_path != None:
                    if self.folder_path_destination != None:
                        logging.info('Main : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' : Creation de l\'objet thread pour le floutage de plusieurs video, dans le main')
                        curr_thread = ThreadVideo(self.files_path,self.folder_path,self.folder_path_destination,None,SHARED_MEMORY, self.extension) #création de l'objet
                        x = threading.Thread(target=curr_thread.run_multiple, args=()) #creation du thread executant la fonction run de notre objet
                        SHARED_MEMORY.files_to_blur = len(self.files_path)
                        x.start() #excution du thread
                        self.window.Element("-BLUR_VIDEO_FOLDER_BUTTON-").Update(disabled=True) #update les boutons
                        self.window.Element("-BLUR_VIDEO_BUTTON-").Update(disabled=True)
                        self.window.Element("-WARNING_OUTPUT_FOLDER-").Update(visible=False)
                        self.window.Element("-WARNING_VIDEO_PATH-").Update(visible=False)
                    else:
                        self.window.Element("-WARNING_OUTPUT_FOLDER-").Update(visible=True)
                        self.window.Element("-WARNING_VIDEO_PATH-").Update(visible=False)
                else:
                    self.window.Element("-WARNING_VIDEO_PATH-").Update(visible=True)

            

            if event == "PLAY_BUTTON" and self.video_path:
                if self.play:
                    self.play = False
                    #self.window.Element("PLAY_BUTTON").Update("Play")
                    self.window.Element("PLAY_BUTTON").Update(button_color=(WHITE_TEXT,DARK_BG), image_filename=image_restart, image_size=(50, 50), image_subsample=2)
                else:
                    self.play = True
                    #self.window.Element("PLAY_BUTTON").Update("Pause")
                    self.window.Element("PLAY_BUTTON").Update(button_color=(WHITE_TEXT,DARK_BG), image_filename=image_pause, image_size=(50, 50), image_subsample=2)

            if event == 'NEXT_FRAME' and self.video_path:
                # Jump forward a frame TODO: let user decide how far to jump
                if self.frame != self.frames :
                    self.set_frame(self.frame + 1)

            if event == 'PREVIOUS_FRAME' and self.video_path:
                # Jump forward a frame TODO: let user decide how far to jump
                if self.frame != 0 :
                    self.set_frame(self.frame - 1)

            if event == 'ROTATE_VIDEO' and self.video_path:
                self.rotate_degree = (self.rotate_degree + 90) % 360

            if event =='-AVI-':
                self.extension = ".avi"
            if event =='-MKV-':
                self.extension = ".mkv"
            if event =='-MOV-':
                self.extension = ".mov"
            if event =='-MP4-': 
                self.extension = ".mp4"

            if event == "slider":
                # self.play = False
                self.set_frame(int(values["slider"]))
                # print(values["slider"])
        # --------------------------------- Close & Exit ---------------------------------
        self.window.Close()
        sys.exit()


    # affiche les files dans la listbox
    def define_files_list(self, values):
        if not self.app_starting and not SHARED_MEMORY.deface_finish:
            self.folder_path = values['-FOLDER_PATH-']
            self.cache["current_folder"] = values['-FOLDER_PATH-']
        try:
            file_list = os.listdir(self.folder_path)         # get list of files in folder
        except:
            file_list = []
        self.files_path = [f for f in file_list if os.path.isfile(
            os.path.join(self.folder_path, f)) and f.lower().endswith((".mov", ".mp4", ".mkv",".avi"))]
        self.window['-FILE_LIST-'].update(self.files_path)



    #################
    # Video methods #
    #################
    def load_video(self):
        """Start video display in a new thread"""
        thread = threading.Thread(target=self.update, args=())
        thread.daemon = 1
        thread.start()

    def update(self):
        """Update the canvas element with the next video frame recursively"""
        start_time = time.time()
        if self.vid:
            if self.play:
                # Get a frame from the video source only if the video is supposed to play
                ret, frame = self.vid.get_frame()
                
                if ret:
                    self.photo = PIL.ImageTk.PhotoImage(
                        image=PIL.Image.fromarray(frame).resize((self.vid_width, self.vid_height), Image.NEAREST)
                    )
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                    if(self.rotate_degree!=0):
                        frame = cv2.rotate(frame, self.rotate_degree)

                    self.frame += 1
                    self.update_counter(self.frame)

            # Uncomment these to be able to manually count fps
            # print(str(self.next) + " It's " + str(time.ctime()))
            # self.next = int(self.next) + 1
        # The tkinter .after method lets us recurse after a delay without reaching recursion limit. We need to wait
        # between each frame to achieve proper fps, but also count the time it took to generate the previous frame.
        self.canvas.after(abs(int((self.delay - (time.time() - start_time)) * 1000)), self.update)

    def set_frame(self, frame_no):
        """Jump to a specific frame"""
        if self.vid:
            # Get a frame from the video source only if the video is supposed to play
            ret, frame = self.vid.goto_frame(frame_no)
            self.frame = frame_no
            self.update_counter(self.frame)

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(
                    image=PIL.Image.fromarray(frame).resize((self.vid_width, self.vid_height), Image.NEAREST))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def update_counter(self, frame):
        """Helper function for updating slider and frame counter elements"""
        self.window.Element("slider").Update(value=frame)
        self.window.Element("counter").Update("{}/{}".format(frame, self.frames))


class MyVideoCapture:
    """
    Defines a new video loader with openCV
    Original code from https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
    Modified by me
    """
    def __init__(self, video_source):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        """
        Return the next frame
        """
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return 0, None
    def goto_frame(self, frame_no):
        """
        Go to specific frame
        """
        if self.vid.isOpened():
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)  # Set current frame
            ret, frame = self.vid.read()  # Retrieve frame
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return 0, None
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == '__main__':
    App()
