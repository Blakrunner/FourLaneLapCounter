'''
    Four lane lap counter and lap timer
    
    Leaderboard for Championship racing

'''
import sys
import os
from operator import itemgetter, attrgetter
import csv
import pandas as pd

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTableView
)
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
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
                
            if isinstance(value, float):
                return Qt.AlignVCenter + Qt.AlignRight
            
            if isinstance(value, str):
                return Qt.AlignCenter
            else:
                return Qt.AlignVCenter + Qt.AlignRight

        if role == Qt.BackgroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, str):
                if value == fllc.RACER1NAME:
                    return fllc.RACER1CARCOLOR
                elif value == fllc.RACER2NAME:
                    return fllc.RACER2CARCOLOR
                elif value == fllc.RACER3NAME:
                    return fllc.RACER3CARCOLOR
                elif value == fllc.RACER4NAME:
                    return fllc.RACER4CARCOLOR
            if index.row() == 1:
                return QColor(183,243,243)
            if index.row() == 2:
                return QColor(193,253,253)
            if index.row() == 3:
                return QColor(183,243,243)
            if index.row() == 4:
                return QColor(193,253,253)
            return QColor(203,253,253)

        if role == Qt.ForegroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value,str):
                if value == fllc.RACER4NAME:
                    if self.isColorMatch(fllc.RACER4CARCOLOR):
                        return QColor(Qt.black)
                if value == fllc.RACER3NAME:
                    if self.isColorMatch(fllc.RACER3CARCOLOR):
                        return QColor(Qt.black)
                if value == fllc.RACER2NAME:
                    if self.isColorMatch(fllc.RACER2CARCOLOR):
                        return QColor(Qt.black)
                if value == fllc.RACER1NAME:
                    if self.isColorMatch(fllc.RACER1CARCOLOR):
                        return QColor(Qt.black)
                return QColor(Qt.white)

        if role == Qt.DecorationRole:
            value = self._data.iloc[index.row()][index.column()]
            if isinstance(value, str):
                if value == fllc.RACER1NAME:
                    if self.isColorMatch(fllc.RACER1CARCOLOR): 
                        return QIcon('images/racerBlack.png')
                    if self.isColorMatch(fllc.RACER2CARCOLOR): 
                        return QIcon('images/racerBlack.png')
                    if self.isColorMatch(fllc.RACER3CARCOLOR): 
                        return QIcon('images/racerBlack.png')
                    if self.isColorMatch(fllc.RACER4CARCOLOR): 
                        return QIcon('images/racerBlack.png')
                return QIcon('images/racerRed.png')

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

    def get_icon_from_color(self, color):
        pixmap = QPixmap(100, 100)
        pixmap.fill(color)
        return QIcon(pixmap)

    def isColorMatch(self, color):
        if color == QColor(Qt.yellow):
            return True
        elif color == QColor(Qt.white):
            return True
        elif color == QColor(Qt.lightGray):
            return True
        elif color == QColor(Qt.gray):
            return True
        elif color == QColor(Qt.red):
            return True
        return False

class Leaderboard(QDialog):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.resize(1060,678)
        heading = QLabel()
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(QFont('Roboto', 26))
        heading.setStyleSheet('color:#FFFFFF; border:4px solid rgb(50,100,90);border-radius:30px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        heading.setText('Championship Leaderboard')
        layout = QVBoxLayout()
        layout.addWidget(heading)
        self.table = QTableView()
        self.table.resize(980,1820)
        data = self.loadData()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        #self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0,300)
        self.table.setColumnWidth(1,105)
        self.table.setColumnWidth(2,300)
        self.table.setColumnWidth(3,170)
        layout.addWidget(self.table)
        button_layout = QHBoxLayout()
        button_cancel = QPushButton()
        button_cancel.setStyleSheet('height: 100px;')
        button_cancel.setText("CANCEL")
        button_cancel.clicked.connect(self.onCancel)
        button_layout.addWidget(button_cancel)
        button_continue = QPushButton()
        button_continue.setStyleSheet('height: 100px;')#('border:2px solid rgb(50,100,90);border-radius:30px;height: 100px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);')
        button_continue.setText('CONTINUE')
        button_continue.clicked.connect(self.onContinue)
        button_layout.addWidget(button_continue)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def loadData(self):
        _data = []
        filename = "lbdata.csv"
        indexes = ['Rank 1','Rank 2','Rank 3','Rank 4']
        columns = [" Driver Name ", "Lane"," BestLap Time ", "Points"]
        try:
            with open(fllc.DATABASE_PATH+filename,'r', newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                cnt = 0
                for row in reader:
                    cnt += 1
                    _data.append([row["name"], int(row["lane"]), int(row["bestLap"])/1000, int(row["points"])])
        except FileNotFoundError:
            _data = [["none",0,0.0,0],["none",0,0.0,0],["none",0,0.0,0],["none",0,0.0,0]]
            
        datasorted = sorted(_data, key=itemgetter(3), reverse=True)
        data = pd.DataFrame(datasorted,columns=columns,index=indexes)
        return data

    def updateData(self):
        self.data = self.loadData()
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        self.update()

    def onCancel(self):
        self.parent.cancel = True
        self.parent.show()
        self.hide()

    def onContinue(self):
        if self.parent is None:
            exit()
        self.parent.show()
        self.hide()
