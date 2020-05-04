import json
import socket

from time import sleep

REST = 3

class CameraNotConnected(Exception):
    
    def __init__(self, Error):
        
        self.Error = Error

class XiaomiYiController:
    
    def __init__(self, IP = "192.168.42.1", Port = 7878, Timeout = 5):
        
        self._IP = IP
        
        self._Port = Port
        
        self._Timeout = Timeout

        self.__Token = None
        
        self.__Control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __repr__(self):
        
        return "Xiaomi YI('{}', {}, {})".format(self._IP, self._Port, self._Timeout)

    def SendMassageToServer(self, JsonMassage, Connection = False):
    
        if self.__Token or Connection:
        
            self.__Control.send(bytes(json.dumps(JsonMassage), 'UTF-8'))
        
            if not Connection: sleep(REST)
    
        else:
        
            raise CameraNotConnected("Make connection with object.connect() first.")
    
    def ConnectToServer(self):
        
        self.__Control.settimeout(self._Timeout)
        
        self.__Control.connect((self._IP, self._Port))
    
        self.SendMassageToServer({"msg_id": 257, "token": 0}, True)
        
        JsonMassage = self.__Control.recv(512).decode("utf-8")
        
        if not "rval" in JsonMassage:
            
            JsonMassage = self.__Control.recv(512).decode("utf-8")
            
        self.__Token = json.loads(JsonMassage)["param"]
        
        print('Token: ', self.__Token)
        

    def PartOneStartVideoToGetCapture(self):
        
        self.SendMassageToServer({"msg_id": 513, "token": self.__Token})
        
    def StopVideo(self):
        
        self.SendMassageToServer({"msg_id": 514, "token": self.__Token})

    def CloseConnection(self):
        
        self.__Control.close()
