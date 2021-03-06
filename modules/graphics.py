import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use('qt5agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# uncomment for matlibplot standard cursor-also in code
#from matplotlib.widgets import Cursor
#import matplotlib.pyplot as plt
import modules.plot_tools as plot_tools
from matplotlib.figure import Figure


class Widgetmain(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widgetmain, self).__init__(parent)

        self.figure = Figure()

        #plt.subplots_adjust(left=0.031, right=0.999, top=0.99, bottom=0.03)
        #plt.subplots_adjust(left=0.001, right=0.999, top=0.999, bottom=0.001)

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        #uncomment for disabling plot toolbar, not recommended
        self.toolbar.hide()

        # set the layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        # set the plot class handlers
        self.wzoom = plot_tools.WheellZoom()
        self.adapt = plot_tools.WindowResize() #keep tight layout
        self.cursor = plot_tools.SnaptoCursor()
        self.selector = plot_tools.Select()
        self.selection = plot_tools.Selection()
        self.dataplot = None


    def setStatus(self,stat):
        self.statusbar = stat

    def save_plot(self):
        self.toolbar.save_figure()

    def axis_configure(self):
        self.toolbar.edit_parameters()


    def plot(self, xaxis=None, real=None , imag=None,
             magn=None, hxlimit=None, lxlimit=None, datas=None):

        #self.dataplot.clear()
        #if self.dataplot:
        # self.figure.delaxes(self.dataplot)
        if self.dataplot is None:
             self.dataplot = self.figure.add_subplot(111)
             self.figure.patch.set_facecolor('white')
             self.selector.setAx(self.dataplot, hxlimit, lxlimit, xaxis.size, datas, self.selection)

        #self.dataplot = self.figure.add_subplot(111)
        #self.selector.setAx(self.dataplot, hxlimit, lxlimit, xaxis.size, datas, self.selection)
        self.statusbar.showMessage("Plot updated")
        self.dataplot.hold(False)
        self.dataplot.plot(xaxis , real , 'r-', xaxis , imag , 'g-',  xaxis , magn , '-')

        # uncomment for matlibplot standard cursor
        #cursor = Cursor(dataplot, useblit=True, color='black', linewidth=1 )

        self.wzoom.setAx(self.dataplot, self.selection, datas)
        self.cursor.setAx(datas, self.dataplot, xaxis, real, self.statusbar)
        self.adapt.setAx(self.dataplot,self.figure)
        self.selection.setAx(self.dataplot, datas)

        self.figure.tight_layout()

        # dataplot.set_autoscaley_on(False) for auto x scale

        # setting background color
        #self.figure.patch.set_visible(False)
        #self.figure.patch.set_facecolor('white')

        self.dataplot.set_xlim([lxlimit, hxlimit])

        # uncomment the following line for raw axis label inside plot
        # self.dataplot.tick_params(direction='in', pad=-19)

        # uncomment the following lines to disable plot toolbar mouse coordinates
        #def format_coord(x, y):
        #    return ' '
        #self.dataplot.format_coord = format_coord


        self.canvas.draw()
