import socket, struct
from PySide2.QtCore import QThread, Signal, Slot

class McastServer(QThread):
    mcastRecv = Signal(bytes)
    def __init__(self, MCAST_GRP, MCAST_PORT, parent = None):
          super(McastServer, self).__init__(parent)
          self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
          self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          self.sock.bind(('', MCAST_PORT))
          mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
          self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    def run(self):
        while True:
            recv = self.sock.recv(2048)
            self.mcastRecv.emit(recv)