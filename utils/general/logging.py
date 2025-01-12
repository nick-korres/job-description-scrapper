import os
from utils.general.load_env import app_settings

class PinnedLog:
    def __init__(self):
        self.pinned_log = []
        self.delimiter = "\n----------------------------------------\n"

    def clear_log(self,clean_pinned = False):
    # In debug mode we dont want to clear the log
        if app_settings["debug"]: return
        if os.name == 'nt':
            os.system('cls')  # Windows
        else:
            os.system('clear')  # Unix/Linux/Mac
    # If there are pinned logs print them after clearing
        if clean_pinned:
            self.pinned_log = []
        else:
            print(self.delimiter.join(self.pinned_log))

    def print_pin(self,msg:str,append = True):
        if append:
            self.pinned_log.append(msg)
        else:
            self.pinned_log = [msg]
        print(msg)

logger = PinnedLog()


