import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QCheckBox


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def geocode(toponym):
    toponym_to_find = toponym

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json",
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
        return json_response
    else:
        print(response.reason)
        return


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(400, 200, 600, 750)

        self.setWindowTitle('Большая задача по Maps API. Часть №4,5,6,7,8,9,10')

        self.modes = ["map", "sat", "sat,skl"]
        self.cur_mode = 0
        self.params = {
            "z": '0',
            "ll": '',
            "size": "450,450",
            "format": "json",
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "l": f"{self.modes[self.cur_mode]}"
        }
        self.url = "https://static-maps.yandex.ru/1.x/"

        self.last_r = ''

        self.img_cont = QLabel(self)
        self.img_cont.resize(450, 450)
        self.img_cont.move(75, 20)

        self.search_input = QLineEdit(self)
        self.search_input.resize(450, 25)
        self.search_input.move(75, 500)
        self.search_input.setText('')

        self.search_output = QLineEdit(self)
        self.search_output.resize(450, 50)
        self.search_output.move(75, 550)
        self.search_output.setText('')
        self.search_output.setReadOnly(True)

        self.write_postal_code = QCheckBox(self)
        self.write_postal_code.move(75, 650)
        self.write_postal_code.setText('Писать почтовый индекс?')
        self.write_postal_code.resize(200,100)
        self.write_postal_code.stateChanged.connect(self.update_output)


        self.reset_dot_btn = QPushButton(self)
        self.reset_dot_btn.resize(150,50)
        self.reset_dot_btn.move(395,625)
        self.reset_dot_btn.setText('Сбросить точку')
        self.reset_dot_btn.clicked.connect(self.reset_dot)
        self.reset_dot_btn.clicked.connect(self.search_output.clear)

        self.search_btn = QPushButton(self)
        self.search_btn.resize(100, 50)
        self.search_btn.move(75, 625)
        self.search_btn.setText('Искать')
        self.search_btn.clicked.connect(self.search)

        self.change_mode_btn = QPushButton(self)
        self.change_mode_btn.resize(120, 50)
        self.change_mode_btn.move(225, 625)
        self.change_mode_btn.setText('Поменять режим')
        self.change_mode_btn.clicked.connect(self.change_mode)


    def update_output(self):
        if self.write_postal_code.isChecked():
            self.search_output.setText(f'{self.search_output.text()}, {self.last_r["postal_code"]}')
        else:
            self.search_output.setText(f'{",".join(self.search_output.text().split(", ")[:-1])}')

    def scale_map(self, response):
        toponym = response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        self.dot = f"{toponym_longitude},{toponym_lattitude}"

        self.params["pt"] = self.dot
        self.params["z"] = "16"
        self.params["ll"] = ",".join([toponym_longitude, toponym_lattitude])

        return self.params

    def change_mode(self):
        self.params["l"] = str(self.modes[(self.cur_mode + 1) % 3])
        self.cur_mode += 1
        self.redraw()

    def reset_dot(self):
        del self.params["pt"]
        self.redraw()


    def check_response(self, r):
        if r:
            self.get_img(r)
            r = geocode(self.params["ll"])
            r = r["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]
            self.last_r = r
            out = ''
            for i in r["Components"]:
                out += f'{i["name"]} '
            if self.write_postal_code.isChecked():
                out += r["postal_code"]
            self.search_output.setText(out.strip().replace(' ', ', '))
            return True
        else:
            print(f"Возникла ошибка : {r.reason}")
            return False


    def search(self):
        r = requests.get(url=self.url, params=self.scale_map(geocode(self.search_input.text())))
        self.check_response(r)


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
            if int(self.params["z"]) < 17:
                self.params["z"] = str(int(self.params["z"]) + 1)
        elif event.key() == Qt.Key_PageDown:
            if int(self.params["z"]) > 1:
                self.params["z"] = str(int(self.params["z"]) - 1)
        self.redraw()

    def first_launch(self):
        coords = ','.join(
            list(map(str, input("Введите координаты (разделитель ,) ").split(','))))
        zoom = input("Введите масштаб ")
        self.params["ll"], self.params["z"] = coords, zoom

        r = requests.get(url=self.url, params=self.params)
        if not self.check_response(r):
            self.first_launch()

    def redraw(self):
        r = requests.get(url=self.url, params=self.params)
        self.check_response(r)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.first_launch()
    sys.excepthook = except_hook
    sys.exit(app.exec())
