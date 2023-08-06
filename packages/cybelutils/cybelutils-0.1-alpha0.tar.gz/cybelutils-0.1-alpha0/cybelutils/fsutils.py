import glob
import os


class fsutils:

    def __init__(self):
        return

    def lastfile(self, path):
        list_of_files = glob.glob(path)
        lastfile = None
        try:
            lastfile = max(list_of_files, key=os.path.getctime)
        except:
            pass
        return lastfile

    def renamelastfile(self, path, filter, newname):
        os.rename(self.lastfileastfile(path + filter), path + '\\' + newname)
