from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QFileDialog

from information_minta import Ui_Information


class Information(QDialog, Ui_Information):
    def __init__(self, row, cardata, parent=None):
        super(Information, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_close.clicked.connect(self.close)

        self.row = row #csak egy sort
        self.cardata = cardata

        image = QLabel(self)  #megjeleníti a képet
        image.setGeometry(50, 40, 400, 400)
        pixmap = QtGui.QPixmap("auto\\" + self.row[0][0] + ".jpg")
        pixmap_scaled = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        image.setPixmap(pixmap_scaled)
        image.show()

        for i in range(len(self.cardata)):
            if self.cardata[i][0] == self.row[0][0]:#ellenőrzi hogy az adott id megegyezik a listában szereplővel
                self.label_name.setText(row[0][1]) #betöltés a megfelelő címkékbe
                self.label_year.setText(self.cardata[i][1])
                self.label_fuel.setText(self.cardata[i][2])
                self.label_power.setText(str(self.cardata[i][3]))
                self.label_ccm.setText(self.cardata[i][4])
                self.label_transmission.setText(self.cardata[i][5])
                self.label_km.setText(self.cardata[i][6])
                break
