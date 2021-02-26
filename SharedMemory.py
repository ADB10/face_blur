class SharedMemory:
    def __init__(self):
        self.deface_executing = False # floutage en cours ?
        self.progress = 0 # progress bar en %
