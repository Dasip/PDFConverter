from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow, QScrollArea, QVBoxLayout,
                             QAction, QFileDialog)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from fitz import *
from PIL import Image
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_file = None

    def initUI(self):

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.box = QVBoxLayout()

        self.widget.setLayout(self.box)
        self.statusBar()

        open_file = QAction(QIcon("trial.png"), "Open", self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip("Open new file")
        open_file.triggered.connect(self.show_open)

        save_file = QAction(QIcon("trial.png"), "Convert to", self)
        save_file.setShortcut('Ctrl+S')
        save_file.setStatusTip("Convert current PDF to some other extension")
        save_file.triggered.connect(self.show_convert)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(open_file)
        fileMenu.addAction(save_file)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle("PDFReader")
        self.show()
        return

    def show_open(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", '/home')[0]
        self.change_pdf(fname)

    def show_convert(self):
        options = QFileDialog.Options()
        filename, ext = QFileDialog.getSaveFileName(self, "Convert PDF to...", "FFF", "All files (*);;PNG (*.png)", options=options)
        if filename:
            self.save_as(filename, ext)

    def clear_layout(self):
        for i in reversed(range(self.box.count())):
            self.box.itemAt(i).widget().setParent(None)

    def change_pdf(self, filename):
        self.clear_layout()
        pdf_file = fitz.open(filename)
        self.current_file = pdf_file
        for page in pdf_file:
            pixmap = page.getPixmap(matrix=Matrix(150/72, 150/72))
            need = pixmap.tobytes()

            qpixmap = QPixmap()
            qpixmap.loadFromData(need)

            label = QLabel("O")
            label.setText("fff")
            label.setPixmap(qpixmap)

            self.box.addWidget(label)

    def save_as(self, fname, ext):
        if ext != "(*)":
            file_sample = fname.split('/')
            name_part = file_sample[-1].split('.')
            name_part[0] = name_part[0] + "{}"
            name_part = ".".join(name_part)
            file_sample[-1] = name_part
            file_sample = '/'.join(file_sample)
            counter = 1
            print(file_sample)

            for page in self.current_file:
                pix = page.getPixmap(matrix=Matrix(300/72, 300/72))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(file_sample.format(str(counter)))
                counter += 1


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

