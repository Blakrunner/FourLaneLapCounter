''' 
    Four Lane Lap Counter and Lap Timer

    Setup dialog to enter drivers names for Four Lane Lap Counter and Lap Timer 
    Added in settings for adjustments in the motion detection from the camera.

'''

import csv
from os.path import isfile, join
from os import listdir

from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtGui import QFont, QColor, QKeyEvent, QKeySequence, QPixmap, QIcon
from PyQt5 import QtCore
from Video import fllc

def ReadPresets():
    presets = []
    try:
        for filename in listdir(fllc.PRESET_PATH):
            if isfile(join(fllc.PRESET_PATH, filename)):
                presets.append(filename)
        presets.append("new preset")

    except [FileNotFoundError, FileExistsError]:
        presets = ["new preset"]
    
    return presets


class Setup(QDialog):
    ''' Setup self.racers names and car color '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1080,500)
        self.parent = parent
        self.new_preset = ""
        self.icon_size = QtCore.QSize(96,96)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        heading = QLabel("SETTINGS")
        heading.setAlignment(QtCore.Qt.AlignCenter)
        heading.setStyleSheet("font-size: 30pt; font-weight: 800;color:#FFFFFF; border:4px solid rgb(50,100,90);border-radius:30px;margins:0px;padding:30px;background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #64D2D2, stop: 0.4 #8FEFEF, stop: 0.5 #9AF5F5, stop: 1.0 #2D9797);")
        self.layout.addWidget(heading)
        self.racer1name = QLineEdit()
        self.racer1name.setStyleSheet("background-color: white;")
        self.racer1color = QComboBox()
        self.racer1color.setMinimumContentsLength(7)
        self.racer2name = QLineEdit()
        self.racer2name.setStyleSheet("background-color: white;")
        self.racer2color = QComboBox()
        self.racer2color.setMinimumContentsLength(7)
        self.racer3name = QLineEdit()
        self.racer3name.setStyleSheet("background-color: white;")
        self.racer3color = QComboBox()
        self.racer3color.setMinimumContentsLength(7)
        self.racer4name = QLineEdit()
        self.racer4name.setStyleSheet("background-color: white;")
        self.racer4color = QComboBox()
        self.racer4color.setMinimumContentsLength(7)
        self.delay_input = QLineEdit()
        self.delay_input.setStyleSheet("background-color: white;")
        self.contour_area_input = QLineEdit()
        self.contour_area_input.setStyleSheet("background-color: white;")
        self.anti_shake_min_input = QLineEdit()
        self.anti_shake_min_input.setStyleSheet("background-color: white;")
        self.anti_shake_max_input = QLineEdit()
        self.anti_shake_max_input.setStyleSheet("background-color: white;")
        self.kernal_input_x = QLineEdit()
        self.kernal_input_x.setStyleSheet("background-color: white;")
        self.kernal_input_y = QLineEdit()
        self.kernal_input_y.setStyleSheet("background-color: white;")
        self.range_start = QLineEdit()
        self.range_start.setStyleSheet("background-color: white;")
        self.range_end = QLineEdit()
        self.range_end.setStyleSheet("background-color: white;")
        self.preset_box = QComboBox()
        self.preset_box.setMinimumContentsLength(7)
        self.tabs = QTabWidget()
        self.tabs.addTab(self.RacersSelectionUI(), "Racers Selector")
        self.tabs.addTab(self.MotionDetectionUI(), "Motion Detector")
        self.tabs.addTab(self.AboutUi(), "About")
        self.layout.addWidget(self.tabs)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        cancel_button = QPushButton()
        cancel_button.setFont(QFont('Roboto',20))
        cancel_button.setStyleSheet("width: 250px; color: #3F6F6F; margin-top: 40px; margin-bottom: 40px; margin-left: 40px;")
        cancel_button.setText('CANCEL')
        cancel_button.clicked.connect(self.Cancel)
        button_layout.addWidget(cancel_button)
        save_button = QPushButton()
        save_button.setFont(QFont('Roboto',20))
        save_button.setStyleSheet("width: 250px; color: #3F6F6F; margin-top: 40px; margin-bottom: 40px; margin-left: 40px;")
        save_button.setText('OKAY')
        save_button.clicked.connect(self.SaveSetup)
        button_layout.addWidget(save_button)
        self.layout.addLayout(button_layout)
        self.OnLoad()

    def RacersSelectionUI(self):
        racers_selection_tab = QWidget()
        #racers_selection_tab.setStyleSheet("QComboBox {background-color: white;width:200px;} QComboBox::down-arrow {width: 96px}  QLineEdit {width:200px; border: 2px solid; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #DAF3F3, stop: 0.6 #BCF1F1, stop: 1.0 #8FEFEF);}")
        gridlayout = QGridLayout()
        gridlayout.addWidget(QLabel("racer 1:"),0,0)
        gridlayout.addWidget(self.racer1name,0,1)
        gridlayout.addWidget(QLabel("lane 1 Car color"),0,2)
        self.racer1color.addItem(self.get_icon_from_color(QColor("black")), "Black", userData=QColor(QtCore.Qt.black))
        self.racer1color.addItem(self.get_icon_from_color(QColor("blue")), "Blue", userData=QColor(QtCore.Qt.blue))
        self.racer1color.addItem(self.get_icon_from_color(QColor("darkBlue")), "Dark Blue", userData=QColor(QtCore.Qt.darkBlue))
        self.racer1color.addItem(self.get_icon_from_color(QColor("cyan")), "Cyan", userData=QColor(QtCore.Qt.cyan))
        self.racer1color.addItem(self.get_icon_from_color(QColor("darkCyan")), "Dark Cyan", userData=QColor(QtCore.Qt.darkCyan))
        self.racer1color.addItem(self.get_icon_from_color(QColor("gray")), "Gray", userData=QColor(QtCore.Qt.gray))
        self.racer1color.addItem(self.get_icon_from_color(QColor("darkGray")), "Dark Gray", userData=QColor(QtCore.Qt.darkGray))
        self.racer1color.addItem(self.get_icon_from_color(QColor("lightGray")), "Light Gray", userData=QColor(QtCore.Qt.lightGray))
        self.racer1color.addItem(self.get_icon_from_color(QColor("green")), "Green", userData=QColor(QtCore.Qt.green))
        self.racer1color.addItem(self.get_icon_from_color(QColor("darkGreen")), "Dark Green", userData=QColor(QtCore.Qt.darkGreen))
        self.racer1color.addItem(self.get_icon_from_color(QColor("magenta")), "Magenta", userData=QColor(QtCore.Qt.magenta))
        self.racer1color.addItem(self.get_icon_from_color(QColor("darkMagenta")), "Dark Magenta", userData=QColor(QtCore.Qt.darkMagenta))
        self.racer1color.addItem(self.get_icon_from_color(QColor("red")), "Red", userData=QColor(QtCore.Qt.red))
        self.racer1color.addItem(self.get_icon_from_color(QColor("darkRed")), "Dark Red", userData=QColor(QtCore.Qt.darkRed))
        self.racer1color.addItem(self.get_icon_from_color(QColor("white")), "White", userData=QColor(QtCore.Qt.white))
        self.racer1color.addItem(self.get_icon_from_color(QColor("yellow")), "Yellow", userData = QColor(QtCore.Qt.yellow))
        gridlayout.addWidget(self.racer1color,0,3)
        
        gridlayout.addWidget(QLabel("racer 2:"),1,0)
        gridlayout.addWidget(self.racer2name,1,1)
        gridlayout.addWidget(QLabel("lane 2 Car color"),1,2)
        self.racer2color.addItem(self.get_icon_from_color(QColor("black")), "Black", userData=QColor(QtCore.Qt.black))
        self.racer2color.addItem(self.get_icon_from_color(QColor("blue")), "Blue", userData=QColor(QtCore.Qt.blue))
        self.racer2color.addItem(self.get_icon_from_color(QColor("darkBlue")), "Dark Blue", userData=QColor(QtCore.Qt.darkBlue))
        self.racer2color.addItem(self.get_icon_from_color(QColor("cyan")), "Cyan", userData=QColor(QtCore.Qt.cyan))
        self.racer2color.addItem(self.get_icon_from_color(QColor("darkCyan")), "Dark Cyan", userData=QColor(QtCore.Qt.darkCyan))
        self.racer2color.addItem(self.get_icon_from_color(QColor("gray")), "Gray", userData=QColor(QtCore.Qt.gray))
        self.racer2color.addItem(self.get_icon_from_color(QColor("darkGray")), "Dark Gray", userData=QColor(QtCore.Qt.darkGray))
        self.racer2color.addItem(self.get_icon_from_color(QColor("lightGray")), "Light Gray", userData=QColor(QtCore.Qt.lightGray))
        self.racer2color.addItem(self.get_icon_from_color(QColor("green")), "Green", userData=QColor(QtCore.Qt.green))
        self.racer2color.addItem(self.get_icon_from_color(QColor("darkGreen")), "Dark Green", userData=QColor(QtCore.Qt.darkGreen))
        self.racer2color.addItem(self.get_icon_from_color(QColor("magenta")), "Magenta", userData=QColor(QtCore.Qt.magenta))
        self.racer2color.addItem(self.get_icon_from_color(QColor("darkMagenta")), "Dark Magenta", userData=QColor(QtCore.Qt.darkMagenta))
        self.racer2color.addItem(self.get_icon_from_color(QColor("red")), "Red", userData=QColor(QtCore.Qt.red))
        self.racer2color.addItem(self.get_icon_from_color(QColor("darkRed")), "Dark Red", userData=QColor(QtCore.Qt.darkRed))
        self.racer2color.addItem(self.get_icon_from_color(QColor("white")), "White", userData=QColor(QtCore.Qt.white))
        self.racer2color.addItem(self.get_icon_from_color(QColor("yellow")), "Yellow", userData = QColor(QtCore.Qt.yellow))
        gridlayout.addWidget(self.racer2color,1,3)
        
        gridlayout.addWidget(QLabel("racer 3:"),2,0)
        gridlayout.addWidget(self.racer3name,2,1)
        gridlayout.addWidget(QLabel("lane 3 Car color"),2,2)
        self.racer3color.addItem(self.get_icon_from_color(QColor("black")), "Black", userData=QColor(QtCore.Qt.black))
        self.racer3color.addItem(self.get_icon_from_color(QColor("blue")), "Blue", userData=QColor(QtCore.Qt.blue))
        self.racer3color.addItem(self.get_icon_from_color(QColor("darkBlue")), "Dark Blue", userData=QColor(QtCore.Qt.darkBlue))
        self.racer3color.addItem(self.get_icon_from_color(QColor("cyan")), "Cyan", userData=QColor(QtCore.Qt.cyan))
        self.racer3color.addItem(self.get_icon_from_color(QColor("darkCyan")), "Dark Cyan", userData=QColor(QtCore.Qt.darkCyan))
        self.racer3color.addItem(self.get_icon_from_color(QColor("gray")), "Gray", userData=QColor(QtCore.Qt.gray))
        self.racer3color.addItem(self.get_icon_from_color(QColor("darkGray")), "Dark Gray", userData=QColor(QtCore.Qt.darkGray))
        self.racer3color.addItem(self.get_icon_from_color(QColor("lightGray")), "Light Gray", userData=QColor(QtCore.Qt.lightGray))
        self.racer3color.addItem(self.get_icon_from_color(QColor("green")), "Green", userData=QColor(QtCore.Qt.green))
        self.racer3color.addItem(self.get_icon_from_color(QColor("darkGreen")), "Dark Green", userData=QColor(QtCore.Qt.darkGreen))
        self.racer3color.addItem(self.get_icon_from_color(QColor("magenta")), "Magenta", userData=QColor(QtCore.Qt.magenta))
        self.racer3color.addItem(self.get_icon_from_color(QColor("darkMagenta")), "Dark Magenta", userData=QColor(QtCore.Qt.darkMagenta))
        self.racer3color.addItem(self.get_icon_from_color(QColor("red")), "Red", userData=QColor(QtCore.Qt.red))
        self.racer3color.addItem(self.get_icon_from_color(QColor("darkRed")), "Dark Red", userData=QColor(QtCore.Qt.darkRed))
        self.racer3color.addItem(self.get_icon_from_color(QColor("white")), "White", userData=QColor(QtCore.Qt.white))
        self.racer3color.addItem(self.get_icon_from_color(QColor("yellow")), "Yellow", userData = QColor(QtCore.Qt.yellow))
        gridlayout.addWidget(self.racer3color,2,3)
        
        gridlayout.addWidget(QLabel("racer 4:"),3,0)
        gridlayout.addWidget(self.racer4name,3,1)
        gridlayout.addWidget(QLabel("lane 4 Car color"),3,2)
        self.racer4color.addItem(self.get_icon_from_color(QColor("black")), "Black", userData=QColor(QtCore.Qt.black))
        self.racer4color.addItem(self.get_icon_from_color(QColor("blue")), "Blue", userData=QColor(QtCore.Qt.blue))
        self.racer4color.addItem(self.get_icon_from_color(QColor("darkBlue")), "Dark Blue", userData=QColor(QtCore.Qt.darkBlue))
        self.racer4color.addItem(self.get_icon_from_color(QColor("cyan")), "Cyan", userData=QColor(QtCore.Qt.cyan))
        self.racer4color.addItem(self.get_icon_from_color(QColor("darkCyan")), "Dark Cyan", userData=QColor(QtCore.Qt.darkCyan))
        self.racer4color.addItem(self.get_icon_from_color(QColor("gray")), "Gray", userData=QColor(QtCore.Qt.gray))
        self.racer4color.addItem(self.get_icon_from_color(QColor("darkGray")), "Dark Gray", userData=QColor(QtCore.Qt.darkGray))
        self.racer4color.addItem(self.get_icon_from_color(QColor("lightGray")), "Light Gray", userData=QColor(QtCore.Qt.lightGray))
        self.racer4color.addItem(self.get_icon_from_color(QColor("green")), "Green", userData=QColor(QtCore.Qt.green))
        self.racer4color.addItem(self.get_icon_from_color(QColor("darkGreen")), "Dark Green", userData=QColor(QtCore.Qt.darkGreen))
        self.racer4color.addItem(self.get_icon_from_color(QColor("magenta")), "Magenta", userData=QColor(QtCore.Qt.magenta))
        self.racer4color.addItem(self.get_icon_from_color(QColor("darkMagenta")), "Dark Magenta", userData=QColor(QtCore.Qt.darkMagenta))
        self.racer4color.addItem(self.get_icon_from_color(QColor("red")), "Red", userData=QColor(QtCore.Qt.red))
        self.racer4color.addItem(self.get_icon_from_color(QColor("darkRed")), "Dark Red", userData=QColor(QtCore.Qt.darkRed))
        self.racer4color.addItem(self.get_icon_from_color(QColor("white")), "White", userData=QColor(QtCore.Qt.white))
        self.racer4color.addItem(self.get_icon_from_color(QColor("yellow")), "Yellow", userData = QColor(QtCore.Qt.yellow))
        gridlayout.addWidget(self.racer4color,3,3)
        
        racers_selection_tab.setLayout(gridlayout)
        return racers_selection_tab
    
    def MotionDetectionUI(self):
        motion_detection_tab = QWidget()
        #motion_detection_tab.setStyleSheet("QComboBox {background-color: white;} QComboBox::down-arrow {width: 96px} QLineEdit {width:200px; border: 2px solid; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #DAF3F3, stop: 0.6 #BCF1F1, stop: 1.0 #8FEFEF);}")
        gridlayout = QGridLayout()
        gridlayout.addWidget(QLabel("Anti Min"),0,0)
        gridlayout.addWidget(self.anti_shake_min_input,0,1)
        gridlayout.addWidget(QLabel("Kernal"),0,2) 
        self.kernal_input_x.textChanged.connect(self.onChangeText)
        #self.range_start.editingFinished.connect(self.onChangeText)
        gridlayout.addWidget(self.kernal_input_x,0,3)
        gridlayout.addWidget(self.kernal_input_y,0,4)
        
        gridlayout.addWidget(QLabel("Anti Max"),1,0)
        gridlayout.addWidget(self.anti_shake_max_input,1,1)
        gridlayout.addWidget(QLabel("Range"),1,2)
        gridlayout.addWidget(self.range_start,1,3)
        gridlayout.addWidget(self.range_end,1,4)
        
        gridlayout.addWidget(QLabel("Delay"),2,0)
        gridlayout.addWidget(self.delay_input,2,1)
        gridlayout.addWidget(QLabel("Contour"),2,2)
        gridlayout.addWidget(self.contour_area_input,2,3)
        
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Select/Create New Presets"))
        self.preset_box.setEditable(True)
        self.preset_box.setStyleSheet("background-color: white;")
        preset_list = ReadPresets()
        for preset in preset_list:
            self.preset_box.addItem(preset.replace(".csv", ""),userData=preset)
        self.preset_box.currentIndexChanged.connect(self.OnIndexChanged)
        #self.preset_box.editTextChanged.connect(self.OnTextChanged)
        preset_layout.addWidget(self.preset_box)
        gridlayout.addLayout(preset_layout,3,0,4,5)
        
        motion_detection_tab.setLayout(gridlayout)
        return motion_detection_tab

    def AboutUi(self):
        about_tab = QWidget()
        layout = QVBoxLayout()
        heading = QLabel("<b>Four Lane Lap Counter & Lap Timer</b>")
        heading.setFont(QFont('Roboto',16))
        heading.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(heading)
        version_label = QLabel()
        version_label.setAlignment(QtCore.Qt.AlignCenter)
        version_label.setFont(QFont('Roboto',10))
        version_label.setText("version 1.0.0   created by <b><i>Budgel</i></b>")
        layout.addWidget(version_label)
        description = QTextEdit()
        description.setReadOnly(True)
        description.setFont(QFont('Roboto',12))
        description.setStyleSheet("background-color: white")
        description.setAlignment(QtCore.Qt.AlignCenter)
        description.setText(fllc.about_text)
        layout.addWidget(description)
        about_tab.setLayout(layout)
        return about_tab

    def onChangeText(self):
        tex = self.kernal_input_x.text()
        self.kernal_input_y.setText("")
        self.kernal_input_y.setText(tex)

    def get_icon_from_color(self, color):
        pixmap = QPixmap(100, 100)
        pixmap.fill(color)
        return QIcon(pixmap)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == QKeySequence.Backspace:
                self.emit(QtCore.SIGNAL(self.Cancel))
    
    def SaveNewPreset(self):
        new_preset = self.preset_box.currentText()
        new_preset = new_preset+".csv"
        self.new_preset = new_preset
        fllc.PRESET_TEXT = new_preset
        fllc.PRESET_INDEX = self.preset_box.currentIndex()
        fllc.save(new_preset)
    
    def Cancel(self):
        if self.parent is None:
            exit()
        self.parent.show()
        self.reject()

    def SaveSetup(self):
        if self.parent is None:
            exit()
        self.SaveNewPreset()
        self.SaveCSV()
        fllc.saveSettings()
        self.parent.show()
        self.reject()
    
    def OnIndexChanged(self):
        next_preset = self.preset_box.currentData()
        if next_preset == "new preset":
            return
        fllc.loadSetting(next_preset)
        self.delay_input.clear()
        self.contour_area_input.clear()
        self.anti_shake_min_input.clear()
        self.anti_shake_max_input.clear()
        self.kernal_input_x.clear()
        self.kernal_input_y.clear()
        self.range_start.clear()
        self.range_end.clear()
        self.delay_input.setText(str(fllc.DELAY))
        self.contour_area_input.setText(str(fllc.CONTOUR_AREA))
        self.anti_shake_min_input.setText(str(fllc.ANTI_SHAKE_MIN))
        self.anti_shake_max_input.setText(str(fllc.ANTI_SHAKE_MAX))
        self.kernal_input_x.setText(str(fllc.KERNAL[0]))
        self.kernal_input_y.setText(str(fllc.KERNAL[1]))
        self.range_start.setText(str(fllc.RANGE_START))
        self.range_end.setText(str(fllc.RANGE_END))
        self.update()
        
    
    def OnTextChanged(self):
        self.new_preset = self.preset_box.currentText()
        return
    
    def OnLoad(self):
        filename = "drivers.csv"
        try:
            with open(fllc.DATABASE_PATH+filename,'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cnt = 0
                for row in reader:
                    if cnt == 0:
                        self.racer1name.insert(row['name'])
                        self.racer1color.setCurrentText(row['color'])
                    if cnt == 1:
                        self.racer2name.insert(row['name'])
                        self.racer2color.setCurrentText(row['color'])
                    if cnt == 2:
                        self.racer3name.insert(row['name'])
                        self.racer3color.setCurrentText(row['color'])
                    if cnt == 3:
                        self.racer4name.insert(row['name'])
                        self.racer4color.setCurrentText(row['color'])
                    cnt += 1
            csvfile.close()
            fllc.RACER1.clear()
            fllc.RACER2.clear()
            fllc.RACER3.clear()
            fllc.RACER4.clear()
            fllc.RACER1NAME = self.racer1name.text()
            fllc.RACER2NAME = self.racer2name.text()
            fllc.RACER3NAME = self.racer3name.text()
            fllc.RACER4NAME = self.racer4name.text()
            fllc.RACER1CARCOLOR = self.racer1color.currentData()
            fllc.RACER2CARCOLOR = self.racer2color.currentData()
            fllc.RACER3CARCOLOR = self.racer3color.currentData()
            fllc.RACER4CARCOLOR = self.racer4color.currentData()
            self.delay_input.setText(str(fllc.DELAY))
            self.contour_area_input.setText(str(fllc.CONTOUR_AREA))
            self.anti_shake_min_input.setText(str(fllc.ANTI_SHAKE_MIN))
            self.anti_shake_max_input.setText(str(fllc.ANTI_SHAKE_MAX))
            self.kernal_input_x.setText(str(fllc.KERNAL[0]))
            self.kernal_input_y.setText(str(fllc.KERNAL[1]))
            self.range_start.setText(str(fllc.RANGE_START))
            self.range_end.setText(str(fllc.RANGE_END))
            self.preset_box.setCurrentIndex(fllc.PRESET_INDEX)
            self.parent.child_racing.child_camera.setTimerDelay(fllc.DELAY)
            return
        except FileNotFoundError:
            self.delay_input.setText(str(fllc.DELAY))
            self.contour_area_input.setText(str(fllc.CONTOUR_AREA))
            self.anti_shake_min_input.setText(str(fllc.ANTI_SHAKE_MIN))
            self.anti_shake_max_input.setText(str(fllc.ANTI_SHAKE_MAX))
            self.kernal_input_x.setText(str(fllc.KERNAL[0]))
            self.kernal_input_y.setText(str(fllc.KERNAL[1]))
            self.range_start.setText(str(fllc.RANGE_START))
            self.range_end.setText(str(fllc.RANGE_END))
            self.preset_box.setCurrentIndex(fllc.PRESET_INDEX)
            self.parent.child_racing.child_camera.setTimerDelay(fllc.DELAY)
            return


    def SaveCSV(self):
        filename = "drivers.csv"
        with open(fllc.DATABASE_PATH+filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'color']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({'name':self.racer1name.text(), 'color':self.racer1color.currentText()})
            writer.writerow({'name':self.racer2name.text(), 'color':self.racer2color.currentText()})
            writer.writerow({'name':self.racer3name.text(), 'color':self.racer3color.currentText()})
            writer.writerow({'name':self.racer4name.text(), 'color':self.racer4color.currentText()})
        csvfile.close()
        fllc.RACER1.clear()
        fllc.RACER2.clear()
        fllc.RACER3.clear()
        fllc.RACER4.clear()
        fllc.RACER1STARTED = False
        fllc.RACER2STARTED = False
        fllc.RACER3STARTED = False
        fllc.RACER4STARTED = False
        fllc.RACER1NAME = self.racer1name.text()
        fllc.RACER2NAME = self.racer2name.text()
        fllc.RACER3NAME = self.racer3name.text()
        fllc.RACER4NAME = self.racer4name.text()
        fllc.RACER1CARCOLOR = self.racer1color.currentData()
        fllc.RACER2CARCOLOR = self.racer2color.currentData()
        fllc.RACER3CARCOLOR = self.racer3color.currentData()
        fllc.RACER4CARCOLOR = self.racer4color.currentData()
        fllc.DELAY = int(self.delay_input.text())
        fllc.CONTOUR_AREA = int(self.contour_area_input.text())
        fllc.ANTI_SHAKE_MIN = int(self.anti_shake_min_input.text())
        fllc.ANTI_SHAKE_MAX = int(self.anti_shake_max_input.text())
        fllc.KERNAL = int(self.kernal_input_x.text()), int(self.kernal_input_y.text())
        fllc.RANGE_START = int(self.range_start.text())
        fllc.RANGE_END = int(self.range_end.text())
        fllc.PRESET_INDEX = self.preset_box.currentIndex()
        fllc.save(self.new_preset)
        self.parent.child_racing.child_camera.setTimerDelay(fllc.DELAY)
        return
