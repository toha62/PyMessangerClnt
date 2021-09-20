import json
import requests
from PyQt6 import QtCore, QtWidgets
import datetime
from requests import HTTPError


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    MessageID = 0

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        msg = window.GetMessage(self.MessageID)
        while msg is not None:
            msg = json.loads(msg)
            user_name = msg['UserName']
            msg_text = msg['MessageText']
            time_stamp = msg['TimeStamp']
            msgtext = f"{time_stamp} : {user_name} : {msg_text}"
            print(msgtext)
            window.list1.insertItem(self.MessageID, msgtext)
            self.MessageID += 1
            msg = window.GetMessage(self.MessageID)
            # self.mysignal.emit(f'i = {i}')
        window.button2.setDisabled(False)


class MyWindow(QtWidgets.QWidget):
    ServerAdress = 'http://localhost:5000'

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.label1 = QtWidgets.QLabel('Входящие сообщения')
        self.label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.list1 = QtWidgets.QListWidget()
        self.label2 = QtWidgets.QLabel('Имя пользователя')
        self.label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit1 = QtWidgets.QLineEdit()
        self.label3 = QtWidgets.QLabel('Исходящие сообщение')
        self.label3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton('Отправить сообщение')
        self.button2 = QtWidgets.QPushButton('Получить сообщения')
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.list1)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(self.lineEdit1)
        self.vbox.addWidget(self.label3)
        self.vbox.addWidget(self.lineEdit2)
        self.vbox.addWidget(self.button)
        self.vbox.addWidget(self.button2)
        self.setLayout(self.vbox)
        self.mythread = MyThread()
        self.button.clicked.connect(self.on_clicked)
        self.button2.clicked.connect(self.on_clicked_get)
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.ConnectionType.QueuedConnection)

    def on_clicked(self):
        # self.button.setDisabled(True)
        # self.mythread.start()
        self.SendMessage()
        self.lineEdit1.clear()
        self.lineEdit2.clear()

    def on_clicked_get(self):
        self.button2.setDisabled(True)
        self.mythread.start()


    def on_started(self):
        self.label1.setText('Вызван метод on_started')

    def on_finished(self):
        self.label1.setText('Вызван метод on_finished')
        # self.button.setDisabled(False)

    def on_change(self, s):
        self.label1.setText(s)

    def SendMessage(self):
        user_name = self.lineEdit1.text()
        message_text = self.lineEdit2.text()
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


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Messenger')
    window.resize(400, 500)
    window.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(window.mythread.start)
    timer.start(5000)
    sys.exit(app.exec())
