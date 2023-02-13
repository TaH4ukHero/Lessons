import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(400, 200, 600, 450)
        self.setWindowTitle('Большая задача по Maps API. Часть №2')
        self.img_cont = QLabel()
        self.img_cont.resize(600, 450)
        self.img_cont.move(0, 0)

    def get_img(self, r):
        self.temp_file = "temp_file.png"
        with open(self.temp_file, 'wb') as f:
            f.write(r.content)
        self.img_cont.setPixmap(QPixmap(self.temp_file))
        self.show()

    def closeEvent(self, event):
        os.remove(self.temp_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.zoom < 17:
                self.zoom += 1
        elif event.key() == Qt.Key_PageDown:
            if self.zoom > 1:
                self.zoom -= 1
        self.get_map(self.zoom)

    def get_map(self, zoom=0):
        url = "https://static-maps.yandex.ru/1.x/"
        if zoom == 0:
            coords = ','.join(
                list(map(str, input("Введите координаты (разделитель ,) ").split(','))))
            zoom = int(input("Введите масштаб "))
            self.coords = coords
        self.zoom = zoom
        print(zoom)
        params = {
            "z": f"{zoom}",
            "ll": f"{self.coords}",
            "l": "map",
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json"
        }
        r = requests.get(url=url, params=params)
        if r:
            self.get_img(r)
        else:
            print('Возникла Ошибка')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.get_map()
    sys.excepthook = except_hook
    sys.exit(app.exec())
