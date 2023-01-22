'''
    Four lane lap counter and lap timer
    
    Main widget

'''
import sys

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from RacersSettings import Setup
from RacingWidget import RacingWidget
from  LapTimingDataTables import AllLapTimes

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(980,1920)
        self.setStyleSheet('background-color:#8FEFEF;')
        self.child_racing = RacingWidget(self)
        self.child_enter = Setup(self)
        self.child_laps = AllLapTimes(self)
        self.options = QVBoxLayout()
        self.options.setAlignment(Qt.AlignCenter)

        self.image = QPixmap('images/logo.png')
        self.logo = QLabel()
        self.logo.setPixmap(self.image)
        self.options.addWidget(self.logo)
        self.heading = QLabel()
        self.heading.setFont(QFont('Roboto',30))
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setStyleSheet('color:#FFFFFF; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.heading.setText('Four Lane Lap Counter')
        self.options.addWidget(self.heading)

        self.setup_button = QPushButton()
        self.setup_button.setStyleSheet('height: 100px;')#border:2px solid rgb(50,100,90);border-radius: 5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.setup_button.setText('SETUP RACERS')
        self.setup_button.clicked.connect(self.onSetup)
        self.options.addWidget(self.setup_button)

        self.laps_button = QPushButton()
        self.laps_button.setStyleSheet('height: 120px; border:2px solid rgb(50,100,90);border-radius: 5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.laps_button.setText('ALL RACING LAP TIMES')
        self.laps_button.clicked.connect(self.onLaps)
        self.options.addWidget(self.laps_button)

        self.race_button = QPushButton()
        self.race_button.setStyleSheet('height: 120px; border:2px solid rgb(50,100,90);border-radius: 5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.race_button.setText('RACING')
        self.race_button.clicked.connect(self.onRace)
        self.options.addWidget(self.race_button)
      
        self.exit_button = QPushButton()
        self.exit_button.setStyleSheet('height: 100px;')#('border:2px solid rgb(50,100,90);border-radius:30px;height: 100px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.exit_button.setText('EXIT')
        self.exit_button.clicked.connect(self.onExit)
        self.options.addWidget(self.exit_button)
        
        self.setLayout(self.options)

    def onExit(self):
        self.close()
        exit()

    def onLaps(self):
        self.hide()
        self.child_laps.updateData()
        self.child_laps.show()

    def onRace(self):
        #Standard race event, set number of laps, and each lap is timed
        self.hide()
        self.child_racing.show()
    
    def onSetup(self):
        self.hide()
        self.child_enter.show()

app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.resize(980,1920)
main_window.setFixedSize(980,1920)
main_window.width = 980
main_window.height = 1920
main_window.top = 0
main_window.left = 0
main_window.setStyleSheet('margin-left: 15px;margin-right;0px;')
main_widget = MainWidget()
main_window.setCentralWidget(main_widget)
main_window.show()
sys.exit(app.exec_())
