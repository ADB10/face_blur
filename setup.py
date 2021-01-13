from cx_Freeze import setup, Executable

base = None
executables = [Executable("monprogramme.py", base=base)]
packages = ["idna","opencv","tkinter"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "Floutage vidéo",
    options = options,
    version = "0.1",
    description = 'Floutage automatiques des visages sur une vidéo',
    executables = executables
)