''' 
    Four Lane Lap Counter and Lap Timer
    
    Camera dialog with lane seperation for Four Lane Lap Counter and Lap Timer 
    
'''
import cv2
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtWidgets import QDialog, QCheckBox, QInputDialog, QLabel, QLayout, QHBoxLayout, QVBoxLayout, QMessageBox, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Video import RecordVideo, VideoWidget, fllc

class Camera(QDialog):
    ''' Camera with layout for positioning '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.player = QtMultimedia.QMediaPlayer()
        self.sound_start_file = fllc.SOUND_PATH+'robotic-countdown.mp3'
        self.sound_crowd_file = fllc.SOUND_PATH+'crowd_of_boys.mp3'
        self.sound_crowd_booing_file = fllc.SOUND_PATH+'crowd_boo.mp3'
        self.sound_end_file = fllc.SOUND_PATH+'victory.mp3'
        self.url_start = QtCore.QUrl.fromLocalFile(self.sound_start_file)
        self.url_crowd = QtCore.QUrl.fromLocalFile(self.sound_crowd_file)
        self.url_crowd_booing = QtCore.QUrl.fromLocalFile(self.sound_crowd_booing_file)
        self.url_end = QtCore.QUrl.fromLocalFile(self.sound_end_file)
        self.setStyleSheet('background-color:#8FEFEF')
        self.title_text = "SETUP"
        self.description_text = "Position camera so all four lanes\n fit vertical lines between each lane."
        self.show_me = True
        self.show_time = False
        self.record_time = False
        self.max_laps = fllc.MAX_LAPS
        self.setWindowTitle(self.title_text)
        self.resize(1080,2180)
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetNoConstraint)
        layout.setAlignment(Qt.AlignCenter)
        self.heading = QLabel()
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setStyleSheet('color:#FFFFFF; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.heading.setFont(QFont("Roboto",26))
        self.heading.setText(self.title_text)
        self.heading.setObjectName("heading")
        layout.addWidget(self.heading)
        self.description = QLabel()
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet('color:blue')
        self.description.setFont(QFont("Roboto",17))
        self.description.setText(self.description_text)
        layout.addWidget(self.description)
        if self.show_me:
            self.video_widget = VideoWidget(parent=self)
            self.record_video = RecordVideo(0,parent=self)
            self.record_video.image_data.connect(self.video_widget.image_data_slot)
            layout.addWidget(self.video_widget)
            self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.button_layout = QHBoxLayout()
        self.exit_button = QPushButton()
        self.exit_button.setText("QUIT")
        self.exit_button.clicked.connect(self.exitToParent)
        self.button_layout.addWidget(self.exit_button)
        self.start_button = QPushButton()
        self.start_button.setText("START")
        self.start_button.clicked.connect(self.onStart)
        self.button_layout.addWidget(self.start_button)
        self.laps_button = QPushButton()
        self.laps_button.setText(str(self.max_laps)+' LAPS')
        self.laps_button.clicked.connect(self.setLaps)
        self.button_layout.addWidget(self.laps_button)
        self.torch = QCheckBox("Torch")
        self.torch.stateChanged.connect(self.onTorch)
        self.button_layout.addWidget(self.torch)
        layout.addLayout(self.button_layout)
        self.setLayout(layout)
    
    def onLoad(self):
        self.record_video.onLoad()

    def exitToParent(self):
        self.reset()
        self.torch.setChecked(False)
        if self.parent == None:
            exit()
        self.parent.show()
        self.hide()

    def onTorch(self, state):
        self.record_video.camera.set(cv2.CAP_PROP_ANDROID_FLASH_MODE, cv2.CAP_ANDROID_FLASH_MODE_ON if state == Qt.Checked else cv2.CAP_ANDROID_FLASH_MODE_OFF)

    def allNamed(self):
        return_bool = self.record_video.allNamed()
        return return_bool
    
    def onJumpStart(self):
        self.player.setMedia(QtMultimedia.QMediaContent(self.url_crowd_booing))
        self.player.setVolume(90)
        self.player.play()
        self.exitToParent()
        
    
    def onStart(self):
        self.record_video.setStart()
        fllc.STARTED = False
        self.player.setMedia(QtMultimedia.QMediaContent(self.url_start))
        self.player.setVolume(90)
        self.player.play()
    
    def onStop(self):
        self.record_video.setStop()
        self.reset()
    
    def showTrackRecord(self):
        self.player.setMedia(QtMultimedia.QMediaContent(self.url_crowd))
        self.player.setVolume(50)
        self.player.play()
        self.description.setText("Track Record {:.3f}".format(fllc.TRACKRECORD/1000)+" by "+fllc.TRACKRECORDHOLDER)
    
    def setTitle(self, title):
        self.heading.setText(title)
        self.title_text = title
        self.video_widget.parent_heading = title

    def setDescription(self, description):
        self.description.setText(description)
        self.description_text = description
    
    def setShowLaps(self, show):
        self.video_widget.show_laps = show
    
    def setShowNames(self, show):
        self.video_widget.show_names = show

    def setShowRacePositions(self, show):
        self.video_widget.show_race_positions = show

    def setShowTime(self, show):
        self.video_widget.setShowTime(show)

    def setRecordTime(self, record):
        self.record_video.record_time = record
    
    def reset(self):
        self.record_video.reset()

    def setMaxLaps(self, value):
        self.record_video.setMaxLaps(value)
    
    def setTimerDelay(self, delay):
        self.video_widget.racer1.setTimerDelay(delay)
        self.video_widget.racer2.setTimerDelay(delay)
        self.video_widget.racer3.setTimerDelay(delay)
        self.video_widget.racer4.setTimerDelay(delay)
    
    def setLaps(self):
        number, ok = QInputDialog.getInt(self, "Input Laps", "Enter number of laps", value=self.max_laps)
        
        if ok:
            self.video_widget.max_laps = number
            self.max_laps = number
            self.setMaxLaps(number)
            self.laps_button.setText(str(self.max_laps)+' LAPS')

    def errorRecord(self):
        QMessageBox.warning(self,"More Racers Required","     You need 4 racers to enter Championship",buttons=QMessageBox.Ok)
