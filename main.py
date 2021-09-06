# import json
import json
import sys
import datetime
import requests
from PyQt6 import uic, QtCore, QtGui, QtWidgets
from requests import HTTPError


class MainWindow(QtWidgets.QMainWindow):
    ServerAdress = 'http://localhost:5000'
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('msnger_cl.ui', self)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        user_name = self.lineEdit_1.text()
        message_text = self.lineEdit_2.text()
        time_stamp = str(datetime.datetime.today())
        msg = {"UserName": user_name,
               "MessageText": message_text,
               "TimeStamp": time_stamp
               }
        print('Send message: ' + str(msg))
        url = self.ServerAdress + '/api/Messanger'
        r = requests.post(url, json=msg)
        print(r.status_code, r.reason)

    def GetMessage(self, id):
        url = self.ServerAdress + '/api/Messanger/' + str(id)
        try:
            r = requests.get(url)
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occured: {err}')
            return None
        else:
            return r.text

    def timer_Event(self):
        msg = self.GetMessage(self.MessageID)
        while msg is not None:
            msg = json.loads(msg)
            user_name = msg['UserName']
            msg_text = msg['MessageText']
            time_stamp = msg['TimeStamp']
            msgtext = f"{time_stamp} : {user_name} : {msg_text}"
            print(msgtext)
            self.listWidget_1.insertItem(self.MessageID, msgtext)
            self.MessageID += 1
            msg = self.GetMessage(self.MessageID)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timer_Event)
    timer.start(5000)
    sys.exit(app.exec())
