from PyQt5.QtWidgets import (QLabel, QWidget, QMainWindow, QScrollArea, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from pdf_master import *


class EditWindow(QScrollArea):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.widget = QWidget()
        self.box = QVBoxLayout()

        self.widget.setLayout(self.box)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

    def displayFile(self, filename):
        self.clearDisplay()
        file = openPDF(filename)
        for page in file:
            qpix = QPixmap()
            pix = page.getPixmap(matrix=Matrix(getDPI(300), getDPI(300))).tobytes()
            qpix.loadFromData(pix)
            lab = QLabel()
            lab.setPixmap(qpix)
            self.box.addWidget(lab)

    def clearDisplay(self):
        for i in reversed(range(self.box.count())):
            self.box.itemAt(i).widget().setParent(None)
