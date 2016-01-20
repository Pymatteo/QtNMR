from PyQt5 import QtCore, QtGui, QtWidgets


class prefDlg(QtWidgets.QDialog):

    def __init__(self, parent=None, data=None):
        super(prefDlg, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.data = data
        self.previous = 0
        
        square_Label = QtWidgets.QLabel('Square Apod. : ')
        square_Spinbox = QtWidgets.QSpinBox()
        #square_Spinbox.setRange(1, 10000)
        leftShift_Label = QtWidgets.QLabel('Square Apod. : ')
        leftShift_Spinbox = QtWidgets.QSpinBox()
        LB_Spinbox = QtWidgets.QSpinBox()
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
        line.setFrameShape(QtWidgets.QFrame.HLine)
        

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
        layout.addWidget(leftShift_Label, 4, 0)
        layout.addWidget(leftShift_Spinbox, 4, 1)
        layout.addWidget(buttonBox, 6, 1, 1, 2)
        self.setLayout(layout)
        phase_Spinbox.valueChanged.connect(dial.setValue)
        dial.valueChanged.connect(phase_Spinbox.setValue)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        phase_Spinbox.valueChanged.connect(self.phase)

        self.setWindowTitle("Preferences")

    @QtCore.pyqtSlot(int)
    def phase(self,angle):
        print(self.previous)
        angle = angle - self.previous
        self.previous = angle + self.previous
        self.data.phase(angle)
        print(angle)
        

    def result(self):
        return 'ok'


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = prefDlg()
    form.show()
    app.exec_()

