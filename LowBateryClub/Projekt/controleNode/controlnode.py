# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ControlNode.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from AirSim_functions import *
from STM32F411 import *
from RemoteControle import *
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
import socket
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
#import urlib2
#import _thread
#import threading
import time
import cv2
from numba import jit
import traceback
import os

@jit(nopython=True)  #pohitritev funkcije iskanja kože
def detekcija_koze(slika):
    #result = np.empty((slika.shape[0], slika.shape[1]), dtype=np.bool)
    #result = np.copy(slika)

    #result = []

    #print(slika)

    x_min = slika.shape[1]
    x_max = 0
    y_min = slika.shape[0]
    y_max = 0
    skin_found = False

    height, width, channels = slika.shape
    #a = 1

#    try:
    for x in range(len(slika)):
        for y in range(len(slika[x])):

            if (y < width/2 - 10 or y > width/2 + 10 or x > height/2):
                continue

            R, G, B = slika[x][y]


            a = R + G + B

            r = R / a
            g = G / a
            b = B / a

            #print(a)

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
#    except:
#        return np.array([-1,-1,-1,-1])

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
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 100, 23))
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
        font.setPointSize(14)
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
        font.setPointSize(14)
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
        font.setPointSize(14)
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
        font.setPointSize(14)
        font.setKerning(True)
        self.textBrowser_4.setFont(font)
        self.textBrowser_4.setAcceptDrops(False)
        self.textBrowser_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_4.setOpenLinks(False)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 500, 741, 331))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 40, 720, 81))
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
        self.label_7.setGeometry(QtCore.QRect(410, 40, 51, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_7.setEnabled(True)
        self.textBrowser_7.setGeometry(QtCore.QRect(470, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
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
        font.setPointSize(13)
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
        font.setPointSize(13)
        font.setKerning(True)
        self.textBrowser_5.setFont(font)
        self.textBrowser_5.setAcceptDrops(False)
        self.textBrowser_5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_5.setOpenLinks(False)
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 130, 210, 80))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setGeometry(QtCore.QRect(10, 30, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.textBrowser_8 = QtWidgets.QTextBrowser(self.groupBox_6)
        self.textBrowser_8.setGeometry(QtCore.QRect(90, 30, 111, 31))
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setGeometry(QtCore.QRect(230, 130, 240, 80))
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
        self.groupBox_8.setGeometry(QtCore.QRect(480, 130, 250, 80))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setObjectName("groupBox_8")
        self.label_10 = QtWidgets.QLabel(self.groupBox_8)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.textBrowser_10 = QtWidgets.QTextBrowser(self.groupBox_8)
        self.textBrowser_10.setGeometry(QtCore.QRect(130, 30, 110, 31))
        self.textBrowser_10.setObjectName("textBrowser_10")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(870, 40, 241, 201))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton.setGeometry(QtCore.QRect(10, 40, 171, 19))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 70, 221, 19))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.toggled.connect(self.radioButton_2Changed)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 100, 151, 19))
        self.radioButton_3.setObjectName("radioButton_3")
