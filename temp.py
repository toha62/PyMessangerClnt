from PyQt6 import QtCore, QtWidgets


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        for i in range(1, 21):
            self.sleep(3)
            self.mysignal.emit(f'i = {i}')


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.label = QtWidgets.QLabel('Нажмите на кнопку для запуска потока')
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button = QtWidgets.QPushButton('Запустить процесс')
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)
        self.mythread = MyThread()
        self.button.clicked.connect(self.on_clicked)
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.ConnectionType.QueuedConnection)

    def on_clicked(self):
        self.button.setDisabled(True)
        self.mythread.start()

    def on_started(self):
        self.label.setText('Вызван метод on_started')

    def on_finished(self):
        self.label.setText('Вызван метод on_finished')
        self.button.setDisabled(False)

    def on_change(self, s):
        self.label.setText(s)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Использование класса QThread')
    window.resize(300, 70)
    window.show()
    sys.exit(app.exec())