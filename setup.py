import sys
from cx_Freeze import setup, Executable

from os.path import dirname

#### needed for ipython ########################
import zmq
import pygments
import scipy
#,'zmq.backend.cython','pygments.lexers.agile' 'pygments.styles.default''zmq.utils.garbage'
#################################################

includes = ['sys','PyQt5.QtCore','PyQt5.QtGui', 'PyQt5.QtWidgets','matplotlib', 'numpy', 'platform', 'struct', 'modules', 'os','re','copy','scipy','io','glob','PyQt5.QtSvg','zmq.backend.cython','pygments.lexers.agile','pygments.styles.default','zmq.utils.garbage','pathlib']
excludes = []
packages = []
path = []
base = None

########### scipy ##############
includefiles_list=[]
scipy_path = dirname(scipy.__file__)
includefiles_list.append(scipy_path)
#################################

#build_exe_options = {"excludes": ["tkinter"],
#                     "optimize": 2}

if sys.platform == 'win32':
    base = "Win32GUI"
    
options = {
    'build_exe': {
        "include_msvcr": True,
        "includes": includes,
        "excludes": excludes,
        "packages": packages,
        "path": path,
        'include_files': includefiles_list,
        #'include_files': [zmq.libzmq.__file__, ],
        # optimize: 2 breaks ipython support!!!!
        "optimize": 1
        #'excludes': ['Tkinter']  # Sometimes a little finetuning is needed
    }
}
executables = [Executable('qtnmr.py', base=base, icon = 'favicon2.ico')]
setup(name='QtNMR',
      version='0.1',
      description='QtNMR',
      executables=executables,
      options = options
#      options = {"build_exe": build_exe_options}
      )
