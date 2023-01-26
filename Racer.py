
from PyQt5.QtCore import QObject, Qt, QDateTime
from PyQt5.QtGui import QColor

class Racer(QObject):
    starttime = 0
    def __init__(self, name, color, lane, maxlaps):
        super().__init__()
        self.name = name
        self.color = color
        self.lane = lane
        self.max_laps = maxlaps
        self.best_time = 0
        self.lap = 0
        self.lap_data = []
        self.lap_started = 0
        self.lap_times = []
        self.last_time = 0
        self.race_finished = False
        self.race_position = 0
        self.race_started = False
        self.rp_text = [" ","First","Second","Third","Fourth"]
        self.time = 0
        self.timer = 0
        self.timer_delay = 1500
        self.lastColor = QColor(Qt.white)
    
    def setTimer(self):
        if self.race_started and self.time < self.timer_delay:
            return
        
        time_now = QDateTime.currentMSecsSinceEpoch()
        if not self.race_started and self.starttime != 0:
            time_now = self.starttime
        else:
            self.starttime = time_now
        
        self.lap_data.append(time_now)
        self.lap_started = time_now
        if self.race_started:
            self.time = self.lapsedTime()
            self.lap_times.append(self.time)
            self.best_time = min(self.lap_times)
            if self.time < self.last_time:
                self.lastColor = QColor(Qt.green)
            elif self.time == self.last_time:
                self.lastColor = QColor(Qt.white)
            else:
                self.lastColor = QColor(Qt.red)
            
            self.last_time = self.time
            self.lap += 1
        
        if self.lap == self.max_laps:
            self.race_finished = True
        
        if self.lap == 0:
            self.race_started = True
        
        self.time = 0
    
    def lapsedTime(self):
        time_now = QDateTime.currentMSecsSinceEpoch()
        time = time_now - self.lap_started
        return time
    
    def reset(self):
        self.lap_data.clear()
        self.lap_times.clear()
        self.best_time = 0
        self.lap = 0
        self.lap_started = 0
        self.last_time = 0
        self.race_finished = False
        self.race_position = 0
        self.race_started = False
        self.timer = 0
        self.time = 0
        self.starttime = 0
    
    def getBestTime(self):
        time = self.best_time
        return time
    
    def getColor(self):
        return self.color
    
    def getLap(self):
        return self.lap

    def getLastTimeColor(self):
        return self.lastColor

    def getLastTime(self):
        time = self.last_time
        return time
    
    def getName(self):
        return self.name
    
    def getRaceData(self):
        return self.lap_data

    def getRacePosition(self, painter):
        return self.rp_text[self.race_position]
    
    def getTime(self):
        if self.race_started:
            self.time = self.lapsedTime()
        
        return self.time
     
    def hasStarted(self):
        return self.race_started
    
    def isFinished(self):
        return self.race_finished
    
    def setMaxLaps(self, laps):
        self.max_laps = laps
    
    def setRacePosition(self, position):
        self.race_position = position