#        self.radioButton_3.toggled.connect(self.radioButton_3Changed)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 130, 211, 19))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.toggled.connect(self.radioButton_4Changed)
        self.groupBox_9 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_9.setGeometry(QtCore.QRect(750, 509, 361, 321))
        self.groupBox_9.setObjectName("groupBox_9")
        font.setPointSize(14)
        self.groupBox_9.setFont(font)
        self.groupBox_10 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_10.setGeometry(QtCore.QRect(10, 30, 341, 80))
        self.groupBox_10.setObjectName("groupBox_10")
        font.setPointSize(10)
        self.groupBox_10.setFont(font)
        self.textBrowser_11 = QtWidgets.QTextBrowser(self.groupBox_10)
        self.textBrowser_11.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.textBrowser_11.setObjectName("textBrowser_11")
        self.textBrowser_12 = QtWidgets.QTextBrowser(self.groupBox_10)
        self.textBrowser_12.setGeometry(QtCore.QRect(120, 30, 101, 31))
        self.textBrowser_12.setObjectName("textBrowser_12")
        self.textBrowser_13 = QtWidgets.QTextBrowser(self.groupBox_10)
        self.textBrowser_13.setGeometry(QtCore.QRect(230, 30, 101, 31))
        self.textBrowser_13.setObjectName("textBrowser_13")
        self.groupBox_11 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_11.setGeometry(QtCore.QRect(10, 120, 341, 80))
        self.groupBox_11.setObjectName("groupBox_11")
        font.setPointSize(10)
        self.groupBox_11.setFont(font)
        self.textBrowser_14 = QtWidgets.QTextBrowser(self.groupBox_11)
        self.textBrowser_14.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.textBrowser_14.setObjectName("textBrowser_14")
        self.textBrowser_15 = QtWidgets.QTextBrowser(self.groupBox_11)
        self.textBrowser_15.setGeometry(QtCore.QRect(120, 30, 101, 31))
        self.textBrowser_15.setObjectName("textBrowser_15")
        self.textBrowser_16 = QtWidgets.QTextBrowser(self.groupBox_11)
        self.textBrowser_16.setGeometry(QtCore.QRect(230, 30, 101, 31))
        self.textBrowser_16.setObjectName("textBrowser_16")
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_12.setGeometry(QtCore.QRect(10, 210, 341, 80))
        self.groupBox_12.setObjectName("groupBox_12")
        font.setPointSize(10)
        self.groupBox_12.setFont(font)
        self.textBrowser_17 = QtWidgets.QTextBrowser(self.groupBox_12)
        self.textBrowser_17.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.textBrowser_17.setObjectName("textBrowser_17")
        self.textBrowser_18 = QtWidgets.QTextBrowser(self.groupBox_12)
        self.textBrowser_18.setGeometry(QtCore.QRect(120, 30, 101, 31))
        self.textBrowser_18.setObjectName("textBrowser_18")
        self.textBrowser_19 = QtWidgets.QTextBrowser(self.groupBox_12)
        self.textBrowser_19.setGeometry(QtCore.QRect(230, 30, 101, 31))
        self.textBrowser_19.setObjectName("textBrowser_19")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 20))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Kontrolno vozlišče"))
        self.pushButton.setText(_translate("MainWindow", "Poveži v Unity"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Slika"))
        self.camera_image.setText(_translate("MainWindow", "NO IMAGE"))
        self.groupBox.setTitle(_translate("MainWindow", "Podatki avtomobila"))
        self.label.setText(_translate("MainWindow", "Hitrost:"))
        self.label_2.setText(_translate("MainWindow", "Prestava:"))
        self.label_3.setText(_translate("MainWindow", "Obrati:"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Senzorji avtomobila"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Senzor razdalje"))
        self.label_5.setText(_translate("MainWindow", "Razdalja:"))
        self.label_6.setText(_translate("MainWindow", "Max dist.:"))
        self.label_7.setText(_translate("MainWindow", "Min dist.:"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Pospeškometer"))
        self.label_8.setText(_translate("MainWindow", "Pospešek:"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Žiroskop"))
        self.label_9.setText(_translate("MainWindow", "Speed of rot.:"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Magnetometer"))
        self.label_10.setText(_translate("MainWindow", "Moč polja.:"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Nadzor avtomobila"))
        self.radioButton.setText(_translate("MainWindow", "Prikaz podatkov"))
        self.radioButton_2.setText(_translate("MainWindow", "Vožnja s PPM signalom"))
        self.radioButton_3.setText(_translate("MainWindow", "Sledenje tarči"))
        self.radioButton_4.setText(_translate("MainWindow", "Vožnja preko ploščice"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Podatki ploščice"))
        self.groupBox_10.setTitle(_translate("MainWindow", "Pospeškometer"))
        self.groupBox_11.setTitle(_translate("MainWindow", "Magnetometer"))
        self.groupBox_12.setTitle(_translate("MainWindow", "Žiroskop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
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
#        msg = QMessageBox()
#        msg.setWindowTitle("Test")
#        msg.setText("Connection failed" if self.Car == False else "Connection succesful")
#        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

#        msg.exec()
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

#        self.thread.mag_x.connect(self.change_mag_x)
#        self.thread.mag_y.connect(self.change_mag_y)
#        self.thread.mag_z.connect(self.change_mag_z)
#        self.thread.acc_x.connect(self.change_acc_x)
#        self.thread.acc_y.connect(self.change_acc_y)
#        self.thread.acc_z.connect(self.change_acc_z)
#        self.thread.gyro_x.connect(self.change_gyro_x)
#        self.thread.gyro_y.connect(self.change_gyro_y)
#        self.thread.gyro_z.connect(self.change_gyro_z)

        self.thread.start() #začetek threda za pridobivanje informacij

        self.thread2 = ThreadSTM()
        self.thread2.mag_x.connect(self.change_mag_x)
        self.thread2.mag_y.connect(self.change_mag_y)
        self.thread2.mag_z.connect(self.change_mag_z)
        self.thread2.acc_x.connect(self.change_acc_x)
        self.thread2.acc_y.connect(self.change_acc_y)
        self.thread2.acc_z.connect(self.change_acc_z)
        self.thread2.gyro_x.connect(self.change_gyro_x)
        self.thread2.gyro_y.connect(self.change_gyro_y)
        self.thread2.gyro_z.connect(self.change_gyro_z)

        self.thread2.start()

        self.thread2.setCar(self.Car)

        #self.thread3 = PPMSignalThread()
        #self.thread3.start()


    def radioButton_2Changed(self):
        if (self.radioButton_2.isChecked() == True):
            self.thread3 = PPMSignalThread()
            self.thread3.start()
            self.thread3.changedButton(self.radioButton_2.isChecked())

        else:
            print("quit")
            self.thread3.quit()
        #self.thread3.changedButton(self.radioButton_2.isChecked())

    def radioButton_3Changed(self):
        self.thread.changedButton(self.radioButton_3.isChecked())

    def radioButton_4Changed(self):
        self.thread2.changedButton(self.radioButton_4.isChecked())


    def change_mag_x(self, text):
        self.textBrowser_14.setText(text)

    def change_mag_y(self, text):
        self.textBrowser_15.setText(text)

    def change_mag_z(self, text):
        self.textBrowser_16.setText(text)

    def change_acc_x(self, text):
        self.textBrowser_11.setText(text)

    def change_acc_y(self, text):
        self.textBrowser_12.setText(text)

    def change_acc_z(self, text):
        self.textBrowser_13.setText(text)

    def change_gyro_x(self, text):
        self.textBrowser_17.setText(text)

    def change_gyro_y(self, text):
        self.textBrowser_18.setText(text)

    def change_gyro_z(self, text):
        self.textBrowser_19.setText(text)


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

#            image = cv2.resize(image, None, fx = 6, fy = 6)

            #Mybe resize image za bolj točne podatke o nahajnu?
            height, width, channels = image.shape
            res = detekcija_koze(image) #Iz slike preberemo kje se nahaja koža

            #print(res)
            #res = [-1,-1]

            if (len(res) == 4):
                if (res[0] != -1):
                    if (len(self.prev) == 0):
                        self.prev = res
                    else:
                        left_right1 = (res[2]+res[0])/2
                        left_right2 = (self.prev[2]+self.prev[0])/2
                        difference = left_right1 - left_right2

                        height, width, channels = image.shape
                        width /= 2

                        if (self.radioButton_3.isChecked()):
                            #print("Vožnja za tarčo")
                            if (res[3]-res[1] < self.prev[3]-self.prev[1]): #preveri razliko v višini trenutnega boxa, ter prejšnega boxa
                                #print("Pospeši")
                                #x = Car()
                                #self.Car.goForward(5,0)
                                #if (difference < 0):
                                #self.Car.goForward(1,difference)
                                self.Car.goForward(30,left_right1 - width)

                            else:
                                #self.Car.goForward(0,difference)
                                self.Car.goForward(0,left_right1 - width)
                                #self.Car.goBreak(1,difference)
                                #self.Car.goReverse(-1, 3, difference, 0)
                                #print("Zavira")

                        self.prev = res #zamnjejaj prejšni box, z zdajšnim


            #V res so shranjene koordinate boundingBoxa
            #Na tej točki dodaj preverjanje v katero smer se je tarča premaknila (dodaj global variable v kateri bo shranjena prejšna postavitev v res pa trenutna)
            #Za tem preveri za koliko se je  zmanšal/povečal bouning box (od y_max odstej y_min) ter reagiraj ustrezno glede na to
            #Iz zgornih podatkov kliči funkcije v AirSim_functions filu

            if (len(res) == 4):
                if (res[0] != -1):
                    cv2.rectangle(image, (res[0], res[1]), (res[2],res[3]), (255,0,0), 1)   #Narisemo bounding box kjer je bila pojavitev kože



            image = QtGui.QImage(image, image.shape[1], image.shape[0],QtGui.QImage.Format_RGB888)  #Pretvorba slike iz np.ndarray v QImage

            #Izrišemo sliko
            pixmap = QPixmap(image)
            self.camera_image.setScaledContents(True)
            #pixmap4 = pixmap.scaled(500, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.camera_image.setPixmap(pixmap)
        except:
            traceback.print_exc()

class ThreadSTM(QThread):
    mag_x = pyqtSignal(str)
    mag_y = pyqtSignal(str)
    mag_z = pyqtSignal(str)
    acc_x = pyqtSignal(str)
    acc_y = pyqtSignal(str)
    acc_z = pyqtSignal(str)
    gyro_x = pyqtSignal(str)
    gyro_y = pyqtSignal(str)
    gyro_z = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.radioButton = False
        self.car = Car()

    def run(self):
        stm32f411 = STM32F411()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 65432))
            s.listen(1)
            conn,addr = s.accept()

        while (True):
            if (stm32f411.is_sensor_open()):
                msg = stm32f411.read_line_from_port()

                conn.sendall(msg)
                msg = msg.decode("utf-8").replace("\n", "").replace("\r", "").split(",")

                self.mag_x.emit(str(msg[0]))
                self.mag_y.emit(str(msg[1]))
                self.mag_z.emit(str(msg[2]))
                self.acc_x.emit(str(msg[3]))
                self.acc_y.emit(str(msg[4]))
                self.acc_z.emit(str(msg[5]))
                self.gyro_x.emit(str(msg[6]))
                self.gyro_y.emit(str(msg[7]))
                self.gyro_z.emit(str(msg[8]))

                if (self.radioButton == True):
                    if (float(msg[8]) > 5.0 or float(msg[8]) < -5.0):
                        self.car.goForward(0,float(msg[8]) * -1)
                    else:
                        self.car.goForward(0,0)

                    if(float(msg[7]) > 5.0):
                        self.car.goForward(0, 0)

                    if(float(msg[7]) < -5.0):
                        self.car.goForward(10, 0)

            else:
                conn.sendall(bytes(",", 'utf-8'))

    def changedButton(self, value):
        #print(value)
        self.radioButton = value


    def setCar(self, car):
        self.car = car


class PPMSignalThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.radioButton = False
        self.ppmsignal = PPM_Signal()

    def run(self):

        while(True):
            if (self.radioButton == True):
                self.ppmsignal.run()

    def changedButton(self, value):
        print(value)
        self.radioButton = value

    def quit(self):
        self.terminate()


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
    mag_x = pyqtSignal(str)
    mag_y = pyqtSignal(str)
    mag_z = pyqtSignal(str)
    acc_x = pyqtSignal(str)
    acc_y = pyqtSignal(str)
    acc_z = pyqtSignal(str)
    gyro_x = pyqtSignal(str)
    gyro_y = pyqtSignal(str)
    gyro_z = pyqtSignal(str)


    #signal = pyqtSignal("PyQt_PyObject")
    def __init__(self):
        QThread.__init__(self)
        self.radioButton = False
        #self.write_to = ""

    #pyqtSlot()
    def run(self):
        x = Car()
#        stm32f411 = STM32F411()
#        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#            s.bind(("127.0.0.1", 65432))
#            s.listen(1)
#            conn,addr = s.accept()

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

            #if (stm32f411.is_sensor_open()):
#            msg = stm32f411.read_line_from_port()

#            conn.sendall(msg)
#            msg = msg.decode("utf-8").replace("\n", "").replace("\r", "").split(",")

#            self.mag_x.emit(str(msg[0]))
#            self.mag_y.emit(str(msg[1]))
#            self.mag_z.emit(str(msg[2]))
#            self.acc_x.emit(str(msg[3]))
#            self.acc_y.emit(str(msg[4]))
#            self.acc_z.emit(str(msg[5]))
#            self.gyro_x.emit(str(msg[6]))
#            self.gyro_y.emit(str(msg[7]))
#            self.gyro_z.emit(str(msg[8]))


            #time.sleep(0.1)

    def changedButton(self, value):
        #print(value)
        self.radioButton = value



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
