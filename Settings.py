''' 
    Four Lane Lap Counter and Lap Timer
    
    Settings object for Four Lane Lap Counter and Lap Timer
    
'''
from PyQt5.QtCore import QObject, Qt, QDateTime
from PyQt5.QtGui import QColor
import csv
from os.path import isfile

class Settings(QObject):
    ''' Variables for Four Lane Lap Counter and Timer '''
    RACER1 = []
    RACER2 = []
    RACER3 = []
    RACER4 = []
    SHAPES = []
    RACER1NAME = ""
    RACER2NAME = ""
    RACER3NAME = ""
    RACER4NAME = ""
    RACER1CARCOLOR = QColor
    RACER2CARCOLOR = QColor
    RACER3CARCOLOR = QColor
    RACER4CARCOLOR = QColor
    RACER1COLOR = Qt.black
    RACER2COLOR = Qt.black
    RACER3COLOR = Qt.black
    RACER4COLOR = Qt.black
    RACER1STARTED = False
    RACER2STARTED = False
    RACER3STARTED = False
    RACER4STARTED = False
    RACER1FINISHED = False
    RACER2FINISHED = False
    RACER3FINISHED = False
    RACER4FINISHED = False
    LANE1TIMER = 0
    LANE2TIMER = 0
    LANE3TIMER = 0
    LANE4TIMER = 0
    STARTED = False
    FINISHED = False
    FIRST = None
    SECOND = None
    THIRD = None
    FORTH = None
    RACETIMESTARTED = None
    TIMELANE1STARTED = None
    TIMELANE2STARTED = None
    TIMELANE3STARTED = None
    TIMELANE4STARTED = None
    PATH = '/storage/emulated/0/Documents/Python/FourLaneLapCounter/'
    IMAGE_PATH = PATH+'images/'
    DATABASE_PATH = PATH+'databases/'
    PATHOUT = PATH+'cache/'
    PRESET_PATH = PATH+'presets/'
    FIRSTPLACE = 50
    SECONDPLACE = 40
    THIRDPLACE = 30
    FOURTHPLACE = 10
    MAX = 5
    MAX_LAPS = 20
    WIDTH = 1080
    HEIGHT = 1920
    OFFSET = 50
    LANEOFFSET = 25
    MESSAGE = ""
    MESSAGE2 = ""
    ERROR = None
    DELAY = 1750
    CONTOUR_AREA = 1000
    ANTI_SHAKE_MIN = 100
    ANTI_SHAKE_MAX = 300
    KERNAL = 5, 5
    RANGE_START = 40
    RANGE_END = 255
    PRESET_INDEX = 0
    PRESET_TEXT = "presetA.csv"
    TRACKRECORD = 15000
    TRACKRECORDHOLDER = "To Be Set"
    start_loop = 0
    end_loop = 0
    var_motion = 0
    about_text = "Designed for <b>AFX TOMY</b> slot car four lane sets. Created to give easy access for four lane lap counting and lap timing by using mobile phone or tablet. <i>Motion detection</i> uses the camera to trigger the lap counting and lap timing. Could be used for other slot car tracks. "

    def __init__(self):
        self.date_time = QDateTime.currentDateTime()
        self.time_now = QDateTime.currentMSecsSinceEpoch()
        self.time_since = 0

    def RestoreSettings(self):
        ''' Restore Variables for Four Lane Lap Counter and Timer '''
        self.RACER1.clear()
        self.RACER2.clear()
        self.RACER3.clear()
        self.RACER4.clear()
        self.SHAPES.clear()
        self.RACER1COLOR = Qt.black
        self.RACER2COLOR = Qt.black
        self.RACER3COLOR = Qt.black
        self.RACER4COLOR = Qt.black
        self.RACER1STARTED = False
        self.RACER2STARTED = False
        self.RACER3STARTED = False
        self.RACER4STARTED = False
        self.RACER1FINISHED = False
        self.RACER2FINISHED = False
        self.RACER3FINISHED = False
        self.RACER4FINISHED = False
        self.LANE1TIMER = 0
        self.LANE2TIMER = 0
        self.LANE3TIMER = 0
        self.LANE4TIMER = 0
        self.STARTED = False
        self.FINISHED = False
        self.FIRST = None
        self.SECOND = None
        self.THIRD = None
        self.FORTH = None
        self.RACETIMESTARTED = None
        self.TIMELANE1STARTED = None
        self.TIMELANE2STARTED = None
        self.TIMELANE3STARTED = None
        self.TIMELANE4STARTED = None
        self.MESSAGE = ""
        self.MESSAGE2 = ""

    def load(self, flname):
        filename = flname
        found = isfile(self.PRESET_PATH+filename)
        if not found:
            return
        try:
            with open(self.PRESET_PATH+ filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.DELAY = int(row['Delay'])
                    self.CONTOUR_AREA = int(row['Area'])
                    self.ANTI_SHAKE_MIN = int(row['AntiMin'])
                    self.ANTI_SHAKE_MAX = int(row['AntiMax'])
                    self.KERNAL = int(row['KernalA']),int(row['KernalB'])
                    self.RANGE_START = int(row['RangeA'])
                    self.RANGE_END = int(row['RangeB'])
                    self.PRESET_INDEX = int(row['Index'])
            csvfile.close()
        
        except FileNotFoundError:
            self.ERROR = "FileNotFoundError"
        filename = "maxlaps.csv"
        try:
            with open(self.DATABASE_PATH+filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.MAX_LAPS = int(row['MaxLaps'])
                    self.TRACKRECORD = int(row['TrackRecord'])
                    self.TRACKRECORDHOLDER = row['TrackRecordHolder']
            csvfile.close()
        except FileNotFoundError:
            self.ERROR = "FileNotFoundError"

    def loadSetting(self, flname):
        filename = flname
        try:
            with open(self.PRESET_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.DELAY = int(row['Delay'])
                    self.CONTOUR_AREA = int(row['Area'])
                    self.ANTI_SHAKE_MIN = int(row['AntiMin'])
                    self.ANTI_SHAKE_MAX = int(row['AntiMax'])
                    self.KERNAL = int(row['KernalA']),int(row['KernalB'])
                    self.RANGE_START = int(row['RangeA'])
                    self.RANGE_END = int(row['RangeB'])
                    self.PRESET_INDEX = int(row['Index'])
            csvfile.close()
        except FileNotFoundError:
            self.ERROR = "FileNotFoundError"
    
    def loadStart(self):
        filename = "settings.csv"
        found = isfile(self.DATABASE_PATH+filename)
        if not found:
            self.load(self.PRESET_TEXT)
            return
        try:
            with open(self.DATABASE_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.PRESET_INDEX = int(row['index'])
                    self.PRESET_TEXT = row['preset']
            csvfile.close()
        except FileNotFoundError:
            pass
        
        self.load(self.PRESET_TEXT)
    
    def saveSettings(self):
        filename = "settings.csv"
        with open(self.DATABASE_PATH+filename, 'w', newline='') as csvfile:
            fields = ['index','preset']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerow({'index':str(self.PRESET_INDEX), 'preset':self.PRESET_TEXT})
        csvfile.close()
  
    def save(self, flname):
        filename = flname
        self.PRESET_TEXT = filename
        with open(self.PRESET_PATH+filename, 'w', newline='') as csvfile:
            fieldnames = ['Delay','Area','AntiMin', 'AntiMax', 'KernalA','KernalB','RangeA','RangeB','Index']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Delay':str(self.DELAY),'Area':str(self.CONTOUR_AREA),'AntiMin':str(self.ANTI_SHAKE_MIN),'AntiMax':str(self.ANTI_SHAKE_MAX),'KernalA':str(self.KERNAL[0]),'KernalB':str(self.KERNAL[1]),'RangeA':str(self.RANGE_START),'RangeB':str(self.RANGE_END),'Index':str(self.PRESET_INDEX)})
        csvfile.close()

    def saveMaxLaps(self):
        filename = "maxlaps.csv"
        with open(self.DATABASE_PATH+filename,'w', newline='') as csvfile:
            fieldnames = ['MaxLaps','TrackRecord','TrackRecordHolder']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'MaxLaps':str(self.MAX_LAPS ),'TrackRecord':str(self.TRACKRECORD),'TrackRecordHolder':self.TRACKRECORDHOLDER})
        csvfile.close()
