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

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Ok")
        fileMenu.addAction(open_file)

        pdf_file = fitz.open("Agro.pdf")
        for page in pdf_file:
            pixmap = page.getPixmap(matrix=Matrix(150/72, 150/72))
            need = pixmap.tobytes()

            qpixmap = QPixmap()
            qpixmap.loadFromData(need)

            label = QLabel("O")
            label.setText("fff")
            label.setPixmap(qpixmap)

            self.box.addWidget(label)

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
        print(fname)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

