from PySide6.QtWidgets import (QLabel, QWidget, QMainWindow, QScrollArea, QVBoxLayout, QHBoxLayout, QPushButton,
                               QGridLayout, QListWidget, QListWidgetItem)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, Slot
from pdf_master import *


class FileListWidget(QListWidget):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.links = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for i in list(filter(lambda x: x.isLocalFile(), event.mimeData().urls())):
                if not i.toString() in self.links:
                    self.links.append(i.path()[1:])
                    self.addItem(i.path()[1:])

    def getLinks(self):
        return self.links[:]


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


class FastConverterWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.box = QVBoxLayout()
        self.setLayout(self.box)

        self.grid = FileListWidget()
        self.box.addWidget(self.grid)

        convert = QPushButton("Convert", self)
        convert.clicked.connect(self.convertAll)
        self.box.addWidget(convert)

    @Slot()
    def convertAll(self):
        if len(self.grid.getLinks()) > 0:
            for i in self.grid.getLinks():

                file = openPDF(i)
                new_name = "D:\Проекты\PDFReader_project\{}.png".format(i.split('/')[-1].split('.')[0])

                savePDFtoPNG(new_name, file)
