from PySide6.QtWidgets import (QLabel, QWidget, QMainWindow, QScrollArea, QVBoxLayout, QHBoxLayout, QPushButton,
                               QGridLayout, QListWidget, QListWidgetItem, QDialog, QLineEdit, QRadioButton, QCheckBox,
                               QButtonGroup, QSpinBox)
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

        self.convert = QPushButton("Convert", self)
        #convert.clicked.connect(self.convertAll)
        self.box.addWidget(self.convert)

    @Slot()
    def convertAll(self):
        if len(self.grid.getLinks()) > 0:
            for i in self.grid.getLinks():

                file = openPDF(i)
                new_name = "D:\Проекты\PDFReader_project\{}.png".format(i.split('/')[-1].split('.')[0])

                savePDFtoPNG(new_name, file)

    def connectConverter(self, slot):
        self.convert.clicked.connect(slot)


class ConvertOptionsDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        poses = {"labd": (0, 0), "dest": (1, 0), "browse": (1, 3), "png": (2, 0), "jpg": (2, 1),
                 "fold": (3, 0), "arc": (3, 1), "lab": (4, 0), "dpi": (4, 1),
                 "canc": (5, 2), "ok": (5, 3)}

        self.labd = QLabel("Destination:")

        self.destination = QLineEdit("")
        self.browse = QPushButton("browse")

        self.extension = QButtonGroup()
        self.png = QRadioButton("PNG")
        self.jpg = QRadioButton("JPG")
        self.extension.addButton(self.png)
        self.extension.addButton(self.jpg)

        self.additions = QButtonGroup()
        self.folder = QCheckBox("Create folder for each")
        self.archive = QCheckBox("Create archive for each")
        self.additions.addButton(self.folder)
        self.additions.addButton(self.archive)

        self.lab = QLabel("DPI:")
        self.dpi = QSpinBox()
        self.dpi.setMinimum(1)
        self.dpi.setMaximum(700)

        self.cancel = QPushButton("Cancel")
        self.ok = QPushButton("Convert")

        self.grid.addWidget(self.labd, poses["labd"][0], poses["labd"][1])
        self.grid.addWidget(self.destination, poses["dest"][0], poses["dest"][1], 1, 3)
        self.grid.addWidget(self.browse, poses["browse"][0], poses["browse"][1])
        self.grid.addWidget(self.png, poses["png"][0], poses["png"][1])
        self.grid.addWidget(self.jpg, poses["jpg"][0], poses["jpg"][1])
        self.grid.addWidget(self.folder, poses["fold"][0], poses["fold"][1])
        self.grid.addWidget(self.archive, poses["arc"][0], poses["arc"][1])
        self.grid.addWidget(self.lab, poses["lab"][0], poses["lab"][1], alignment=Qt.AlignRight)
        self.grid.addWidget(self.dpi, poses["dpi"][0], poses["dpi"][1])
        self.grid.addWidget(self.cancel, poses["canc"][0], poses["canc"][1])
        self.grid.addWidget(self.ok, poses["ok"][0], poses["ok"][1])

