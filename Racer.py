import sys

from PyQt5.QtCore import (QObject, QPoint, Qt, QTimer, QDateTime)
from PyQt5.QtGui import (QBrush, QColor, QFont, QPainter, QPen, QIntValidator)

class Racer(QObject):
    lap_data = []
    lap_times = []
    rp_text = [" ","First","Second","Third","Fourth"]

    def __init__(self, name, color, lane, maxlaps, position_x, parent=None):
        super().__init__(parent)
        self.best_time = 0
        self.color = color
        self.lane = lane
        self.lap = 0
        self.lap_started = 0
        self.last_time = 0
        self.max_laps = maxlaps
        self.name = name
        self.parent = parent
        self.position = position_x
        self.race_finished = False
        self.race_position = 0
        self.race_started = False
        self.timer = 0
        self.time = 0
    
    def setTimer(self):
        time_now = QDateTime.currentMSecsSinceEpoch()
        self.lap_data.append(time_now)
        self.lap_started = time_now
        if self.started:
            self.time = self.lapsedTime
            self.lap_times.append(self.time)
            self.best_time = min(self.lap_data)
            self.last_time = self.time
            self.lap += 1
        self.started = True
        self.time = 0
    
    def lapsedTime(self):
        time_now = QDateTime.currentMSecsSinceEpoch()
        time = time_now - self.lap_data[len(self.lap_data)-1]
        return time
            
    def getBestTime(self):
        return self.best_time
    
    def getColor(self):
        return self.color
    
    def getLap(self):
        return self.lap

    def getLastTime(self):
        return self.last_time
    
    def getName(self):
        return self.name

    def getRacePosition(self, painter):
        return self.rp_text[self.race_position]
    
    def getTime(self):
        self.time = self.lapsedTime()
        return self.time
    