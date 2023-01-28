''' 
    Four lane lap counter and lap timer 
    
    Menu layout for different racing types

'''

from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from Camera import Camera, fllc
from LapTimingDataTables import ChampionshipLapTimes, RaceLapTimes, LapTimes
from LeaderboardTable import Leaderboard, LeaderboardEnd

class RacingWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.cancel = False
        self.child_camera = Camera(self)
        self.child_championship_laps = ChampionshipLapTimes(self)
        self.child_race_laps = RaceLapTimes(self)
        self.child_laps = LapTimes(self)
        self.child_leaderboard = Leaderboard(self)
        self.child_leaderboard_end = LeaderboardEnd(self)
        options = QVBoxLayout()
        options.setAlignment(Qt.AlignCenter)

        image = QPixmap('images/logo1.png')
        self.logo = QLabel()
        self.logo.setStyleSheet("padding: 10px")
        self.logo.setPixmap(image)
        options.addWidget(self.logo)

        heading = QLabel()
        heading.setFont(QFont('Roboto',30))
        heading.setStyleSheet('color:#FFFFFF; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        heading.setText('Four Lane Lap Counter')
        options.addWidget(heading)
        
        menu_button = QPushButton()
        menu_button.setStyleSheet('height: 120px; border: 1px solid; border-radius: 10px;')
        menu_button.setText('Main Menu')
        menu_button.clicked.connect(self.onMenu)
        options.addWidget(menu_button)
        
        free_button = QPushButton()
        free_button.setStyleSheet('height: 120px; border:2px solid rgb(50,100,90);border-radius: 5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        free_button.setText('FREE RACE')
        free_button.clicked.connect(self.onFreeRace)
        options.addWidget(free_button)

        race_button = QPushButton()
        race_button.setStyleSheet('height: 120px; border:2px solid rgb(50,100,90);border-radius: 5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        race_button.setText('RACING')
        race_button.clicked.connect(self.onRace)
        options.addWidget(race_button)

        champ_button = QPushButton()
        champ_button.setStyleSheet('height: 120px; border:2px solid rgb(50,100,90);border-radius: 5px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        champ_button.setText('CHAMPIONSHIP')
        champ_button.clicked.connect(self.onRaceChampionship)
        options.addWidget(champ_button)
        
        exit_button = QPushButton()
        exit_button.setStyleSheet('height: 120px;')
        exit_button.setText('EXIT')
        exit_button.clicked.connect(self.onExit)
        options.addWidget(exit_button)
        
        self.setLayout(options)

    def onExit(self):
        self.close()
        exit()

    def onMenu(self):
        self.parent.show()
        self.hide()
    
    def onFreeRace(self):
        #Race around track, lapcounter and or laptimer can be used
        if self.parent is None:
            self.errorNotMain()
            return
        self.child_camera.onLoad()
        self.child_camera.setTitle("FREE RACING")
        self.child_camera.setShowLaps(True)
        self.child_camera.setShowNames(True)
        self.child_camera.setShowRacePositions(False)
        if self.child_camera.video_widget.numberRacers() == 1:
            self.child_camera.setDescription("Track Record {:.3f}".format(fllc.TRACKRECORD/1000)+" by "+fllc.TRACKRECORDHOLDER)
            self.child_camera.setShowTime(True)
            self.child_camera.setRecordTime(True)
        else:
            self.child_camera.setDescription("Set number of laps, press [Start].")
            self.child_camera.setShowTime(False)
            self.child_camera.setRecordTime(False)
        self.child_camera.torch.setChecked(True)
        self.hide()
        self.child_camera.exec_()
        self.child_camera.onStop()
        fllc.saveMaxLaps()
        if self.child_camera.video_widget.numberRacers() == 1:
            self.child_camera.reset()
            self.child_laps.updateData()
            self.child_laps.exec()

    def onRace(self):
        #Standard race event, set number of laps, and each lap is timed
        if self.parent is None:
            self.errorNotMain()
            return
        if self.child_camera.video_widget.numberRacers() >= 2:
            self.child_camera.setShowRacePositions(True)
        else:
            self.child_camera.setShowRacePositions(False)
        self.child_camera.onLoad()
        self.child_camera.setTitle("RACING")
        self.child_camera.setDescription("Track Record {:.3f}".format(fllc.TRACKRECORD/1000)+" by "+fllc.TRACKRECORDHOLDER)
        self.child_camera.setShowLaps(True)
        self.child_camera.setShowNames(True)
        self.child_camera.setShowTime(True)
        self.child_camera.setRecordTime(True)
        self.child_camera.torch.setChecked(True)
        self.hide()
        self.child_camera.exec()
        self.child_camera.onStop()
        fllc.saveMaxLaps()
        self.hide()
        self.child_camera.reset()
        self.child_race_laps.updateData()
        self.child_race_laps.exec()
    
    def onRaceChampionship(self):
        #Champion race event
        if self.parent is None:
            self.errorNotMain()
            return
        self.showLeaderboard()
        if self.cancel:
            self.cancel = False
            return
        named_bool = self.child_camera.allNamed()
        if not named_bool:
            self.errorRecord()
            return
        self.child_camera.onLoad()
        self.child_camera.setTitle("CHAMPIONSHIP")
        self.child_camera.setDescription("Track Record {:.3f}".format(int(fllc.TRACKRECORD)/1000)+" by "+fllc.TRACKRECORDHOLDER)
        self.child_camera.setShowLaps(True)
        self.child_camera.setShowNames(True)
        self.child_camera.setShowRacePositions(True)
        self.child_camera.setShowTime(True)
        self.child_camera.setRecordTime(True)
        self.child_camera.torch.setChecked(True)
        self.hide()
        self.child_camera.exec_()
        self.child_camera.onStop()
        fllc.saveMaxLaps()
        self.child_camera.reset()
        self.showLeaderboardEnd()
        self.showLapTimes()

    def showLapTimes(self):
        self.hide()
        self.child_championship_laps.updateData()
        self.child_championship_laps.exec_()

    def showLeaderboard(self):
        self.hide()
        self.child_leaderboard.updateData()
        self.child_leaderboard.exec_()

    def showLeaderboardEnd(self):
        self.hide()
        self.child_leaderboard_end.updateData()
        self.child_leaderboard_end.exec_()

    def showIncomplete(self):
        QMessageBox.information(self,"Incomplete","To be done.",buttons=QMessageBox.Ok)
    
    def showNotCompleted(self):
        QMessageBox.information(self,"Leaderboard not Completed","To be finished, lap timing data done.Can race and save lap time data",buttons=QMessageBox.Ok)
    
    def errorRecord(self):
        QMessageBox.warning(self,"More Racers Required"," You need four racers to enter\nChampionship",buttons=QMessageBox.Ok)

    def errorNotMain(self):
        QMessageBox.warning(self,"APPLICATION NOT LOADED","You have executed a test for this menu",buttons=QMessageBox.Ok)
