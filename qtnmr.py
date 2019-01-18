#!/usr/bin/python3
import os
import platform
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import modules.main_window as main_window
import modules.qrc_resources

os.environ['PYZMQ_BACKEND'] = 'cython'

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Universita di Pavia - Dip. di Fisica - NMR group")
    app.setOrganizationDomain("arturo.unipv.it")
    app.setApplicationName("QtNMR")
    app.setWindowIcon(QtGui.QIcon(':/icon.png'))

    main = main_window.MainWindow()

    # on resize event added as a workaround
    # for Windows visualization (black bands)
    def onResize(event):
        main.update()

    print(sys.argv, len(sys.argv))
    main.setWindowTitle('QtNMR')
    main.resizeEvent = onResize

    #print(os.path.dirname(__file__))
    main.show()
    #main.showFullScreen()
    #main.showMaximized()
    sys.exit(app.exec_())
