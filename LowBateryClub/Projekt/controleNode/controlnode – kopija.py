# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ControlNode.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from AirSim_functions import *
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
#import urlib2
#import _thread
#import threading
import time
import cv2
#from numba import njit
import traceback
import os

#@njit   #pohitritev funkcije iskanja kože
def detekcija_koze(slika):
    #result = np.empty((slika.shape[0], slika.shape[1]), dtype=np.bool)
    #result = np.copy(slika)

    #result = []

    x_min = slika.shape[1]
    x_max = 0
    y_min = slika.shape[0]
    y_max = 0
    skin_found = False


    for x in range(len(slika)):
        for y in range(len(slika[x])):
            R, G, B = slika[x][y]

            a = R+G+B

            r = R / a
            g = G / a
            b = B / a

            if (((r / g) > 1.185) and ((r * b) / pow((r + b + g), 2) > 0.107) and ((r * g) / pow((r + b + g),2) > 0.112)):
                skin_found = True
                if (y_min > x):
                    y_min = x
                if (y_max < x):
                    y_max = x
                if (x_min > y):
                    x_min = y
                if (x_max < y):
                    x_max = y

    if (skin_found == False):   #Vrne array z koordinatami bounding boxa
        return np.array([-1,-1,-1,-1])
    else:
        return np.array([x_min,y_min,x_max,y_max])

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.prev = []
        self.Car = None

        #os.remove("img.png")

        #print(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"\img.png"):
          os.remove(os.path.dirname(os.path.abspath(__file__)) + "\img.png")

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1121, 892)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1121, 861))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.connectClick)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 40, 821, 451))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.camera_image = QtWidgets.QLabel(self.groupBox_5)
        self.camera_image.setGeometry(QtCore.QRect(10, 30, 791, 401))
        self.camera_image.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_image.setObjectName("camera_image")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(870, 250, 241, 241))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(100, 30, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser.setFont(font)
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_2.setEnabled(True)
        self.textBrowser_2.setGeometry(QtCore.QRect(100, 80, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setAcceptDrops(False)
        self.textBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_2.setOpenLinks(False)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_3.setEnabled(True)
        self.textBrowser_3.setGeometry(QtCore.QRect(100, 130, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser_3.setFont(font)
        self.textBrowser_3.setAcceptDrops(False)
        self.textBrowser_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_3.setOpenLinks(False)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_4.setEnabled(True)
        self.textBrowser_4.setGeometry(QtCore.QRect(100, 180, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser_4.setFont(font)
        self.textBrowser_4.setAcceptDrops(False)
        self.textBrowser_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_4.setOpenLinks(False)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 500, 1101, 331))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 40, 691, 81))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(210, 30, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(410, 40, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_7.setEnabled(True)
        self.textBrowser_7.setGeometry(QtCore.QRect(470, 30, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser_7.setFont(font)
        self.textBrowser_7.setAcceptDrops(False)
        self.textBrowser_7.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_7.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_7.setOpenLinks(False)
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_6.setEnabled(True)
        self.textBrowser_6.setGeometry(QtCore.QRect(270, 30, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser_6.setFont(font)
        self.textBrowser_6.setAcceptDrops(False)
        self.textBrowser_6.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_6.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_6.setOpenLinks(False)
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_5.setEnabled(True)
        self.textBrowser_5.setGeometry(QtCore.QRect(80, 30, 111, 31))
        font = QtGui.QFont()
        font.setKerning(True)
        self.textBrowser_5.setFont(font)
        self.textBrowser_5.setAcceptDrops(False)
        self.textBrowser_5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_5.setOpenLinks(False)
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 130, 200, 80))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setGeometry(QtCore.QRect(10, 30, 61, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.textBrowser_8 = QtWidgets.QTextBrowser(self.groupBox_6)
        self.textBrowser_8.setGeometry(QtCore.QRect(80, 30, 111, 31))
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setGeometry(QtCore.QRect(220, 130, 230, 80))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setObjectName("groupBox_7")
        self.label_9 = QtWidgets.QLabel(self.groupBox_7)
        self.label_9.setGeometry(QtCore.QRect(10, 30, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.textBrowser_9 = QtWidgets.QTextBrowser(self.groupBox_7)
        self.textBrowser_9.setGeometry(QtCore.QRect(110, 30, 111, 31))
        self.textBrowser_9.setObjectName("textBrowser_9")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_8.setGeometry(QtCore.QRect(460, 130, 240, 80))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setObjectName("groupBox_8")
        self.label_10 = QtWidgets.QLabel(self.groupBox_8)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.textBrowser_10 = QtWidgets.QTextBrowser(self.groupBox_8)
        self.textBrowser_10.setGeometry(QtCore.QRect(110, 30, 110, 31))
        self.textBrowser_10.setObjectName("textBrowser_10")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(870, 40, 241, 201))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsettings_json = QtWidgets.QAction(MainWindow)
        self.actionsettings_json.setObjectName("actionsettings_json")
        self.menuFile.addAction(self.actionsettings_json)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Camera Image"))
        self.camera_image.setText(_translate("MainWindow", "NO IMAGE"))
        self.groupBox.setTitle(_translate("MainWindow", "Car information"))
        self.label.setText(_translate("MainWindow", "Speed:"))
        self.label_2.setText(_translate("MainWindow", "Gear:"))
        self.label_3.setText(_translate("MainWindow", "Rpm:"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Sensors"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Distance"))
        self.label_5.setText(_translate("MainWindow", "Distance:"))
        self.label_6.setText(_translate("MainWindow", "Max dist.:"))
        self.label_7.setText(_translate("MainWindow", "Min dist.:"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Accelometer"))
        self.label_8.setText(_translate("MainWindow", "Pospešek:"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Gyroscope"))
        self.label_9.setText(_translate("MainWindow", "Hitrost vrtenja: "))
        self.groupBox_8.setTitle(_translate("MainWindow", "Magnetometer"))
        self.label_10.setText(_translate("MainWindow", "Moč mag. pol.:"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Car control"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Car"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionsettings_json.setText(_translate("MainWindow", "settings.json"))



    #def zka_to_ne_dela(self):
        #x = Car()
        #y = x.getCarState()
        #self.textBrowser.setText("TEST")
        #count = 0;
        #while (count < 100):
        #    print("thread_name")
        #    count += 1


    def showValues(self, x):
        y = x.getCarState()
        self.textBrowser.setText(y.speed)


    def connectClick(self):
        #print("TEST")
        #x = Car()
        self.Car = Car()
        msg = QMessageBox()
        msg.setWindowTitle("Test")
        msg.setText("Connection failed" if self.Car == False else "Connection succesful")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.exec()
        #if returnValue == QMessageBox.Ok:

        self.thread = CloneThread()
        self.thread.speed.connect(self.change_speed)    #dolocanje spremenljivke speed iz CloneThread razreda
        self.thread.gear.connect(self.change_gear)
        self.thread.rpm.connect(self.change_rpm)
        self.thread.distance.connect(self.change_distance)
        self.thread.max_distance.connect(self.change_max_distance)
        self.thread.min_distance.connect(self.change_min_distance)
        self.thread.acceleration.connect(self.change_acceleration)
        self.thread.sping_velocity.connect(self.change_spin_velocity)
        self.thread.magnet_power.connect(self.change_magnet_power)
        self.thread.image.connect(self.change_image)


        self.thread.start() #začetek threda za pridobivanje informacij


    def change_speed(self, text): #change za textfielde
        self.textBrowser.setText(text)

    def change_gear(self, text):
        self.textBrowser_2.setText(text)

    def change_rpm(self, text):
        self.textBrowser_3.setText(text)

    def change_distance(self, text):
        self.textBrowser_5.setText(text)

    def change_max_distance(self, text):
        self.textBrowser_6.setText(text)

    def change_min_distance(self, text):
        self.textBrowser_7.setText(text)

    def change_acceleration(self, text):
        self.textBrowser_8.setText(text)

    def change_spin_velocity(self, text):
        self.textBrowser_9.setText(text)

    def change_magnet_power(self, text):
        self.textBrowser_10.setText(text)

    def change_image(self, text):
        try:
            image = cv2.imread("img.png")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image = cv2.resize(image, None, fx = 6, fy = 6)

            #Mybe resize image za bolj točne podatke o nahajnu?
            #res = detekcija_koze(image) #Iz slike preberemo kje se nahaja koža

            if (len(self.prev) == 0):
                self.prev = res
            else:
                left_right1 = (res[2]+res[0])/2
                left_right2 = (self.prev[2]+self.prev[0])/2
                difference = left_right1 - left_right2
                if (res[3]-res[1] < self.prev[3]-self.prev[1]): #preveri razliko v višini trenutnega boxa, ter prejšnega boxa
                    #print("Pospeši")
                    #x = Car()
                    #self.Car.goForward(5,0)
                    #if (difference < 0):
                    self.Car.goForward(1,difference)

                else:
                    self.Car.goForward(0,difference)
                    #self.Car.goBreak(1,difference)
                    #self.Car.goReverse(-1, 3, difference, 0)
                    #print("Zavira")

                self.prev = res #zamnjejaj prejšni box, z zdajšnim


            #V res so shranjene koordinate boundingBoxa
            #Na tej točki dodaj preverjanje v katero smer se je tarča premaknila (dodaj global variable v kateri bo shranjena prejšna postavitev v res pa trenutna)
            #Za tem preveri za koliko se je  zmanšal/povečal bouning box (od y_max odstej y_min) ter reagiraj ustrezno glede na to
            #Iz zgornih podatkov kliči funkcije v AirSim_functions filu

            cv2.rectangle(image, (res[0], res[1]), (res[2],res[3]), (255,0,0), 1)   #Narisemo bounding box kjer je bila pojavitev kože



            image = QtGui.QImage(image, image.shape[1], image.shape[0],QtGui.QImage.Format_RGB888)  #Pretvorba slike iz np.ndarray v QImage

            #Izrišemo sliko
            pixmap = QPixmap(image)
            self.camera_image.setScaledContents(True)
            #pixmap4 = pixmap.scaled(500, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.camera_image.setPixmap(pixmap)
        except:
            traceback.print_exc()



class CloneThread(QThread):
    speed = pyqtSignal(str)
    gear = pyqtSignal(str)
    rpm = pyqtSignal(str)
    distance = pyqtSignal(str)
    max_distance = pyqtSignal(str)
    min_distance = pyqtSignal(str)
    acceleration = pyqtSignal(str)
    sping_velocity = pyqtSignal(str)
    magnet_power = pyqtSignal(str)
    image = pyqtSignal(str)


    #signal = pyqtSignal("PyQt_PyObject")
    def __init__(self):
        QThread.__init__(self)
        #self.write_to = ""

    #pyqtSlot()
    def run(self):
        x = Car()

        while (True):
            y = x.getCarState()
            #print(y)
            self.speed.emit(str(y.speed))
            self.gear.emit(str(y.gear))
            self.rpm.emit(str(y.rpm))
            self.acceleration.emit(str(y.kinematics_estimated.angular_acceleration.x_val))

            y = x.getDistanceSensorData()
            self.distance.emit(str(y.distance))
            self.max_distance.emit(str(y.max_distance))
            self.min_distance.emit(str(y.min_distance))

            y = x.getCarState()
            #self.acceleration.emit(str(y.kinematics_estimated.angular_acceleration.x_val))
            #print(y.kinematics_estimated.angular_acceleration.x_val)

            y = x.getSceneImage()
            self.image.emit(str("img.png"))

            time.sleep(0.1)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
