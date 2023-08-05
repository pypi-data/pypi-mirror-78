import os, glob, time 
from .printer import printd
from .base import Base

class FileDaemon(Base):

    def __init__(self, indices=None):

        # --- Initialize
        self.load_configs()
        self.init_custom()

        printd('STARTING | {} (FileDaemon)'.format(self.name))

    def init_custom(self): pass

    def find_sources(self): 
        """
        Method to identify source directories for trigger search 

        """
        return ['/']

    def find_trigger(self, path):
        """
        Method to identify search string or list of potential files to check exists

        """
        return ['/']

    def exec_actions(self, paths):
        """
        Method to perform desired actions if trigger is found

        """
        pass

    def start(self, single_iteration=False):

        while True:

            # --- Identify source directories 
            paths = self.find_sources()

            for path in paths:

                # --- Identify triggers
                ts = self.find_trigger(path)

                assert type(ts) in [list, str]

                # --- Check exists
                if type(ts) is list:
                    paths = [t for t in ts if os.path.exists(t)]
                else:
                    paths = glob.glob(ts, recursive=True)
                
                # --- Perform actions if files found
                if len(paths) > 0:
                    self.exec_actions(paths)

            if single_iteration:
                break

            time.sleep(self.jhubd['refresh']['time-sleep'])
