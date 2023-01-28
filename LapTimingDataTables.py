'''
    Four lane lap counter and lap timer
    
    Tables for Lap times

'''
import csv
import pandas as pd

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QTableView
)
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QColor
from  Video import fllc

class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, float):
                # Render float to 3 dp for milliseconds
                return "%.3f" % value
            return str(value)

        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]

            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignVCenter + Qt.AlignRight
            if isinstance(value, str):
                return Qt.AlignCenter

        if role == Qt.BackgroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value,str):
                return QColor(255,250,180)
            if value > 40.0:
                return QColor(255,255,243)
            return QColor(203,253,253)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        if role == Qt.EditRole:
            return Qt.NoItemFlags

class ChampionshipLapTimes(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(1080,2170)
        self.parent = parent
        self.header_names = []
        self.total_row = []
        self.heading = QLabel()
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setFont(QFont('Roboto',36))
        self.heading.setStyleSheet('color:white; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.heading.setText('CHAMPIONSHIP')
        self.subheading = QLabel()
        self.subheading.setAlignment(Qt.AlignCenter)
        self.subheading.setFont(QFont('Roboto',30))
        self.subheading.setText("Lap Times")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.subheading)
        self.table_view = QTableView()
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        #self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(0,210)
        self.table_view.setColumnWidth(1,210)
        self.table_view.setColumnWidth(2,210)
        self.table_view.setColumnWidth(3,210)
        self.table_view.setStyleSheet("QScrollBar:vertical{width:50px;}")
        self.layout.addWidget(self.table_view)
        
        self.button_exit = QPushButton()
        self.button_exit.setStyleSheet('height: 80px;')#('border:2px solid rgb(50,100,90);border-radius:30px;height: 100px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.button_exit.setText('CONTINUE')
        self.button_exit.clicked.connect(self.onExit)
        self.layout.addWidget(self.button_exit)
        self.setLayout(self.layout)
    
    def updateData(self):
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        self.update()
    
    def upDateBackground(self):
        # change background colors
        self.model.data(self.model.rowCount(1) ,role=Qt.BackgroundRole)
    
    def loadData(self):
        _data = []
        _lap_index = []
        ln1, ln2, ln3, ln4 = 0, 0, 0, 0
        filename = 'lap_time_data.csv'
        try:
            with open(fllc.DATABASE_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cnt,laps,lpcnt,nl = 0,0,0,0
                lane1, lane2, lane3, lane4 = "","","",""
                row = None
                for row in reader:
                    if cnt == 0:
                        if row['lane1'] == "" or row['lane2'] == "" or row['lane3'] == "" or row['lane4'] == "":
                            continue
                        if nl > 0:
                            _data.append([(int(lane1)-ln1)/1000,(int(lane2)-ln2)/1000,(int(lane3)-ln3)/1000,(int(lane4)-ln4)/1000])
                            _lap_index.append('Total')
                            self.total_row.append(len(_data)-1)
                            lpcnt = 0
                        _data.clear()
                        _lap_index.clear()
                        if row['lane1'] == "" or row['lane2'] == "" or row['lane3'] == "" or row['lane4'] == "":
                            continue
                        _data.append([row['lane1'],row['lane2'],row['lane3'],row['lane4']])
                        laps = int(row['date'])
                        _lap_index.append('Name')
                    elif cnt == 1:
                        if row['lane1'] == "" or row['lane2'] == "" or row['lane3'] == "" or row['lane4'] == "":
                            continue
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        ln1, ln2, ln3, ln4 = int(lane1), int(lane2), int(lane3), int(lane4)
                    elif cnt > 1:
                        if row['lane1'] == "" or row['lane2'] == "" or row['lane3'] == "" or row['lane4'] == "":
                            continue
                        _data.append([(int(row['lane1'])-int(lane1))/1000,(int(row['lane2'])-int(lane2))/1000,(int(row['lane3'])-int(lane3))/1000,(int(row['lane4'])-int(lane4))/1000])
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        lpcnt += 1
                        _lap_index.append('Lap '+str(lpcnt))
                    if (cnt-1) == laps:
                        cnt = 0
                        nl += 1
                    else:
                        cnt += 1
            
            if row['lane1'] == "" or row['lane2'] == "" or row['lane3'] == "" or row['lane4'] == "":
                raise FileNotFoundError
            _data.append([(int(lane1)-ln1)/1000,(int(lane2)-ln2)/1000,(int(lane3)-ln3)/1000,(int(lane4)-ln4)/1000])
            _lap_index.append('Total')
            csvfile.close()
        
        except FileNotFoundError:
            if len(_data) == 0:
                _data = [[fllc.RACER1NAME,fllc.RACER2NAME,fllc.RACER3NAME,fllc.RACER4NAME],[0.0,0.0,0.0,0.0]]
                _lap_index = ['Name','Lap 1']
          
        data = pd.DataFrame(_data, columns=['Lane1','Lane2','Lane 3','Lane4'],index=_lap_index)
        return data

    def onExit(self):
        if self.parent is None:
            exit()
        self.parent.show()
        self.hide()

'''------------------> Class for all lap times <----‐-‐-----------------------------------------‐---------------------------------------‐--‐--------‐--------------------------------------------------------‐--'''

class AllLapTimes(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(1080,2170)
        self.parent = parent
        self.header_names = []
        self.total_row = []
        self.heading = QLabel()
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setFont(QFont('Roboto',36))
        self.heading.setStyleSheet('color:white; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.heading.setText('All Races Lap Times')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.table_view = QTableView()
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        #self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(0,205)
        self.table_view.setColumnWidth(1,205)
        self.table_view.setColumnWidth(2,205)
        self.table_view.setColumnWidth(3,205)
        self.table_view.setStyleSheet("QScrollBar:vertical{width:60px;}")
        self.layout.addWidget(self.table_view)
        
        self.button_exit = QPushButton()
        self.button_exit.setStyleSheet('height: 80px;')#('border:2px solid rgb(50,100,90);border-radius:30px;height: 100px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.button_exit.setText("BACK")
        self.button_exit.clicked.connect(self.onExit)
        self.layout.addWidget(self.button_exit)
        self.setLayout(self.layout)
    
    def updateData(self):
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        self.update()
    
    def upDateBackground(self):
        # change background colors
        self.model.data(self.model.rowCount(1) ,role=Qt.BackgroundRole)
    
    def loadData(self):
        _data = []
        _lap_index = []
        ln1, ln2, ln3, ln4 = 0, 0, 0, 0
        filename = 'lap_time_data.csv'
        try:
            with open(fllc.DATABASE_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cnt,laps,lpcnt,nl = 0,0,0,0
                lane1, lane2, lane3, lane4 = "","","",""
                for row in reader:
                    if cnt == 0:
                        if nl > 0:
                            _data.append([self.setValue(lane1, ln1),self.setValue(lane2, ln2),self.setValue(lane3, ln3),self.setValue(lane4, ln4)])
                            _lap_index.append('Total')
                            self.total_row.append(len(_data)-1)
                            lpcnt = 0
                        _data.append([row['lane1'],row['lane2'],row['lane3'],row['lane4']])
                        laps = int(row['date'])
                        _lap_index.append('Name')
                    elif cnt == 1:
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        if lane1 != "":
                            ln1 = int(lane1)
                        else:
                            ln1 = 0
                        if lane2 != "":
                            ln2 = int(lane2)
                        else:
                            ln2 = 0
                        if lane3 != "":
                            ln3 = int(lane3)
                        else:
                            ln3 = 0
                        if lane4 != "":
                            ln4 = int(lane4)
                        else:
                            ln4 = 0
                    elif cnt > 1:
                        _data.append([self.setValue(row['lane1'], lane1),self.setValue(row['lane2'], lane2),self.setValue(row['lane3'], lane3),self.setValue(row['lane4'], lane4)])
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        lpcnt += 1
                        _lap_index.append('Lap '+str(lpcnt))
                    if (cnt-1) == laps:
                        cnt = 0
                        nl += 1
                    else:
                        cnt += 1
            _data.append([self.setValue(lane1, ln1),self.setValue(lane2, ln2),self.setValue(lane3, ln3),self.setValue(lane4, ln4)])
            _lap_index.append('Total')
            csvfile.close()
            
        except FileNotFoundError:
            _data = [[fllc.RACER1NAME,fllc.RACER2NAME,fllc.RACER3NAME,fllc.RACER4NAME],[0.0,0.0,0.0,0.0]]
            _lap_index=['Name','Lap 1']
        
        data = pd.DataFrame(_data, columns=['Lane1','Lane2','Lane 3','Lane4'],index=_lap_index)
        return data

    def setValue(self, value1, value2):
        if value1 == "":
            return 0.0
        return (int(value1) - int(value2))/1000

    def onExit(self):
        if self.parent is None:
            exit()
        self.parent.show()
        self.hide()

'''------------------> Class for 3 lane lap times <----‐-‐-----------------------------------------‐---------------------------------------‐--‐--------‐--------------------------------------------------------‐--'''

class RaceLapTimes(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(1080,2170)
        self.parent = parent
        self.header_names = []
        self.total_row = []
        self.heading = QLabel()
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setFont(QFont('Roboto',36))
        self.heading.setStyleSheet('color:white; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.heading.setText('Race Lap Times')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.table_view = QTableView()
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        #self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(0,210)
        self.table_view.setColumnWidth(1,210)
        self.table_view.setColumnWidth(2,210)
        self.table_view.setColumnWidth(3,210)
        self.table_view.setStyleSheet("QScrollBar:vertical{width:50px;}")
        self.layout.addWidget(self.table_view)
        
        self.button_exit = QPushButton()
        self.button_exit.setStyleSheet('height: 80px;')#('border:2px solid rgb(50,100,90);border-radius:30px;height: 100px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.button_exit.setText('CONTINUE')
        self.button_exit.clicked.connect(self.onExit)
        self.layout.addWidget(self.button_exit)
        self.setLayout(self.layout)
    
    def updateData(self):
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        self.update()
    
    def upDateBackground(self):
        # change background colors
        self.model.data(self.model.rowCount(1) ,role=Qt.BackgroundRole)
    
    def loadData(self):
        _data = []
        _lap_index = []
        ln1, ln2, ln3, ln4 = 0, 0, 0, 0
        filename = 'lap_time_data.csv'
        try:
            with open(fllc.DATABASE_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cnt,laps,lpcnt,nl = 0,0,0,0
                lane1, lane2, lane3, lane4 = "","","",""
                for row in reader:
                    if cnt == 0:
                        if nl > 0:
                            _data.append([self.setValue(lane1, ln1),self.setValue(lane2, ln2),self.setValue(lane3, ln3),self.setValue(lane4, ln4)])
                            _lap_index.append('Total')
                            self.total_row.append(len(_data)-1)
                            lpcnt = 0
                            _data.clear()
                            _lap_index.clear()
                        _data.append([row['lane1'],row['lane2'],row['lane3'],row['lane4']])
                        laps = int(row['date'])
                        _lap_index.append('Name')
                    elif cnt == 1:
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        if lane1 != "":
                            ln1 = int(lane1)
                        else:
                            ln1 = 0.0
                        if lane2 != "":
                            ln2 = int(lane2)
                        else:
                            ln2 = 0.0
                        if lane3 != "":
                            ln3 = int(lane3)
                        else:
                            ln3 = 0.0
                        if lane4 != "":
                            ln4 = int(lane4)
                        else:
                            ln4 = 0.0
                    elif cnt > 1:
                        _data.append([self.setValue(row['lane1'], lane1),self.setValue(row['lane2'], lane2),self.setValue(row['lane3'], lane3),self.setValue(row['lane4'], lane4)])
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        lpcnt += 1
                        _lap_index.append('Lap '+str(lpcnt))
                    if (cnt-1) == laps:
                        cnt = 0
                        nl += 1
                    else:
                        cnt += 1
            _data.append([self.setValue(lane1, ln1),self.setValue(lane2, ln2),self.setValue(lane3, ln3),self.setValue(lane4, ln4)])
            _lap_index.append('Total')
            csvfile.close()
        except FileNotFoundError:
            _data = [[fllc.RACER1NAME,fllc.RACER2NAME,fllc.RACER3NAME,fllc.RACER4NAME],[0.0,0.0,0.0,0.0]]
            _lap_index=['Name','Lap 1']
        
        data = pd.DataFrame(_data, columns=['Lane1','Lane2','Lane 3','Lane4'],index=_lap_index)
        return data

    def setValue(self, value1, value2):
        if value1 == "":
            return 0.0
        return (int(value1) - int(value2))/1000

    def numberOfLanes(self,lane1,lane2,lane3,lane4):
        count = 0
        if lane1 != "":
            count += 1
        if lane2 != "":
            count += 1
        if lane3 != "":
            count += 1
        if lane4 != "":
            count += 1
        return count

    def onExit(self):
        if self.parent is None:
            exit()
        self.parent.show()
        self.hide()

''' ------------------> Class for 1 lane lap times <----‐-‐-----------------------------------------‐---------------------------------------‐--‐--------‐--------------------------------------------------------‐--'''

class LapTimes(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(1080,2170)
        self.parent = parent
        self.header_names = []
        self.total_row = []
        self.heading = QLabel()
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setFont(QFont('Roboto',36))
        self.heading.setStyleSheet('color:white; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.heading.setText('Lap Times')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.heading)
        self.table_view = QTableView()
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        #self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(0,210)
        self.table_view.setColumnWidth(1,210)
        self.table_view.setColumnWidth(2,210)
        self.table_view.setColumnWidth(3,210)
        self.table_view.setStyleSheet("QScrollBar:vertical{width:50px;}")
        self.layout.addWidget(self.table_view)
        
        self.button_exit = QPushButton()
        self.button_exit.setStyleSheet('height: 80px;')#('border:2px solid rgb(50,100,90);border-radius:30px;height: 100px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        self.button_exit.setText('CONTINUE')
        self.button_exit.clicked.connect(self.onExit)
        self.layout.addWidget(self.button_exit)
        self.setLayout(self.layout)

    def updateData(self):
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)
        self.update()
    
    def upDateBackground(self):
        # change background colors
        self.model.data(self.model.rowCount(1) ,role=Qt.BackgroundRole)
    
    def loadData(self):
        _data = []
        _lap_index = []
        ln1, ln2, ln3, ln4 = 0, 0, 0, 0
        filename = 'lap_time_data.csv'
        try:
            with open(fllc.DATABASE_PATH+filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cnt,laps,lpcnt,nl = 0,0,0,0
                lane1, lane2, lane3, lane4 = "","","",""
                row = None
                for row in reader:
                    if cnt == 0:
                        if self.numberOfLanes(row['lane1'],row['lane2'],row['lane3'],row['lane4']) > 1:
                            continue
                        if nl > 0:
                            _data.append([self.setValue(lane1, ln1),self.setValue(lane2, ln2),self.setValue(lane3, ln3),self.setValue(lane4, ln4)])
                            _lap_index.append('Total')
                            self.total_row.append(len(_data)-1)
                            lpcnt = 0
                            _data.clear()
                            _lap_index.clear()
                        if self.numberOfLanes(row['lane1'],row['lane2'],row['lane3'],row['lane4']) > 1:
                            continue
                        _data.append([row['lane1'],row['lane2'],row['lane3'],row['lane4']])
                        laps = int(row['date'])
                        _lap_index.append('Name')
                    elif cnt == 1:
                        if self.numberOfLanes(row['lane1'],row['lane2'],row['lane3'],row['lane4']) > 1:
                            continue
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        if lane1 != "":
                            ln1 = int(lane1)
                        else:
                            ln1 = 0.0
                        if lane2 != "":
                            ln2 = int(lane2)
                        else:
                            ln2 = 0.0
                        if lane3 != "":
                            ln3 = int(lane3)
                        else:
                            ln3 = 0.0
                        if lane4 != "":
                            ln4 = int(lane4)
                        else:
                            ln4 = 0.0
                    elif cnt > 1:
                        if self.numberOfLanes(row['lane1'],row['lane2'],row['lane3'],row['lane4']) > 1:
                            continue
                        _data.append([self.setValue(row['lane1'], lane1),self.setValue(row['lane2'], lane2),self.setValue(row['lane3'], lane3),self.setValue(row['lane4'], lane4)])
                        lane1, lane2, lane3, lane4 = row['lane1'], row['lane2'], row['lane3'], row['lane4']
                        lpcnt += 1
                        _lap_index.append('Lap '+str(lpcnt))
                    if (cnt-1) == laps:
                        cnt = 0
                        nl += 1
                    else:
                        cnt += 1
            if self.numberOfLanes(row['lane1'],row['lane2'],row['lane3'],row['lane4']) > 1:
                raise FileNotFoundError
            _data.append([self.setValue(lane1, ln1),self.setValue(lane2, ln2),self.setValue(lane3, ln3),self.setValue(lane4, ln4)])
            _lap_index.append('Total')
            csvfile.close()
        
        except FileNotFoundError:
            if len(_data) == 0:
                _data = [[fllc.RACER1NAME,fllc.RACER2NAME,fllc.RACER3NAME,fllc.RACER4NAME],[0.0,0.0,0.0,0.0]]
                _lap_index = ['Name','Lap 1']
          
        data = pd.DataFrame(_data, columns=['Lane1','Lane2','Lane 3','Lane4'],index=_lap_index)
        return data

    def onExit(self):
        if self.parent is None:
            exit()
        self.parent.show()
        self.hide()

    def setValue(self, value1, value2):
        if value1 == "":
            return 0.0
        return (int(value1) - int(value2))/1000

    def numberOfLanes(self,lane1,lane2,lane3,lane4):
        count = 0
        if lane1 != "":
            count += 1
        if lane2 != "":
            count += 1
        if lane3 != "":
            count += 1
        if lane4 != "":
            count += 1
        return count
