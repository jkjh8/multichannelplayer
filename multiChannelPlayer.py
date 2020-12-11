import sys, vlc, time, os, queue, json
from pymongo import MongoClient
from PySide2.QtCore import QCoreApplication, Qt, QTimer, Slot, Signal, QThread
from PySide2.QtWidgets import *

from Ui import Ui_MainWindow
from player import player
from mcastServer import McastServer

db_client =  MongoClient("mongodb://localhost:27017/TtsServer")["TtsServer"]
db_zones = db_client['Zones']
db_devices = db_client['DeviceId']

MCAST_GRP = "230.128.128.128"
MCAST_PORT = 12345

# HOST_IP = socket.gethostbyname(socket.gethostname())
MEDIA_PATH = os.path.join(os.path.expanduser("~"),'media')


class Main(QMainWindow, Ui_MainWindow):
    player1GetDevices = Signal();player2GetDevices = Signal();player3GetDevices = Signal();player4GetDevices = Signal();player5GetDevices = Signal();player6GetDevices = Signal();player7GetDevices = Signal();player8GetDevices = Signal();
    player1SetDevices = Signal(int);player2SetDevices = Signal(int);player3SetDevices = Signal(int);player4SetDevices = Signal(int);player5SetDevices = Signal(int);player6SetDevices = Signal(int);player7SetDevices = Signal(int);player8SetDevices = Signal(int);
    player1Play = Signal(str);player2Play = Signal(str);player3Play = Signal(str);player4Play = Signal(str);player5Play = Signal(str);player6Play = Signal(str);player7Play = Signal(str);player8Play = Signal(str)
    player1Stop = Signal();player2Stop = Signal();player3Stop = Signal();player4Stop = Signal();player5Stop = Signal();player6Stop = Signal();player7Stop = Signal();player8Stop = Signal(); playLoader = Signal(str)

    def __init__(self):
        super().__init__()
        self.playersGetDevices = [ self.player1GetDevices, self.player2GetDevices, self.player3GetDevices, self.player4GetDevices, self.player5GetDevices, self.player6GetDevices, self.player7GetDevices, self.player8GetDevices ]
        self.playersSetDevices = [ self.player1SetDevices, self.player2SetDevices, self.player3SetDevices, self.player4SetDevices, self.player5SetDevices, self.player6SetDevices, self.player7SetDevices, self.player8SetDevices ]
        self.playersPlay = [ self.player1Play, self.player2Play, self.player3Play, self.player4Play, self.player5Play, self.player6Play, self.player7Play, self.player8Play ]
        self.playersStop = [ self.player1Stop, self.player2Stop, self.player3Stop, self.player4Stop, self.player5Stop, self.player6Stop, self.player7Stop, self.player8Stop ]
        
        self.setupUi(self)
        self.show()

        self.zone = list(db_zones.find())
        print(self.zone)
        
        self.players = []
        self.playersStatus = []
        self.waitList = []

        for i in range(8):
            self.players.append(player(i))
            self.playersStatus.append(False)

            self.playersGetDevices[i].connect(self.players[i].getAudioDevices)
            self.playersSetDevices[i].connect(self.players[i].setAudioDevices)
            self.playersPlay[i].connect(self.players[i].play)
            self.playersStop[i].connect(self.players[i].stop)

            self.players[i].devicesList.connect(self.getDevices)
            self.players[i].playersStatus.connect(self.playerStatusChange)
            self.players[i].currentDevice.connect(self.setDevices)

            self.cbb_Player_Device_Sel_[i].currentIndexChanged.connect(self.playersSetDevices[i])

            self.playersGetDevices[i].emit()

        # self.currentDevices = list(db_devices.find())
        # for i in range(8):
        #     # self.playersSetDevices[i].emit(self.currentDevices[i]["value"])
        #     self.cbb_Player_Device_Sel_[i].setCurrentIndex(self.currentDevices[i]["value"])

        self.McastServer = McastServer(MCAST_GRP, MCAST_PORT)
        self.McastServer.mcastRecv.connect(self.parcer)
        self.McastServer.start()

        self.playerLoader = playerLoader()
        self.playLoader.connect(self.playerLoader.addQueue)
        self.playerLoader.play.connect(self.play)
        self.playerLoader.start()

        # self.playersSetDevices[0].emit(3)    
    @Slot(int, int)
    def setDevices(self, id, value):
        db_devices.update_one(
            { "_id": id },
            { "$set": {
                "value": value
                }
            }, upsert=True
        )

    @Slot(int, list)
    def getDevices(self, id, listItems):
        deviceList = []
        for i in range(len(listItems)):
            self.cbb_Player_Device_Sel_[id].addItem(listItems[i])
            deviceList.append(listItems[i])
        db_devices.update_one(
            { "_id": id },
            { "$set": {
                "list": deviceList
                }
            }, upsert=True
        )
        
    @Slot(int, bool, bool)
    def playerStatusChange(self, id, state, endReached):
        self.playersStatus[id] = state
        self.PlayerStatus[id].setChecked(state)
        print('wait = ', self.waitList)
        if endReached:
            self.playersStop[id].emit()
        if self.waitList:
            self.playLoader.emit(self.waitList[0])
            del self.waitList[0]

    @Slot(str)
    def play(self, playFile):
        for i in range(8):
            if self.playersStatus[i] == False:
                self.playersPlay[i].emit(playFile)
                self.callPalyer = True
                break
        else:
            self.waitList.append(playFile)

    @Slot(bytes)
    def parcer(self, recv):
        recvDict = json.loads(recv)
        if recvDict['func'] == 'play':
            self.playLoader.emit(recvDict['file'])


class playerLoader(QThread):
    play = Signal(str)
    def __init__(self, parent = None):
        super(playerLoader, self).__init__(parent)
        self.playlist = queue.Queue()

    def run(self):
        while True:
            if self.playlist.qsize():
                file = self.playlist.get()
                self.play.emit(file)
                time.sleep(1)

    @Slot(str, list)
    def addQueue(self, playFile):
        print('put ', playFile)
        self.playlist.put(playFile)

if __name__=="__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())