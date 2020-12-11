# -*- coding: utf-8 -*-

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QRect, QSize, Qt)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ind_Style = ("QPushButton{background-color: rgb(255, 255, 255); border-radius: 5px;} QPushButton:checked{color:white;background-color:red}")

        self.PlayerTab = ["i"]*8
        self.PlayerStatus = ["i"]*8;self.lbl_Player_Name_ = ["i"]*8;
        self.cbb_Player_Device_Sel_ = ["i"]*8

        MainWindow.resize(500, 400)

        self.centralwidget = QWidget(MainWindow)
        self.vbox_player = QVBoxLayout(self.centralwidget)
        self.hbox_Name_Tag = QHBoxLayout()
        self.hbox_Name_Tag.setContentsMargins(6, 6, 6, 6)
        self.vbox_player.addLayout(self.hbox_Name_Tag)

        self.main_sc = QScrollArea(self.centralwidget)
        self.main_sc.setWidgetResizable(True)
        self.sc = QWidget()
        self.sc.setGeometry(QRect(0, 0, 600, 300))

        self.vbox_Main = QVBoxLayout(self.sc)       

        for i in range(8):
            self.PlayerStatus[i] = QPushButton("P{}".format(i+1), self.centralwidget)
            self.PlayerStatus[i].setMinimumSize(QSize(0,30))
            self.PlayerStatus[i].setMaximumSize(QSize(30, 16777215))
            self.PlayerStatus[i].setCheckable(True)
            self.PlayerStatus[i].setStyleSheet(ind_Style)
            self.hbox_Name_Tag.addWidget(self.PlayerStatus[i])

            self.lbl_Player_Name_[i] = QLabel("Player {}".format(i+1),self.sc)
            self.lbl_Player_Name_[i].setMaximumWidth(50)
            self.cbb_Player_Device_Sel_[i] = QComboBox(self.sc)


            self.PlayerTab[i] = QHBoxLayout()

            self.PlayerTab[i].addWidget(self.lbl_Player_Name_[i])
            self.PlayerTab[i].addWidget(self.cbb_Player_Device_Sel_[i])           
                    
            self.vbox_Main.addLayout(self.PlayerTab[i])

        self.main_sc.setWidget(self.sc)

        self.vbox_player.addWidget(self.main_sc)

        MainWindow.setCentralWidget(self.centralwidget)
