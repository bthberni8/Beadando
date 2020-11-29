from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from addwindow_minta import Ui_AddWindow


class AddWindow(QDialog, Ui_AddWindow): #a hozzáadás ablaknak a kódja

    def __init__(self, data, parent=None):
        super(AddWindow, self).__init__(parent)
        self.setupUi(self)

        self.data = data #ez az egész cars lista

        self.pushButton_add.clicked.connect(self.add)
        self.pushButton_cancel.clicked.connect(self.close) #gombkattintások

        self.add_new_car = []
        self.add_new_car_data = []

    def add(self): #hozzáadás gomb függvénye
        identification = self.lineEdit_ident.text() #szöveget amit a felhaszn beír beteszi a változóba
        brand = self.lineEdit_brand.text()
        car_type = self.lineEdit_type.text()
        price = self.lineEdit_price.text()
        number = self.lineEdit_number.text()
        location = self.lineEdit_location.text()
        year = self.lineEdit_year.text()
        fuel = self.lineEdit_fuel.text()
        power = self.lineEdit_power.text()
        ccm = self.lineEdit_ccm.text()
        transmission = self.lineEdit_transmission.text()
        km = self.lineEdit_km.text()

        r = True #ha bármelyik érték rossz hamisra kell állítani

        for i in range(len(self.data)):
            if identification == self.data[i][0]: #végig megy az egész listán és ha létezik ilyen azon akkor hibaüzenet
                QMessageBox.about(self, "Hiba", "Már létezik ilyen azonosítójú autó!")
                r = False
            elif number == self.data[i][4]: #alvázszám ellenőrzése
                QMessageBox.about(self, "Hiba", "Már létezik ilyen alvázszámú autó!")
                r = False

        pr = 0
        try:
            pr = int(price)
            if pr <= 0:
                QMessageBox.about(self, "Hiba", "Az ár 0-nál nagyobb kell legyen!")
                r = False
        except ValueError:
            QMessageBox.about(self, "Hiba", "Az árban nem szerepelhetnek betűk!")
            r = False

        try:
            y = int(year)
            if 1950 >= y or y >= 2020:
                QMessageBox.about(self, "Hiba", "Az év 1950 és 2020 között kell legyen!")
                r = False
        except ValueError:
            QMessageBox.about(self, "Hiba", "Az évben nem szerepelhetnek betűk!")
            r = False

        p = 0
        try:
            p = int(power)
            if p < 0:
                QMessageBox.about(self, "Hiba", "A lóerő nem lehet negatív!")
                r = False
        except ValueError:
            QMessageBox.about(self, "Hiba", "A lóerőben nem szerepelhetnek betűk!")
            r = False

        try:
            c = int(ccm)
            if c < 0:
                QMessageBox.about(self, "Hiba", "A hengerűrtartalom nem lehet negatív!")
                r = False
        except ValueError:
            QMessageBox.about(self, "Hiba", "A hengerűrtartalomban nem szerepelhetnek betűk!")
            r = False

        try:
            k = int(km)
            if k < 0:
                QMessageBox.about(self, "Hiba", "A kilométer nem lehet negatív!")
                r = False
        except ValueError:
            QMessageBox.about(self, "Hiba", "A kilométerben nem szerepelhetnek betűk!")
            r = False

        if r: #ha minden helyes akkor létrehozza a tuple-t és küld egy acceptet
            self.add_new_car = (identification, brand, car_type, pr, number, location) #táblázatos
            self.add_new_car_data = (identification, year, fuel, p, ccm, transmission, km) #bővebbenes
            self.accept()
