import PySimpleGUI as sg
import os
import sys
import threading
import time
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import cv2

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App:
    def __init__(self):
        background = '#F0F0F0'
        image_pause = resource_path('./interface/ButtonGraphics/pause.png')
        image_restart = resource_path('./interface/ButtonGraphics/restart.png')
        image_next = resource_path('./interface/ButtonGraphics/next.png')
        deface_path = resource_path('./deface/deface.py')

        # ------ App states ------ #
        self.play = True  # Is the video currently playing?
        self.delay = 0.023  # Delay between frames - not sure what it should be, not accurate playback
        self.frame = 1  # Current frame
        self.frames = None  # Number of frames
        # ------ Other vars ------ #
        self.vid = None
        self.photo = None
        self.next = "1"
        self.video_path = None
        self.folder_path = None

        # --------------------------------- Define Layout ---------------------------------

        # First the window layout 2 columns

        left_col = [[sg.Text('Dossier'), sg.In(size=(25,1), enable_events=True ,key='_FILEPATH_'), sg.FolderBrowse()],
                    [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
                    [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
                    [sg.Button('Flouter la vidéo', enable_events=True, key='BLUR_VIDEO_BUTTON'), sg.Button('Flouter le dossier', enable_events=True, key='BLUR_VIDEO_FOLDER_BUTTON')]]

        videos_col = [[sg.Text(size=(15, 2), font=("Helvetica", 14), key='output')],
                    [sg.Canvas(size=(500, 500), key="canvas", background_color="black")],
                    [sg.Slider(size=(30, 20), range=(0, 100), resolution=100, key="slider", orientation="h",
                                    enable_events=True), sg.T("0", key="counter", size=(10, 1))],
                    [sg.Button('', button_color=(background,background),
                                        image_filename=image_restart, image_size=(50, 50), image_subsample=2, border_width=0, key='PLAY_BUTTON'),
                                        sg.Text(' ' * 2),
                    sg.Button('', button_color=(background,background), image_filename=image_next, image_size=(50, 50), image_subsample=2, border_width=0, key='Next')]]

        # ----- Full layout -----
        layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(videos_col, element_justification='c')]]

        # --------------------------------- Create Window ---------------------------------
        self.window = sg.Window('Floutage de vidéo automatique', layout,resizable=True).Finalize()

        # set return_keyboard_events=True to make hotkeys for video playback
        # Get the tkinter canvas for displaying the video
        canvas = self.window.Element("canvas")
        self.canvas = canvas.TKCanvas

        # Start video display thread
        self.load_video()

        # --------------------------------- Event Loop ---------------------------------
        while True:
            event, values = self.window.Read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == '_FILEPATH_':                         # Folder name was filled in, make a list of files in the folder
                self.folder_path = values['_FILEPATH_']
                print(self.folder_path)
                try:
                    file_list = os.listdir(self.folder_path)         # get list of files in folder
                except:
                    file_list = []
                fnames = [f for f in file_list if os.path.isfile(
                    os.path.join(self.folder_path, f)) and f.lower().endswith((".mov", ".mp4", ".mkv"))]
                self.window['-FILE LIST-'].update(fnames)
            elif event == '-FILE LIST-' and len(values['-FILE LIST-']) > 0:    # A file was chosen from the listbox
                self.video_path = None
                try:
                    self.video_path =os.path.join(self.folder_path, values['-FILE LIST-'][0])
                except AttributeError:
                    print("no video selected, doing nothing")
                if self.video_path:
                    self.window.Element("PLAY_BUTTON").Update(button_color=(background,background), image_filename=image_pause, image_size=(50, 50), image_subsample=2)
                    print(self.video_path)
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
                    self.window.Element("_FILEPATH_").Update(self.video_path)
            
            if event == "BLUR_VIDEO_BUTTON" and self.video_path != None:
                # Il existe sans doute un facon BIEN MEILLEURE pour faire ça
                sg.popup_get_folder('Dossier de destination des vidéos floutés :', title='Floutage', default_path = self.video_path)
                os.system("python3 " + deface_path + " " + self.video_path)
            
            if event == "BLUR_VIDEO_FOLDER_BUTTON" and self.folder_path != None:
                sg.popup_get_folder('Dossier de destination des vidéos floutés :', title='Floutage', default_path = self.video_path)
                os.system("python3 " + deface_path + " " + self.folder_path + "/*.mp4")

            if event == "PLAY_BUTTON" and self.video_path:
                if self.play:
                    self.play = False
                    #self.window.Element("PLAY_BUTTON").Update("Play")
                    self.window.Element("PLAY_BUTTON").Update(button_color=(background,background), image_filename=image_restart, image_size=(50, 50), image_subsample=2)
                else:
                    self.play = True
                    #self.window.Element("PLAY_BUTTON").Update("Pause")
                    self.window.Element("PLAY_BUTTON").Update(button_color=(background,background), image_filename=image_pause, image_size=(50, 50), image_subsample=2)

            if event == 'Next frame':
                # Jump forward a frame TODO: let user decide how far to jump
                self.set_frame(self.frame + 1)

            if event == "slider":
                # self.play = False
                self.set_frame(int(values["slider"]))
                # print(values["slider"])
        # --------------------------------- Close & Exit ---------------------------------
        self.window.Close()
        sys.exit()



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
