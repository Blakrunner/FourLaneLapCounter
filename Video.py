''' 
    Four Lane Lap Counter and Lap Timer
    
    Video class for Four lane Lap Counter and Lap Timer

'''
from os.path import isfile
import numpy as np
import cv2
import csv

from PyQt5.QtWidgets import (
    QWidget
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QImage,
    QPainter
)
from PyQt5.QtCore import (
    QDateTime,
    QObject,
    QPoint,
    QRect,
    QTimer
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Shapes import Rectangle
from Settings import Settings

fllc = Settings()
fllc.loadStart()

class RecordVideo(QObject):
    ''' record video class '''
    image_data = QtCore.pyqtSignal(np.ndarray)
    x_array = []
    laneonetimes = []
    lanetwotimes = []
    lanethreetimes = []
    lanefourtimes = []
    
    def __init__(self, camera_port, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.camera = cv2.VideoCapture(camera_port)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1820)
        self.out_count = 0
        self.record_time = False
        self.started = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.Frame_init = None
        self.Frame_second = None
        self.Frame_differ = None
        self.Frame_gray = None
        self.Frame_blur = None
        self.Frame_thresh_a = None
        self.Frame_thresh_b = None
    
    def timerEvent(self):
        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)
            self.resetVariables()
            if fllc.FINISHED:
                return
            contours = self.detectMotion(data)
            if len(contours) == 0:
                return
            for cur in contours:
                if cv2.contourArea(cur) < fllc.CONTOUR_AREA:
                    continue
                (x, y, w, h) = cv2.boundingRect(cur)
                if w < fllc.ANTI_SHAKE_MIN or w > fllc.ANTI_SHAKE_MAX:
                    continue
               # fllc.MESSAGE = " w="+str(w) + fllc.MESSAGE
                fllc.SHAPES.append(Rectangle(w, h, QPoint(x, y), QColor(0, 255, 0), 1))
                self.x_array.append(x)
            
            if not self.started:
                return
            #!self.saveImageData()
            laneA, laneB, laneC, laneD = self.hasTriggered()
            self.collectLapTiming(laneA, laneB, laneC, laneD)
            self.x_array.clear()
            return
    
    def detectMotion(self, image1):
        _, image2 = self.camera.read()
        self.Frame_init = image1
        self.Frame_second = image2
        kernel = np.ones(fllc.KERNAL, np.uint8)
        differ_image = cv2.absdiff(image1, image2)
        self.Frame_differ = differ_image
        gray_image = cv2.cvtColor(differ_image, cv2.COLOR_BGR2GRAY)
        self.Frame_gray = gray_image
        fllc.HEIGHT = gray_image.shape[0]
        fllc.WIDTH = gray_image.shape[1]
        blur_image = cv2.GaussianBlur(gray_image, fllc.KERNAL, 0)
        self.Frame_blur = blur_image
        thresh_frameA = cv2.threshold(blur_image, fllc.RANGE_START, fllc.RANGE_END, cv2.THRESH_BINARY)[1]
        self.Frame_thresh_a = thresh_frameA
        thresh_frameB = cv2.dilate(thresh_frameA, kernel, iterations = 2)
        self.Frame_thresh_b = thresh_frameB
        cont, _ = cv2.findContours(thresh_frameB.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return cont
    
    def hasTriggered(self):
        ''' check if car has passed '''
        width = fllc.WIDTH - fllc.OFFSET
        ln1 = int(width/4)
        ln2 = int(width/2)
        ln3 = int((width/4)*3)
        trig1 = False
        trig2 = False
        trig3 = False
        trig4 = False
        if (len(fllc.RACER1) - 1) == fllc.MAX_LAPS:
            fllc.RACER1FINISHED = True
            self.setPlacings(fllc.RACER1NAME)
            fllc.FINISHED = self.allFinished()
        if (len(fllc.RACER2) - 1) == fllc.MAX_LAPS:
            fllc.RACER2FINISHED = True
            self.setPlacings(fllc.RACER2NAME)
            fllc.FINISHED = self.allFinished()
        if (len(fllc.RACER3) - 1) == fllc.MAX_LAPS:
            fllc.RACER3FINISHED = True
            self.setPlacings(fllc.RACER3NAME)
            fllc.FINISHED = self.allFinished()
        if (len(fllc.RACER4) - 1) == fllc.MAX_LAPS:
            fllc.RACER4FINISHED = True
            self.setPlacings(fllc.RACER4NAME)
            fllc.FINISHED = self.allFinished()
        for x in self.x_array:
            if x < (ln1 - fllc.LANEOFFSET) and not trig1:
                if not fllc.RACER1NAME == "":
                    if fllc.LANE1TIMER > fllc.DELAY or not fllc.RACER1STARTED:
                        trig1 = True
            elif x > ln1 and x < (ln2 - fllc.LANEOFFSET) and not trig2:
                if not fllc.RACER2NAME == "":
                    if fllc.LANE2TIMER > fllc.DELAY or not fllc.RACER2STARTED:
                        trig2 = True
            elif x > ln2 and x < (ln3 - fllc.LANEOFFSET) and not trig3:
                if not fllc.RACER3NAME == "":
                    if fllc.LANE3TIMER > fllc.DELAY or not fllc.RACER3STARTED:
                        trig3 = True
            elif x > ln3 and x < (width - fllc.LANEOFFSET) and not trig4:
                if not fllc.RACER4NAME == "":
                    if fllc.LANE4TIMER > fllc.DELAY or not fllc.RACER4STARTED:
                        trig4 = True
        return trig1, trig2, trig3, trig4
    
    def collectLapTiming(self, lane1, lane2, lane3, lane4):
        ''' collect lap and timing for lap data '''
        if lane1 and not fllc.RACER1FINISHED and not fllc.RACER1NAME == "":
            if len(fllc.RACER1) > 0:
                fllc.RACER1.append(fllc.LANE1TIMER)
                fllc.TIMELANE1STARTED = QDateTime.currentMSecsSinceEpoch()
                fllc.LANE1TIMER = 0
                fllc.RACER1COLOR = Qt.red
            elif len(fllc.RACER1) == 0:
                fllc.RACER1STARTED = True
                self.setStartedTime(QDateTime.currentMSecsSinceEpoch())
                if fllc.STARTED:
                    fllc.TIMELANE1STARTED = fllc.RACETIMESTARTED
                else:
                    fllc.STARTED = True
                    fllc.TIMELANE1STARTED = fllc.RACETIMESTARTED
                fllc.RACER1.append(fllc.TIMELANE1STARTED)
            if self.record_time:
                self.laneonetimes.append(fllc.TIMELANE1STARTED)
        #-------------------------------------------‐--------------------------------------‐----------------‐-----------------------
        if lane2 and not fllc.RACER2FINISHED and not fllc.RACER2NAME == "":
            if len(fllc.RACER2) > 0:
                fllc.RACER2.append(fllc.LANE2TIMER)
                fllc.TIMELANE2STARTED = QDateTime.currentMSecsSinceEpoch()
                fllc.LANE2TIMER = 0
                fllc.RACER2COLOR = Qt.red
            elif len(fllc.RACER2) == 0:
                fllc.RACER2STARTED = True
                self.setStartedTime(QDateTime.currentMSecsSinceEpoch())
                if fllc.STARTED:
                    fllc.TIMELANE2STARTED = fllc.RACETIMESTARTED
                else:
                    fllc.STARTED = True
                    fllc.TIMELANE2STARTED = fllc.RACETIMESTARTED
                fllc.RACER2.append(fllc.TIMELANE2STARTED)
            if self.record_time:
                self.lanetwotimes.append(fllc.TIMELANE2STARTED)
        #-------------------------------------------‐--------------------------------------‐----------------‐-----------------------
        if lane3 and not fllc.RACER3FINISHED and not fllc.RACER3NAME == "":
            if len(fllc.RACER3) > 0:
                fllc.RACER3.append(fllc.LANE3TIMER)
                fllc.TIMELANE3STARTED = QDateTime.currentMSecsSinceEpoch()
                fllc.LANE3TIMER = 0
                fllc.RACER3COLOR = Qt.red
            elif len(fllc.RACER3) == 0:
                fllc.RACER3STARTED = True
                self.setStartedTime(QDateTime.currentMSecsSinceEpoch())
                if fllc.STARTED:
                    fllc.TIMELANE3STARTED = fllc.RACETIMESTARTED
                else:
                    fllc.STARTED = True
                    fllc.TIMELANE3STARTED = fllc.RACETIMESTARTED
                fllc.RACER3.append(fllc.TIMELANE3STARTED)
            if self.record_time:
                self.lanethreetimes.append(fllc.TIMELANE3STARTED)
        #-------------------------------------------‐--------------------------------------‐----------------‐-----------------------
        if lane4 and not fllc.RACER4FINISHED and not fllc.RACER4NAME == "":
            if len(fllc.RACER4) > 0:
                fllc.RACER4.append(fllc.LANE4TIMER)
                fllc.TIMELANE4STARTED = QDateTime.currentMSecsSinceEpoch()
                fllc.LANE4TIMER = 0
                fllc.RACER4COLOR = Qt.red
            elif len(fllc.RACER4) == 0:
                fllc.RACER4STARTED = True
                self.setStartedTime(QDateTime.currentMSecsSinceEpoch())
                if fllc.STARTED:
                    fllc.TIMELANE4STARTED = fllc.RACETIMESTARTED
                else:
                    fllc.STARTED = True
                    fllc.TIMELANE4STARTED = fllc.RACETIMESTARTED
                fllc.RACER4.append(fllc.TIMELANE4STARTED)
            if self.record_time:
                self.lanefourtimes.append(fllc.TIMELANE4STARTED)
        #-------------------------------------------‐--------------------------------------‐----------------‐-----------------------
        if fllc.FINISHED:
            if self.record_time:
                if self.parent.title_text == "CHAMPIONSHIP":
                    self.saveLBdata()
                self.saveLapData()
                self.parent.exitToParent()
    
    def saveImageData(self):
        ''' used for visual checking of images are correct '''
        if self.out_count > fllc.MAX:
            return
        self.out_count += 1
        cv2.imwrite(fllc.PATHOUT+"Frame_init_"+str(self.out_count)+".png",self.Frame_init)
        cv2.imwrite(fllc.PATHOUT+"Frame_"+str(self.out_count)+".png",self.Frame_second)
        cv2.imwrite(fllc.PATHOUT+"Frame_differ_"+str(self.out_count)+".png",self.Frame_differ)
        cv2.imwrite(fllc.PATHOUT+"Frame_gray_"+str(self.out_count)+".png",self.Frame_gray)
        cv2.imwrite(fllc.PATHOUT+"Frame_blur_"+str(self.out_count)+".png",self.Frame_blur)
        cv2.imwrite(fllc.PATHOUT+"Frame_threshA_"+str(self.out_count)+".png",self.Frame_thresh_a)
        cv2.imwrite(fllc.PATHOUT+"Frame_threshB_"+str(self.out_count)+".png",self.Frame_thresh_b)

    def reverseLapData(self):
        '''  reverse data to correct order for display '''
        self.laneonetimes.reverse()
        self.lanetwotimes.reverse()
        self.lanethreetimes.reverse()
        self.lanefourtimes.reverse()
    
    def resetVariables(self):
        ''' reset color bar if been triggered '''
        fllc.RACER1COLOR = self.isRedChange(fllc.RACER1COLOR)
        fllc.RACER2COLOR = self.isRedChange(fllc.RACER2COLOR)
        fllc.RACER3COLOR = self.isRedChange(fllc.RACER3COLOR)
        fllc.RACER4COLOR = self.isRedChange(fllc.RACER4COLOR)
    
    def setMaxLaps(self, value):
        fllc.MAX_LAPS = value
        fllc.saveMaxLaps()
    
    def onLoad(self):
        self.timer.start(0)
    
    def setStart(self):
        self.started = True
    
    def setStop(self):
        self.started = False
        self.timer.stop()
    
    def reset(self):
        fllc.RestoreSettings()
        fllc.RACER1.clear()
        fllc.RACER2.clear()
        fllc.RACER3.clear()
        fllc.RACER4.clear()
    
    def isRedChange(self, color):
        if color == Qt.red:
            return Qt.black
        return color
    
    def setStartedTime(self,time):
        if not fllc.STARTED:
            fllc.RACETIMESTARTED = time
    
    def allNamed(self):
        if fllc.RACER1NAME == "":
            return False
        if fllc.RACER2NAME == "":
            return False
        if fllc.RACER3NAME == "":
            return False
        if fllc.RACER4NAME == "":
            return False
        return True
    
    def allFinished(self):
        if not fllc.RACER1NAME =="":
            if not fllc.RACER1FINISHED:
                return False
        if not fllc.RACER2NAME =="":
            if not fllc.RACER2FINISHED:
                return False
        if not fllc.RACER3NAME =="":
            if not fllc.RACER3FINISHED:
                return False
        if not fllc.RACER4NAME =="":
            if not fllc.RACER4FINISHED:
                return False
        return True
    
    def setPlacings(self, racer):
        fllc.MESSAGE += racer
        if fllc.FIRST is None and not fllc.SECOND == racer and not fllc.THIRD == racer and not fllc.FORTH == racer:
            fllc.FIRST = racer
            fllc.MESSAGE += " First "
            return
        elif fllc.SECOND is None and not fllc.FIRST == racer and not fllc.THIRD == racer and not fllc.FORTH == racer:
            fllc.SECOND = racer
            fllc.MESSAGE += " Second "
            return
        elif fllc.THIRD is None and not fllc.FIRST == racer and not fllc.SECOND == racer and not fllc.FORTH == racer:
            fllc.THIRD = racer
            fllc.MESSAGE += " Third "
            return
        elif fllc.FORTH is None and not fllc.FIRST == racer and not fllc.SECOND == racer and not fllc.THIRD == racer:
            fllc.FORTH = racer
            fllc.MESSAGE += " Fourth "
            return
        return

    def saveLapData(self):
        ''' Save lap data to a csv file '''
        self.reverseLapData()
        date = QDateTime.currentDateTime().toString()
        max_range = fllc.MAX_LAPS + 1
        #title = self.parent.title_text
        filename = "lap_time_data.csv"
        try:
            found = isfile(fllc.DATABASE_PATH+filename)
            if not found:
                raise FileNotFoundError
            
            with open(fllc.DATABASE_PATH+filename, 'a', newline='') as csvfile:
                fieldnames = ['date','lane1','lane2','lane3','lane4']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'date':fllc.MAX_LAPS,'lane1':fllc.RACER1NAME,'lane2':fllc.RACER2NAME,'lane3':fllc.RACER3NAME,'lane4':fllc.RACER4NAME})
                for _ in range(max_range):
                    writer.writerow({'date':date,'lane1':self.setValueLane(1),'lane2':self.setValueLane(2),'lane3':self.setValueLane(3),'lane4':self.setValueLane(4)})
            csvfile.close()
        except FileNotFoundError:
            with open(fllc.DATABASE_PATH+filename, 'w', newline='') as csvfile:
                fieldnames = ['date','lane1','lane2','lane3','lane4']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'date':fllc.MAX_LAPS,'lane1':fllc.RACER1NAME,'lane2':fllc.RACER2NAME,'lane3':fllc.RACER3NAME,'lane4':fllc.RACER4NAME})
                for _ in range(max_range):
                    writer.writerow({'date':date,'lane1':self.setValueLane(1),'lane2':self.setValueLane(2),'lane3':self.setValueLane(3),'lane4':self.setValueLane(4)})
            csvfile.close()

    def saveLBdata(self):
        if not self.allNamed:
            return
        
        filename = "lbdata.csv"
        fields = ["name", "lane","bestLap", "points"]
        racer1,racer2,racer3,racer4 = "","","",""
        best1,best2,best3,best4 = 0,0,0,0
        pnts1,pnts2,pnts3,pnts4 = 0,0,0,0
        try:
            with open(fllc.DATABASE_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cnt = 1
                for row in reader:
                    if cnt == 1:
                        racer1 = row["name"]
                        best1 = self.setBestLap(1, int(row["bestLap"]))
                        pnts1 = self.setPoints(1, int(row["points"]))
                    if cnt == 2:
                        racer2 = row["name"]
                        best2 = self.setBestLap(2, int(row["bestLap"]))
                        pnts2 = self.setPoints(2, int(row["points"]))
                    if cnt == 3:
                        racer3 = row["name"]
                        best3 = self.setBestLap(3, int(row["bestLap"]))
                        pnts3 = self.setPoints(3, int(row["points"]))
                    if cnt == 4:
                        racer4 = row["name"]
                        best4 = self.setBestLap(4, int(row["bestLap"]))
                        pnts4 = self.setPoints(4, int(row["points"]))
                    cnt += 1

            csvfile.close()
            with open(fllc.DATABASE_PATH+filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                writer.writerow({"name":fllc.RACER1NAME,"lane":1,"bestLap":best1,"points":pnts1})
                writer.writerow({"name":fllc.RACER2NAME,"lane":2,"bestLap":best2,"points":pnts2})
                writer.writerow({"name":fllc.RACER3NAME,"lane":3,"bestLap":best3,"points":pnts3})
                writer.writerow({"name":fllc.RACER4NAME,"lane":4,"bestLap":best4,"points":pnts4})
            csvfile.close()
        except FileNotFoundError:
            with open(fllc.DATABASE_PATH+filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                writer.writerow({"name":fllc.RACER1NAME,"lane":1,"bestLap":self.getLaneValue(self.laneonetimes.index(min(self.laneonetimes)),self.laneonetimes),"points":self.getPoints(fllc.RACER1NAME)})
                writer.writerow({"name":fllc.RACER2NAME,"lane":2,"bestLap":self.getLaneValue(self.lanetwotimes.index(min(self.lanetwotimes)),self.lanetwotimes),"points":self.getPoints(fllc.RACER2NAME)})
                writer.writerow({"name":fllc.RACER3NAME,"lane":3,"bestLap":self.getLaneValue(self.lanethreetimes.index(min(self.lanethreetimes)),self.lanethreetimes),"points":self.getPoints(fllc.RACER3NAME)})
                writer.writerow({"name":fllc.RACER4NAME,"lane":4,"bestLap":self.getLaneValue(self.lanefourtimes.index(min(self.lanefourtimes)),self.lanefourtimes),"points":self.getPoints(fllc.RACER4NAME)})
            csvfile.close()

    def getPoints(self, racer):
        if racer == fllc.FIRST:
            return int(fllc.FIRSTPLACE)
        elif racer == fllc.SECOND:
            return int(fllc.SECONDPLACE)
        elif racer == fllc.THIRD:
            return int(fllc.THIRDPLACE)
        else:
            return int(fllc.FOURTHPLACE)
        return 0

    def setPoints(self, lane, points):
        if not self.allNamed:
            return
        
        if lane == 1:
            p = self.getPoints(fllc.RACER1NAME)
            p += points
            return p
        if lane == 2:
            p = self.getPoints(fllc.RACER2NAME)
            p += points
            return p
        if lane == 3:
            p = self.getPoints(fllc.RACER3NAME)
            p += points
            return p
        if lane == 4:
            p = self.getPoints(fllc.RACER4NAME)
            p += points
            return p
        return points

    def setBestLap(self, value, best):
        if value == 1 and not fllc.RACER1NAME == "":
            b1 = min(self.laneonetimes)
            b1 = self.getLaneValue(self.laneonetimes.index(b1),self.laneonetimes)
            if best == 0:
                return b1
            if b1 < best:
                return b1
            else:
                return best
        if value == 2 and not fllc.RACER2NAME == "":
            b2 = min(self.lanetwotimes)
            b2 = self.getLaneValue(self.lanetwotimes.index(b2),self.lanetwotimes)
            if best == 0:
                return b2
            if b2 < best:
                return b2
            else:
                return best
        if value == 3 and not fllc.RACER3NAME == "":
            b3 = min(self.lanethreetimes)
            b3 = self.getLaneValue(self.lanethreetimes.index(b3),self.lanethreetimes)
            if best == 0:
                return b3
            if b3 < best:
                return b3
            else:
                return best
        if value == 4 and not fllc.RACER3NAME == "":
            b4 = min(self.lanefourtimes)
            b4 = self.getLaneValue(self.lanefourtimes.index(b4),self.lanefourtimes)
            if best == 0:
                return b4
            if b4 < best:
                return b4
            else:
                return best
        return best

    def getLaneValue(self, index, lanedata):
        cnt, timedata = 0, 0
        _dat = []
        for data in lanedata:
            if cnt == 0:
                timedata = data
            else:
                _dat.append(data - timedata)
                timedata = data
            cnt += 1
        
        return_value = min(_dat)
        return return_value

    def setValueLane(self, lane):
        if lane == 1:
            if len(self.laneonetimes) > 0:
                return self.laneonetimes.pop()
        if lane == 2:
            if len(self.lanetwotimes) > 0:
                return self.lanetwotimes.pop()
        if lane == 3:
            if len(self.lanethreetimes) > 0:
                return self.lanethreetimes.pop()
        if lane == 4:
            if len(self.lanefourtimes) > 0:
                return self.lanefourtimes.pop()
        return

class VideoWidget(QWidget):
    image_data = None
    frames = []
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color:#8FEFEF;margins:0px;padding:0px;')
        self.image = QImage()
        self.show_laps = False
        self.show_names = False
        self.show_time = False
        self.max_laps = fllc.MAX_LAPS
        self.box = 0,0
        self.parent_heading = None
        self.parent = parent
        self.test = True
    
    def setShowTime(self, show):
        self.show_time = show
    
    def image_data_slot(self, image_data):
        if (self.width() > self.height()) != (image_data.shape[1] > image_data.shape[0]):
            # Need to rotate image data, the screen / camera is rotated
            image_data = cv2.rotate(image_data, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.image = self.get_qimage(image_data)
        self.update()
    
    def get_qimage(self, image):
        height, width, _ = image.shape
        self.box = width, height
        image = QImage(image.data, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
        return image
    
    def resize_image(self, image, scale):
        #get the webcam size
        height, width, _ = image.shape

        #prepare the crop
        centerX,centerY=int(height/2),int(width/2)
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)

        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY

        cropped = image[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height))
        return resized_cropped
    
    def paintEvent(self, event):
        painter = QPainter(self)
        fllc.var_motion += 1
        if not fllc.FINISHED:
            if fllc.STARTED and not self.parent_heading == None and not self.parent_heading == "SETUP CAMERA POSITION":
                timenow = QDateTime.currentMSecsSinceEpoch()
                if fllc.RACER1STARTED and not fllc.RACER1FINISHED:
                    timepassed = timenow - fllc.TIMELANE1STARTED
                    fllc.LANE1TIMER = timepassed
                if fllc.RACER2STARTED and not fllc.RACER2FINISHED:
                    timepassed = timenow - fllc.TIMELANE2STARTED
                    fllc.LANE2TIMER = timepassed
                if fllc.RACER3STARTED and not fllc.RACER3FINISHED:
                    timepassed = timenow - fllc.TIMELANE3STARTED
                    fllc.LANE3TIMER = timepassed
                if fllc.RACER4STARTED and not fllc.RACER4FINISHED:
                    timepassed = timenow - fllc.TIMELANE4STARTED
                    fllc.LANE4TIMER = timepassed
        w, h = self.box 
        w, h = int(w), int(h)
        if w < 1000:
            w = 1080
        if h < 1780 or h > 1780:
            h = 1780
        '''
        cw = self.image.width()
        ch = self.image.height()
 
        # Keep aspect ratio
        if ch != 0 and cw != 0:
            w = min(cw * h / ch, w)
            h = min(ch * w / cw, h)
            w, h = int(w), int(h)'''
        w = w-fllc.OFFSET
        painter.drawImage(QRect(0, 0, w, h), self.image)
        self.drawOverlay(painter, w, h)
        for shape in fllc.SHAPES:
            shape.paint(painter)
        if fllc.var_motion == 5:
            fllc.var_motion = 0
            fllc.SHAPES.clear()
        ''' set this and start_loop to show timing of motion detector cycle time
        fllc.end_loop = QDateTime.currentMSecsSinceEpoch()
        if fllc.start_loop != 0:
            painter.setFont(QFont('Roboto',14))
            taken = fllc.end_loop - fllc.start_loop
            painter.setPen(QColor(Qt.yellow))
            painter.drawText(10,1700,"took:"+str(taken)+"ms")
        '''
        '''  Show error messages    '''
        if not fllc.MESSAGE == "":
            painter.drawText(10,1600,fllc.MESSAGE)
        self.image = QImage()
        #fllc.start_loop = QDateTime.currentMSecsSinceEpoch()
    
    def drawOverlay(self, qpainter, w, h):
        ''' function for draw overlay for track lanes '''
        painter = qpainter
        offset = 10
        lanewidth = w/4
        self.frames.clear()
        self.frames.append(Rectangle(lanewidth,h,QPoint(0,0),QColor(255,255,255),5))
        self.frames.append(Rectangle(lanewidth,h,QPoint(lanewidth,0),QColor(255,255,255),5))
        self.frames.append(Rectangle(lanewidth,h,QPoint(lanewidth*2,0),QColor(255,255,255),5))
        self.frames.append(Rectangle(lanewidth,h,QPoint(lanewidth*3,0),QColor(255,255,255),5))

        self.frames.append(Rectangle(lanewidth-20,5,QPoint(offset,100),QColor(fllc.RACER1COLOR),5))
        self.frames.append(Rectangle(lanewidth-20,5,QPoint(lanewidth+offset,100),QColor(fllc.RACER2COLOR),5))
        self.frames.append(Rectangle(lanewidth-20,5,QPoint((lanewidth*2)+offset,100),QColor(fllc.RACER3COLOR),5))
        self.frames.append(Rectangle(lanewidth-20,5,QPoint((lanewidth*3)+offset,100),QColor(fllc.RACER4COLOR),5))

        painter.drawImage(QRect(0, 0, w, h), self.image)
        painter.setFont(QFont('Roboto',30))
        painter.setPen(QColor(Qt.white))
        for frame in self.frames:
            frame.paint(painter)
        painter.setFont(QFont('Roboto',20))
        if self.show_names:
            painter.setPen(fllc.RACER1CARCOLOR)
            painter.drawText(20,70,fllc.RACER1NAME)
            painter.setPen(fllc.RACER2CARCOLOR)
            painter.drawText(lanewidth+20,70,fllc.RACER2NAME)
            painter.setPen(fllc.RACER3CARCOLOR)
            painter.drawText((lanewidth*2)+20,70,fllc.RACER3NAME)
            painter.setPen(fllc.RACER4CARCOLOR)
            painter.drawText((lanewidth*3)+20,70,fllc.RACER4NAME)
        if self.show_laps:
            painter.setPen(QColor(Qt.white))
            laps_racer1 = self.isMax(len(fllc.RACER1)-1)
            laps_racer1 = self.isBelowZero(laps_racer1)
            painter.drawText(50,170,"Lap "+str(laps_racer1))
            laps_racer2 = self.isMax(len(fllc.RACER2)-1)
            laps_racer2 = self.isBelowZero(laps_racer2)
            painter.drawText(lanewidth+50,170,"Lap "+str(laps_racer2))
            laps_racer3 = self.isMax(len(fllc.RACER3)-1)
            laps_racer3 = self.isBelowZero(laps_racer3)
            painter.drawText((lanewidth*2)+50,170,"Lap "+str(laps_racer3))
            laps_racer4 = self.isMax(len(fllc.RACER4)-1)
            laps_racer4 = self.isBelowZero(laps_racer4)
            painter.drawText((lanewidth*3)+50,170,"Lap "+str(laps_racer4))
        if self.show_time:
            painter.setFont(QFont('Roboto',14))
            painter.setPen(QColor(Qt.yellow))
            painter.drawText(15,370,"Time:{: .3f}".format(fllc.LANE1TIMER/1000))
            painter.drawText(lanewidth+15,370,"Time:{: .3f}".format(fllc.LANE2TIMER/1000))
            painter.drawText((lanewidth*2)+15,370,"Time:{: .3f}".format(fllc.LANE3TIMER/1000))
            painter.drawText((lanewidth*3)+15,370,"Time:{: .3f}".format(fllc.LANE4TIMER/1000))
            if len(fllc.RACER1) > 0:
                color = QColor(Qt.yellow)
                if len(fllc.RACER1) > 1:
                    self.checkTrackRecord(min(fllc.RACER1),fllc.RACER1NAME)
                    painter.setPen(QColor(Qt.blue))
                    painter.drawText(10,300,"Best:{:.3f}".format(min(fllc.RACER1)/1000))
                    color = self.getColor(fllc.RACER1[len(fllc.RACER1)-1] , fllc.RACER1[len(fllc.RACER1)-2])
                painter.setPen(color)
                painter.drawText(10,440,"Last:{:.3f}".format(fllc.RACER1[len(fllc.RACER1)-1]/1000))
            if len(fllc.RACER2) > 0:
                color = QColor(Qt.yellow)
                if len(fllc.RACER2) > 1:
                    self.checkTrackRecord(min(fllc.RACER2),fllc.RACER2NAME)
                    painter.setPen(QColor(Qt.blue))
                    painter.drawText(lanewidth+10,300,"Best:{:.3f}".format(min(fllc.RACER2)/1000))
                    color = self.getColor(fllc.RACER2[len(fllc.RACER2)-1] , fllc.RACER2[len(fllc.RACER2)-2])
                painter.setPen(color)
                painter.drawText(lanewidth+10,440,"Last:{:.3f}".format(fllc.RACER2[len(fllc.RACER2)-1]/1000))
            if len(fllc.RACER3) > 0:
                color = QColor(Qt.yellow)
                if len(fllc.RACER3) > 1:
                    self.checkTrackRecord(min(fllc.RACER3),fllc.RACER3NAME)
                    painter.setPen(QColor(Qt.blue))
                    painter.drawText((lanewidth*2)+10,300,"Best:{:.3f}".format(min(fllc.RACER3)/1000))
                    color = self.getColor(fllc.RACER3[len(fllc.RACER3)-1] , fllc.RACER3[len(fllc.RACER3)-2])
                painter.setPen(color)
                painter.drawText((lanewidth*2)+10,440,"Last:{:.3f}".format(fllc.RACER3[len(fllc.RACER3)-1]/1000))
            if len(fllc.RACER4) > 0:
                color = QColor(Qt.yellow)
                if len(fllc.RACER4) > 1:
                    self.checkTrackRecord(min(fllc.RACER4),fllc.RACER4NAME)
                    painter.setPen(QColor(Qt.blue))
                    painter.drawText((lanewidth*3)+10,300,"Best:{:.3f}".format(min(fllc.RACER4)/1000))
                    color = self.getColor(fllc.RACER4[len(fllc.RACER4)-1] , fllc.RACER4[len(fllc.RACER4)-2])
                painter.setPen(color)
                painter.drawText((lanewidth*3)+10,440,"Last:{:.3f}".format(fllc.RACER4[len(fllc.RACER4)-1]/1000))
        if self.test:
            self.test = False
        painter.setFont(QFont('Roboto',16))
        painter.setPen(QColor(Qt.white))
        if fllc.RACER1FINISHED and not fllc.RACER1NAME == fllc.FIRST:
            painter.drawText(25,240,"FINISHED")
        if fllc.RACER2FINISHED and not fllc.RACER2NAME == fllc.FIRST:
            painter.drawText(lanewidth+25,240,"FINISHED")
        if fllc.RACER3FINISHED and not fllc.RACER3NAME == fllc.FIRST:
            painter.drawText(lanewidth*2+25,240,"FINISHED")
        if fllc.RACER4FINISHED and not fllc.RACER4NAME == fllc.FIRST:
            painter.drawText(lanewidth*3+25,240,"FINISHED")
            
        painter.setFont(QFont('Roboto',22))
        painter.setPen(QColor(Qt.magenta))
        if fllc.RACER1NAME == fllc.FIRST:
            painter.drawText(5,250,"WINNER")
        if fllc.RACER2NAME == fllc.FIRST:
            painter.drawText(lanewidth+5,250,"WINNER")
        if fllc.RACER3NAME == fllc.FIRST:
            painter.drawText(lanewidth*2+5,250,"WINNER")
        if fllc.RACER4NAME == fllc.FIRST:
            painter.drawText(lanewidth*3+5,250,"WINNER")

    def isMax(self, value):
        return_value = value
        if value > fllc.MAX_LAPS:
            return_value = fllc.MAX_LAPS
        return return_value

    def isBelowZero(self, value):
        return_value = value
        if value < 0:
            return_value = 0
        return return_value

    def getColor(self,value1, value2):
        if value1 < value2:
            color = QColor(Qt.green)
        elif value1 == value2:
            color = QColor(Qt.yellow)
        else:
            color = QColor(Qt.red)
        return color

    def checkTrackRecord(self, value, racer):
        if value < fllc.TRACKRECORD:
            fllc.TRACKRECORD = value
            fllc.TRACKRECORDHOLDER = racer
            self.parent.showTrackRecord()
