import sys, vlc, time, os.path
from PySide2.QtCore import QThread, Slot, Signal

class player(QThread):
    devicesList = Signal(int, list)
    currentDevice = Signal(int, int)
    playersStatus = Signal(int, bool, bool)

    def __init__(self, playerId, parent = None):
        super(player, self).__init__(parent)
        self.playerId = playerId
        print('player', playerId)
        self.mediafile = None
        self.setNewPlayer()

    def setNewPlayer(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.eventManager = self.player.event_manager()
        self.setEventManager()

    def setMedia(self, mediaFile):
        self.media = self.instance.media_new(mediaFile)
        self.player.set_media(self.media)

    def setEventManager(self):
        self.eventManager.event_attach(vlc.EventType.MediaPlayerEndReached, self.endReached) #meida end
        self.eventManager.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.getMediaLength, self.player) #media length
        self.eventManager.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.getCurrentTime, self.player) #emdia get currnet time
    
    def getCurrentTime(self, time, player):
        # print(time.u.new_time)
        pass

    def getMediaLength(self, time, player):
        # print(time.u.new_time)
        pass
    
    @Slot()
    def getAudioDevices(self):
        self.devices = []
        self.devicesName = []
        self.mods = self.player.audio_output_device_enum()
        if self.mods:
            while self.mods:
                self.devices.append(self.mods.contents.device)
                self.devicesName.append((self.mods.contents.description).decode())
                self.mods = self.mods.contents.next
        self.devicesList.emit(self.playerId, self.devicesName)

    @Slot(int)
    def setAudioDevices(self, deviceId):
        self.player.audio_output_device_set(None, self.devices[deviceId])
        current = self.player.audio_output_device_get()
        if current:
            currentdeviceid = self.devices.index(current.encode('utf-8'))
        else:
            currentdeviceid = 0
        self.currentDevice.emit(self.playerId, currentdeviceid)

    def endReached(self, event):
        print('endReached')
        self.playersStatus.emit(self.playerId, False, True)
        self.setNewPlayer()

    @Slot(str)
    def play(self, mediaFile):
        if self.mediafile == mediaFile: self.player.stop()
        else: self.mediafile = mediaFile; self.setMedia(mediaFile)
        self.player.play()
        self.playersStatus.emit(self.playerId, True, False)
    
    @Slot()
    def pause(self):
        self.player.pause()

    @Slot()
    def stop(self):
        self.player.stop()
        self.playersStatus.emit(self.playerId, False, False)
        self.mediafile = None

    @Slot(int)
    def setVol(self, vol):
        self.player.audio_set_volume(vol)
    
    @Slot()
    def getVol(self):
        print(self.player.audio_get_volume())