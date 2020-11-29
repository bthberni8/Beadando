from PyQt5 import QtWidgets, QtGui
import sys

from PyQt5.QtWidgets import QAction, QFileDialog, QInputDialog, QDialog, QAbstractItemView, QMessageBox

from mainwindow_minta import Ui_MainWindow
from addwindow import AddWindow
from information import Information


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_delete.clicked.connect(self.deleteCar) #ez érzékeli a kattintásokat
        self.pushButton_add.clicked.connect(self.addCar)
        self.pushButton_inf.clicked.connect(self.inf)
        self.pushButton_search.clicked.connect(self.searchCar)

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        menuBar = self.menuBar() #ez a felső menü, ahol be lehet tölteni a fájlt is
        filelMenu = menuBar.addMenu('&Fájl')
        fileOpen = QAction('&Megnyitás', self)
        fileOpen.triggered.connect(self.openFile)

        filelMenu.addAction(fileOpen)

        self.cars = [] #autók listája
        self.cardata = [] #autó adatainak listája
        self.brand_list = [] #ezeket a listáka töltjük be a comboboxokba
        self.price_list = []
        self.year_list = []
        self.power_list = []
        self.fuel_list = []

    def openFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog) #meghívás
        if name:
            self.cars = []
            with open(name) as f: #megnyitás
                lines = f.readlines() #kiolvasás
            lines = [line.rstrip('\n') for line in lines] #leveszi az újsor karakert
            for line in lines:
                words = line.split(" ") #szeletelés
                d = (words[0], words[1], words[2], int(words[3]), words[4], words[5])
                self.cars.append(d)

            self.sort_cars()
            self.fillTable()

            with open('CARadats.txt') as f: #megnyitás
                lines = f.readlines() #kiolvasás
            lines = [line.rstrip('\n') for line in lines]  # leveszi az újsor karakert
            for line in lines:
                words = line.split(" ")  # szeletelés
                d = (words[0], words[1], words[2], int(words[3]), words[4], words[5], words[6])
                self.cardata.append(d)

            self.comboBox_brand.clear() #törli a combobox tartalmát
            self.comboBox_price.clear()
            self.comboBox_year.clear()
            self.comboBox_power.clear()
            self.comboBox_fuel.clear()

            for i in range(len(self.cars)): #feltölti a comboboxok listáját nem ismétlődő elemekkel
                if self.cars[i][1] not in self.brand_list:
                    self.brand_list.append(self.cars[i][1])

                if self.cars[i][3] not in self.price_list:
                    self.price_list.append(self.cars[i][3])

            for i in range(len(self.cardata)):
                if self.cardata[i][1] not in self.year_list:
                    self.year_list.append(self.cardata[i][1])

                if self.cardata[i][3] not in self.power_list:
                    self.power_list.append(self.cardata[i][3])

                if self.cardata[i][2] not in self.fuel_list:
                    self.fuel_list.append(self.cardata[i][2])

            self.comboBox_brand.addItems(self.brand_list) #hozzáadjuk a listákat a comboboxokhoz

            self.sort(self.price_list) #meghívja a rendező függvényt
            string_price_list = (str(j) for j in self.price_list) #át kell konvertálni stringre mert csak azzal lehet feltölteni a comboboxokat
            self.comboBox_price.addItems(string_price_list)

            self.sort(self.year_list)
            self.comboBox_year.addItems(self.year_list)

            self.sort(self.power_list)
            string_power_list = (str(j) for j in self.power_list)
            self.comboBox_power.addItems(string_power_list)

            self.sort(self.fuel_list)
            self.comboBox_fuel.addItems(self.fuel_list)

    def fillTable(self): #táblázat betöltése
        self.tableWidget.setRowCount(len(self.cars)) #beállítjuk hány sora legyen a táblázatnak
        for i in range(len(self.cars)):
            for j in range(6):
                cells = QtWidgets.QTableWidgetItem() #cellák létrehozása
                cells.setText(str(self.cars[i][j])) #szöveg beállítása
                self.tableWidget.setItem(i, j, cells) #cella a táblázatba

    def deleteCar(self): #törlésgomb függvénye
        indexes = self.tableWidget.selectionModel().selectedRows() #kijelölt sort veszi fel
        tmp = []
        for index in sorted(indexes): #rendezett sorba megy
            for i in range(len(self.cars)):
                if index.data() != self.cars[i][0]: #ami nem egyezik meg a kijelöltel beltesszük a tmp-be
                    tmp.append(self.cars[i])

        self.cars = tmp
        self.fillTable() #táblázat újratöltése

    def addCar(self): #hozzáadás gomb függvénye
        addNewItem = AddWindow(self.cars) #a listát átadjuk a hozzáadás ablakhoz
        if addNewItem.exec_() == QDialog.Accepted: #ablak megnyitása és ellenőrzése h helyes-e az új érték
            self.cars.append(addNewItem.add_new_car) #hozzáadás(addwindow)
            self.cardata.append(addNewItem.add_new_car_data)
            self.sort_cars() #rendezzük
            self.fillTable() #újratöltjük

            for i in range(len(self.cars)): #új hozzáadott értéket hozzáadjuk a listához, ha még nem szerepel
                if self.cars[i][1] not in self.brand_list:
                    self.brand_list.append(self.cars[i][1])

                if self.cars[i][3] not in self.price_list:
                    self.price_list.append(self.cars[i][3])

            for i in range(len(self.cardata)):
                if self.cardata[i][1] not in self.year_list:
                    self.year_list.append(self.cardata[i][1])

                if self.cardata[i][3] not in self.power_list:
                    self.power_list.append(self.cardata[i][3])

                if self.cardata[i][2] not in self.fuel_list:
                    self.fuel_list.append(self.cardata[i][2])

            self.comboBox_brand.clear() #kitörlés
            self.comboBox_price.clear()
            self.comboBox_year.clear()
            self.comboBox_power.clear()
            self.comboBox_fuel.clear()

            self.comboBox_brand.addItems(self.brand_list) #hozzárendelés

            self.sort(self.price_list) #rendezés
            string_price_list = (str(j) for j in self.price_list)
            self.comboBox_price.addItems(string_price_list)

            self.sort(self.year_list)
            self.comboBox_year.addItems(self.year_list)

            self.sort(self.power_list)
            string_power_list = (str(j) for j in self.power_list)
            self.comboBox_power.addItems(string_power_list)

            self.sort(self.fuel_list)
            self.comboBox_fuel.addItems(self.fuel_list)

    def inf(self): #bővebbinf. gomb függvény
        indexes = self.tableWidget.selectionModel().selectedRows() #kijelölt sor
        tmp = []
        if indexes: #van-e kiválasztva valami
            for index in sorted(indexes):
                for i in range(len(self.cars)):
                    if index.data() == self.cars[i][0]: #kimásolja a tmp változóba a megfelelő sort
                        tmp.append(self.cars[i])
                        break
        if len(tmp) > 0: #van-e valami a tmp-be
            information = Information(tmp, self.cardata) #példányosítás , változó átadás és autók adatai
            information.exec_() #meghívja az információs ablakot
        else:
            QMessageBox.about(self, "Hiba", "A bővebb információhoz ki kell választani valamit a táblázatból!") #kivételkezelés

    def sort_cars(self): #sorbarendezi a név alapján a táblázatba bekerülő értékeket
        for i in range(len(self.cars) - 1):
            for j in range(i + 1, len(self.cars)):
                if self.cars[i][1] > self.cars[j][1]:
                    a = self.cars[i]     #innen van a sor csere
                    self.cars[i] = self.cars[j]
                    self.cars[j] = a

    def sort(self, array): #sorbarendezi a comboboxok listáit
        for i in range(len(array)-1):
            for j in range(i+1, len(array)):
                if array[i] > array[j]:
                    tmp = array[i]
                    array[i] = array[j]
                    array[j] = tmp

    def searchCar(self):
        brand = self.comboBox_brand.currentText() #a combobox aktuális értékét eltárolja egy változóban
        price = self.comboBox_price.currentText()
        year = self.comboBox_year.currentText()
        power = self.comboBox_power.currentText()
        fuel = self.comboBox_fuel.currentText()

        for i in range(len(self.cars)): #az összes sor összes cellájának hátterét fehérre színezi
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.item(i, j).setBackground(QtGui.QColor('white'))

        for i in range(len(self.cars)):
            for k in range(len(self.cardata)):
                if self.cars[i][0] == self.cardata[k][0]:  #egyforma azonosítójú sorok
                    if brand == self.cars[i][1] and int(price) >= self.cars[i][3] and year <= self.cardata[k][1]:
                        if int(power) <= self.cardata[k][3] and fuel == self.cardata[k][2]:

                            for j in range(self.tableWidget.columnCount()): #zöldre színezi a sort/sorokat
                                self.tableWidget.item(i, j).setBackground(QtGui.QColor('green'))


app = QtWidgets.QApplication(sys.argv)
form = MainWindow()
form.show()
sys.exit(app.exec_())
