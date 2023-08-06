import platform
import os
import subprocess
import xl2dict
from logging import getLogger

logger = getLogger("pyC")

def open(filenameAndPath: str):
    """Will open the given file with the Operating system default program.

    param

    filenameAndPath : Complete absolute path to file.
    return : True if sucessfully open. False if file doesn't exists or operating system doesn't have default program.
    """

    if not isinstance(filenameAndPath, str):
        filenameAndPath = str(filenameAndPath)

    filenameAndPath = os.path.abspath(filenameAndPath)
    logger.debug(f"Trying to open file with it's application: {filenameAndPath}")

    if not os.path.exists(filenameAndPath):
        logger.warning(f"Filename doesn't exist and can't be opened: {filenameAndPath}")
        return False

    elif platform.system().lower() == "windows":
        try:
            filenameAndPath = f'"{filenameAndPath}"'
            os.startfile(filenameAndPath)
            return True
        except Exception as errorcode:
            if errorcode.errno == 22:
                os.popen(r"Rundll32.exe SHELL32.DLL, OpenAs_RunDLL "+filenameAndPath)
                return True
            else:
                return False

    elif platform.system().lower() == "linux":
        logger.debug(f"In Linux trying to call xdg-open with filename: {str(filenameAndPath)}")
        status = subprocess.call(["xdg-open", str(filenameAndPath)])
        if status == 0:
            return True
        else:
            return False

    elif platform.system().lower() == "darwin":
        filenameAndPath = f'"{filenameAndPath}"'
        status = os.system("open " + str(filenameAndPath))
        if status == 0:
            return True
        else:
            return False


class FilesOpen:
    """
    Class is called from UI and will open the corresponding file-type in the os-specific application.
    """
    def __init__(self):
        pass

    @staticmethod
    def openResultFile(filenameAndPath):
        return open(filenameAndPath=filenameAndPath)
