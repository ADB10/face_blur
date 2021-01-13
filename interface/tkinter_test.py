from tkinter import *
from tkinter.filedialog import askopenfilename

class Application:
    def __init__(self, master):
    
        def set_filename():
            file = askopenfilename(filetypes=FILETYPES)
            file = file.name
            filename.set(file)
                        
        frame = Frame(master)
        frame.pack()
        filez = askopenfilenames(parent=root,title='Choose a file')
        # OtherWidgetsHere
        
        btn_one = Button(master, text='Exit', command=quit)
        btn_one.pack(side=BOTTOM)

# GUI configurations
root = Tk()                # Parent Window
app = Application(root)    # Kickstart the main application
root.title('Title Here')   # Windows main title
root.minsize(300,300)      # Window default sizes
root.mainloop()            # Loop to display everything