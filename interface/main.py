import PySimpleGUI as sg
import os.path

background = '#F0F0F0'
image_pause = './ButtonGraphics/pause.png'
image_restart = './ButtonGraphics/restart.png'
image_next = './ButtonGraphics/next.png'

# --------------------------------- Define Layout ---------------------------------

# First the window layout 2 columns

left_col = [[sg.Text('Dossier'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

''' TODO BOUCLE POUR LA PROGRESS BAR A REVOIR
for i in range(1000):
    # check to see if the cancel button was clicked and exit loop if clicked
    event, values = window.read(timeout=0)
    if event == 'Cancel' or event == sg.WIN_CLOSED:
        break
        # update bar with loop value +1 so that bar eventually reaches the maximum
    window['progbar'].update_bar(i + 1)
'''

#TODO Bloc pour video
videos_col = [[sg.Text(size=(15, 2), font=("Helvetica", 14), key='output')],
             [sg.Button('', button_color=(background,background),
                                image_filename=image_restart, image_size=(50, 50), image_subsample=2, border_width=0, key='Play'),
                                sg.Text(' ' * 2),
              sg.Button('', button_color=(background,background),
                                image_filename=image_pause, image_size=(50, 50), image_subsample=2, border_width=0, key='Stop'),
                                sg.Text(' ' * 2),
              sg.Button('', button_color=(background,background), image_filename=image_next, image_size=(50, 50), image_subsample=2, border_width=0, key='Next')]]

# ----- Full layout -----
layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(videos_col, element_justification='c')]]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Multiple Format Image Viewer', layout,resizable=True)

# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-FOLDER-':                         # Folder name was filled in, make a list of files in the folder
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)         # get list of files in folder
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".mov", ".mp4"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':    # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            if values['-W-'] and values['-H-']:
                new_size = int(values['-W-']), int(values['-H-'])
            else:
                new_size = None

            #TODO PRINT VIDEO 
            #window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))
        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename
# --------------------------------- Close & Exit ---------------------------------
window.close()