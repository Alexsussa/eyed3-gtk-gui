import sys
import platform
from cx_Freeze import setup, Executable

def getOS():
    myOS = platform.system()
    if myOS == 'Linux':
        return 'eyed3gtk'
    elif myOS == 'Windows':
        return 'eyed3gtk.exe'
    else:
        return 'eyed3gtk.dmg'

build_exe_options = {'packages': ['gi'], 'excludes': [], 'includes': [], 'include_files': ['eyed3.ui', 'icons']}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(  name='eyeD3 Gtk Gui',
        version='0.2',
        description='Editor de tags de áudio baseado no eyeD3',
        author='Alex Pinheiro',
        options={'build_exe': build_exe_options},
        executables=[Executable('eyed3gtk.py', base=base, targetName=getOS())])
