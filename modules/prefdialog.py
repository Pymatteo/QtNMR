from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class prefDlg(QtWidgets.QDialog):

    def __init__(self, parent=None, data=None):
        super(prefDlg, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.data = data
        self.previous = 0
        self.LB_previous = self.data.getLB()

        square_Label = QtWidgets.QLabel('Square Apod. : ')
        square_Spinbox = QtWidgets.QSpinBox()
        squareapod_CheckBox = QtWidgets.QCheckBox("Fix")
        squareapod_CheckBox.setChecked(self.data.getSqrApodBool())
        squareapod_CheckBox.stateChanged.connect(self.data.setSqrApodBool)
        square_Spinbox.setRange(0, self.data.get1dpoints())
        square_Spinbox.valueChanged.connect(self.data.setSqrShift)
        square_Spinbox.setValue(self.data.getSqrShift())
        #square_Spinbox.setRange(1, 10000)

        leftShift_Label = QtWidgets.QLabel('Left shift: ')
        leftShift_Spinbox = QtWidgets.QSpinBox()
        leftShift_CheckBox = QtWidgets.QCheckBox("Fix")
        leftShift_CheckBox.setChecked(self.data.getLeftShiftBool())
        leftShift_CheckBox.stateChanged.connect(self.data.setLeftShiftBool)
        leftShift_Spinbox.setRange(0, self.data.get1dpoints())
        leftShift_Spinbox.valueChanged.connect(self.data.setLeftShift)
        leftShift_Spinbox.setValue(self.data.getLeftShift())

        timer_Label = QtWidgets.QLabel('Script Timer Interval (seconds): ')
        timer_Spinbox = QtWidgets.QSpinBox()
        timer_Spinbox.setRange(0, 90000)
        timer_Spinbox.valueChanged.connect(self.timer_set)
        timer_Spinbox.setValue(self.data.getTimerInterval()/1000)


        threshold_Label = QtWidgets.QLabel('Threshold for echo selection: ')
        threshold_Spinbox = QtWidgets.QDoubleSpinBox()
        threshold_Spinbox.setRange(0, 90000)
        threshold_Spinbox.valueChanged.connect(self.threshold_set)
        threshold_Spinbox.setValue(self.data.getThreshold())

        LB_Spinbox = QtWidgets.QSpinBox()
        LB_Spinbox.setMinimum(0)
        LB_Spinbox.setMaximum(100000)
        LB_Spinbox.setValue(self.data.getLB())
        LB_Label = QtWidgets.QLabel('Exponential LB: ')
        phaseLabel = QtWidgets.QLabel('Phase: ')
        phase_Spinbox = QtWidgets.QSpinBox()
        phase_Spinbox.setRange(0, 360)
        #phaseLabel.setBuddy(self.spinbox)
        dial = QtWidgets.QDial()
        dial.setNotchesVisible(True)
        dial.setSingleStep(20)
        dial.setMinimum(0)
        dial.setMaximum(360)
        line = QtWidgets.QFrame()
        line2 = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line2.setFrameShape(QtWidgets.QFrame.HLine)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|
                                     QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setAutoDefault

        layout = QtWidgets.QGridLayout()
        layout.setHorizontalSpacing(9)
        layout.setVerticalSpacing(9)
        layout.addWidget(phaseLabel, 0, 0)
        layout.addWidget(dial, 0, 1)
        layout.addWidget(phase_Spinbox, 0, 2)
        layout.addWidget(line, 1, 0, 1, 3)
        layout.addWidget(LB_Label, 2, 0)
        layout.addWidget(LB_Spinbox, 2, 1)
        layout.addWidget(square_Label, 3, 0)
        layout.addWidget(square_Spinbox, 3, 1)
        layout.addWidget(squareapod_CheckBox, 3, 2)
        layout.addWidget(leftShift_Label, 4, 0)
        layout.addWidget(leftShift_Spinbox, 4, 1)
        layout.addWidget(leftShift_CheckBox, 4, 2)
        layout.addWidget(threshold_Label, 5, 0)
        layout.addWidget(threshold_Spinbox, 5, 1)
        layout.addWidget(line2, 6, 0, 1, 3)
        layout.addWidget(timer_Label, 7, 0)
        layout.addWidget(timer_Spinbox, 7, 1)
        layout.addWidget(buttonBox, 8, 1, 1, 2)
        self.setLayout(layout)
        phase_Spinbox.valueChanged.connect(dial.setValue)
        dial.valueChanged.connect(phase_Spinbox.setValue)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        phase_Spinbox.valueChanged.connect(self.phase)
        LB_Spinbox.valueChanged.connect(self.lbroad)

        self.setWindowTitle("Preferences")

    @QtCore.pyqtSlot(int)
    def phase(self,angle):
        print(self.previous)
        angle = angle - self.previous
        self.previous = angle + self.previous
        self.data.phase(angle)
        print(angle)

    def lbroad(self,LB):
        self.data.setLB(LB)

    def timer_set(self,timer_interval):
        self.data.setTimerInterval(timer_interval*1000)

    def threshold_set(self,threshold):
        self.data.setThreshold(threshold)

    def result(self):
        return 'ok'

    def nonaccpted(self):
        self.phase(0)
        self.lbroad(self.LB_previous)

        return 'not'


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    form = prefDlg()
    form.show()
    app.exec_()
