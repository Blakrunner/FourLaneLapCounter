'''
    Four lane lap counter and lap timer
    
    Racer class for better tracking of race timings and laps

'''
from PyQt5.QtCore import Qt, QDateTime, QObject
from PyQt5.QtGui import QColor

class Racer(QObject):
    starttime = 0
    race_position = []
    def __init__(self, name, color, lane, maxlaps):
        super().__init__()
        self.lap_data = []
        self.lap_times = []
        self.name = name
        self.color = color
        self.lane = lane
        self.max_laps = maxlaps
        self.number_racers = 0
        self.best_time = 0
        self.lap = 0
        self.lap_started = 0
        self.last_time = 0
        self.race_finished = False
        self.race_started = False
        self.time = 0
        self.timer = 0
        self.timer_delay = 1500
        self.lastColor = QColor(Qt.white)

    def setTimer(self):
        if self.race_started is True and self.time < self.timer_delay:
            return
        if self.checkRacePosition() is False:
            self.race_position.append([self.name,self.lap])
            
        time_now = QDateTime.currentMSecsSinceEpoch()
        if not self.race_started and self.starttime != 0:
            time_now = self.starttime
        else:
            self.starttime = time_now
        new_time = self.lapsedTime()
        if self.race_finished is False:
            self.lap_data.append(time_now)
        if self.lap >= self.max_laps:
            self.lap = self.max_laps
            self.race_finished = True
            return
        self.lap_started = time_now
        if self.race_started is True:
            old_time = self.last_time
            self.last_time = new_time
            self.lap_times.append(new_time)
            if len(self.lap_times) >= 2:
                self.best_time = min(self.lap_times)
            self.lap += 1
            self.changeColor(new_time,old_time)
        if self.lap == self.max_laps:
            self.race_finished = True
        if self.lap == 0:
            self.race_started = True
        self.time = 0

    def lapsedTime(self):
        time_now = QDateTime.currentMSecsSinceEpoch()
        _time = time_now - self.lap_started
        return _time

    def changeColor(self, new_time, old_time):
        if new_time == old_time:
            self.lastColor = QColor(Qt.white)
        elif  new_time < old_time:
            self.lastColor = QColor(Qt.green)
        else:
            self.lastColor = QColor(Qt.red)

    def checkRacePosition(self):
        return_bool = False
        if len(self.race_position) == 0:
            return return_bool
        i = 0
        l = []
        for name, lap in self.race_position:
            l.append(lap)
            if name == self.name:
                return_bool = True
                if lap < self.lap:
                    self.race_position.pop(i)
                    self.race_position.insert(i,[self.name,self.lap])
            i += 1
        if self.lap > max(l) and len(self.race_position) == self.number_racers:
            self.race_position.clear()
            return_bool = False
        return return_bool

    def clearRacePositions(self):
        self.race_position.clear()

    def reset(self):
        self.race_position.clear()
        self.lap_data.clear()
        self.lap_times.clear()
        self.best_time = 0
        self.lap = 0
        self.lap_started = 0
        self.last_time = 0
        self.race_finished = False
        self.race_started = False
        self.timer = 0
        self.time = 0
        self.starttime = 0

    def getBestTime(self):
        _time = self.best_time
        return _time

    def getColor(self):
        return self.color

    def getLap(self):
        return self.lap

    def getLastTimeColor(self):
        return self.lastColor

    def getLastTime(self):
        _time = self.last_time
        return _time

    def getName(self):
        return self.name

    def getRaceData(self):
        return self.lap_data

    def getTime(self):
        if self.race_started:
            self.time = self.lapsedTime()
        
        return self.time
 
    def hasStarted(self):
        return self.race_started

    def isFinished(self):
        return self.race_finished

    def setCarColor(self, color):
        self.color = color

    def setMaxLaps(self, laps):
        self.max_laps = laps

    def setName(self, name):
        self.name = name

    def setNumberRacers(self, number):
        self.number_racers = number

    def setTimerDelay(self, delay):
        self.timer_delay = delay
