import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from detection_custom import detectInput

#from fbs_runtime.application_context.PyQt5 import ApplicationContext

class SDVD_GUI(QMainWindow):
    """View|Window of SDVD_GUI."""

    def __init__(self):
        """Initializer"""
        super().__init__()
        self.fname = ""
        self.saveFname = ""
        self.showConfidence = False
        self.showViolationOnly = False

        #top level window properties
        self.setWindowTitle("Social Distancing Violation Detector")
        self.setGeometry(50, 50, 320, 640)

        #init GUI window
        self.window = QWidget()

        #init QGridLayout
        self.layout = QVBoxLayout()

        #select file ; turns to image after image selected
        self.lImg = QLabel("<center><b>Select an Image/Video</b></center>")
        self.layout.addWidget(self.lImg)

        #display path to selected image if image selected
        self.la = QLabel("")
        self.layout.addWidget(self.la)

        #Open File button
        self.btnOpenFile = QPushButton('Open File')
        self.btnOpenFile.clicked.connect(self.openFileNameDialog)
        self.layout.addWidget(self.btnOpenFile)

        #start analyze img/vid button
        self.btnAnalzye = QPushButton('Analyze')
        self.btnAnalzye.clicked.connect(self.checkInput)
        self.layout.addWidget(self.btnAnalzye)

        #set QGridLayout to window(QtWidget)
        self.window.setLayout(self.layout)

        #make window as central widget for Main window
        self.setCentralWidget(self.window)
        #create a Main window toolbar
        self._createToolBar()
        #create a bottom status bar for main window
        self._createStatusBar()

    def _createToolBar(self):
        tools = QToolBar()

        #add toolbar to right side of window
        self.addToolBar(Qt.RightToolBarArea, tools)

        self.saveCheckBox = QCheckBox("Save \nAnalyzed")
        tools.addWidget(self.saveCheckBox)

        self.showConfidenceCheckBox = QCheckBox("Show \nConfidence")
        tools.addWidget(self.showConfidenceCheckBox)

        self.onlyViolatedCheckBox = QCheckBox("Show \nViolation Only")
        tools.addWidget(self.onlyViolatedCheckBox)

    def _createStatusBar(self):
        self.status = QStatusBar()

        #set color
        self.status.setStyleSheet("color : red")

        #set msg to be shown
        self.status.showMessage("Not Ready. Open a File")
        self.setStatusBar(self.status)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","Image/Video files (*.jpg *.jpeg *mp4 *avi)", options=options)

        if fileName:
            #open selected img as QPixmap
            pix = QPixmap(fileName)
            #scaled photo keeping aspect ratio
            pix = pix.scaled(960, 540, Qt.KeepAspectRatio)
            #change the lImg label to show chosen img
            self.lImg.setPixmap(pix)
            #change la label to path of the selected img
            self.la.setText(fileName)
            #change status bar to Ready after file is selected
            self.status.showMessage("Ready. Click on Analyze to start")
            #set staus bar txt color
            self.status.setStyleSheet("color : lightgreen")
            #change the fname to store path to file
            self.fname = fileName

    def checkInput(self):
        self.chkBoxState()

        if self.fname == "":
            alert = QMessageBox()
            alert.setText("Please select an image or video to analyze")
            alert.exec()
        else:
            self.status.showMessage("Running Inference...")
            self.status.setStyleSheet("color : white; background-color : lightgreen; font-weight : bold")
            qApp.processEvents()

            #Run inference
            image = detectInput(self.fname, self.saveFname, self.showConfidence, self.showViolationOnly)
            image = QImage(image, image.shape[1],image.shape[0], image.shape[1] * 3,QImage.Format_RGB888).rgbSwapped()
            image = QPixmap(image)
            image = image.scaled(960, 540, Qt.KeepAspectRatio)
            self.lImg.setPixmap(image)

            #set status back to ready after inference completed
            self.status.showMessage("Inference completed.")
            self.status.setStyleSheet("color : lightgreen")

    def chkBoxState(self):
        if (self.saveCheckBox.isChecked() == True):
            splitedFname = self.fname.split("/")
            splitedFname = splitedFname[-1].split(".")
            self.saveFname = "./IMAGES/" + str(splitedFname[0]) + "_Analyzed." + str(splitedFname[-1])
        else:
            self.saveFname = ""

        if (self.showConfidenceCheckBox.isChecked() == True):
            self.showConfidence =  True
        else:
            self.showConfidence = False

        if (self.onlyViolatedCheckBox.isChecked() == True):
            self.showViolationOnly = True
        else:
            self.showViolationOnly = False

def main():
    """Main"""
    # Create an instance of QApplication
    SDVD = QApplication(sys.argv)
    SDVD.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)

    SDVD.setPalette(palette)
    # Show the SDVC GUI
    view = SDVD_GUI()
    view.show()
    # Execute the SDVC's main loop
    sys.exit(SDVD.exec())

if __name__ == '__main__':
    main()
