from PySide6.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow, QScrollArea, QVBoxLayout, QFileDialog)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import Qt
from fitz import *
from PIL import Image
from widgets import *
from pdf_master import *
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_file = None

    def initUI(self):

        self.scroll = EditWindow()
        self.fastc = FastConverterWindow()

        self.widget = QWidget()
        self.box = QHBoxLayout()
        self.widget.setLayout(self.box)

        button_converter = QPushButton("Fast Convert", self)
        button_converter.clicked.connect(self.openConverter)
        # TODO: create fast converter for converting multiple PDFs at once

        button_editor = QPushButton("Open File", self)
        button_editor.clicked.connect(self.openEditor)

        self.box.addWidget(button_converter)
        self.box.addWidget(button_editor)

        self.statusBar()

        open_file = QAction(QIcon("trial.png"), "Open", self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip("Open new file")
        open_file.triggered.connect(self.showOpen)

        save_file = QAction(QIcon("trial.png"), "Convert to", self)
        save_file.setShortcut('Ctrl+S')
        save_file.setStatusTip("Convert current PDF to some other extension")
        save_file.triggered.connect(self.showConvert)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(open_file)
        fileMenu.addAction(save_file)

        self.setCentralWidget(self.widget)

        self.setGeometry(300, 100, 700, 700)
        self.setWindowTitle("PDFReader")
        self.show()
        return

    @Slot()
    def openConverter(self):
        print("Converter opened")
        self.setCentralWidget(self.fastc)
        self.fastc.connectConverter(self.showFastConvert)

    @Slot()
    def openEditor(self):
        print("Editor opened")
        self.show_open()

    @Slot()
    def showFastConvert(self):
        c = ConvertOptionsDialog()
        c.connectPackage(self.fastConvert)
        c.exec()

    @Slot()
    def fastConvert(self, datapack):
        print(datapack)
        for file in self.fastc.getLinks():
            convertPDF(file, datapack)


    def showOpen(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", '/home')[0]
        self.current_file = fitz.open(fname)
        if self.scroll.parentWidget() != self:
            self.setCentralWidget(self.scroll)
        self.scroll.displayFile(fname)

    def showConvert(self):
        options = QFileDialog.Options()
        filename, ext = QFileDialog.getSaveFileName(self, "Convert PDF to...", "FFF", "All files (*);;PNG (*.png)", options=options)
        if filename:
            savePDFtoPNG(filename, self.current_file)




def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

