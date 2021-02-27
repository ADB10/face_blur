class SharedMemory:
    def __init__(self):
        self.deface_executing = False # floutage en cours ?
        self.progress = 0 # progress bar en %
        self.files_to_blur = 0 # nb de fichiers à flouter
        self.file_being_blur = 1 # numéro du fichier en train de se faire flouter
