import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap, QFontDatabase
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QLabel, QApplication, QPushButton, QToolBar, QAction

os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = "1"

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.flashcbt.0.0.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

app = None


class BrowserWindow(QMainWindow):

    def __init__(self, *args):
        super(BrowserWindow, self).__init__()
        self.window().setWindowIcon(QIcon(os.path.join(basedir, 'jamb-logo.ico')))
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(*args))

        self.setCentralWidget(self.browser)
        self.showMaximized()

        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        self.zoom_in_btn = QAction("Zoom In", self)
        self.zoom_in_btn.triggered.connect(self.zoom_in)
        self.zoom_in_btn.setIcon(QIcon(os.path.join(basedir, 'zoom-in.png')))
        nav_bar.addAction(self.zoom_in_btn)

        self.zoom_out_btn = QAction("Zoom Out", self)
        self.zoom_out_btn.triggered.connect(self.zoom_out)
        self.zoom_out_btn.setIcon(QIcon(os.path.join(basedir, 'zoom-out.png')))
        nav_bar.addAction(self.zoom_out_btn)

    def zoom_in(self):
        if self.browser.zoomFactor() < 3.0:
            self.browser.setZoomFactor(
                self.browser.zoomFactor() + 0.1
            )
            self.zoom_out_btn.setEnabled(True)
        else:
            self.zoom_in_btn.setEnabled(False)

    def zoom_out(self):

        if self.browser.zoomFactor() > 0.1:
            self.browser.setZoomFactor(
                self.browser.zoomFactor() - 0.1
            )
            self.zoom_in_btn.setEnabled(True)
        else:
            self.zoom_out_btn.setEnabled(False)


class StartWindow(QMainWindow):

    def __init__(self):
        super(StartWindow, self).__init__()
        QFontDatabase.addApplicationFont(os.path.join(basedir, "Roboto-Bold.ttf"))

        label_font = QFont("Roboto", 12)
        font = QFont("Roboto Lt", 10)
        self.browser_window = None
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.window().setWindowIcon(QIcon(os.path.join(basedir, 'jamb-logo.ico')))

        self.lab = QLabel(self)
        pixmap = QPixmap(os.path.join(basedir, 'jamb-logo.png'))
        self.lab.setPixmap(pixmap)
        self.lab.setFixedWidth(250)
        self.lab.setFixedHeight(250)
        self.lab.move(250, 50)

        self.top = 100
        self.left = 400
        self.setStyleSheet("background-color: white")
        self.setGeometry(self.left, self.top, 700, 650)

        self.url_bar = QLineEdit("", self)
        self.url_bar.setFixedWidth(400)
        self.url_bar.setFixedHeight(50)
        self.url_bar.setPlaceholderText("Enter IP-Address")
        self.url_bar.setStyleSheet("border: 2px solid black; background-color: transparent; padding: 8px 6px")
        self.url_bar.setFont(font)
        self.url_bar.move(170, 400)

        self.label = QLabel("Enter IP address to Logon to FlashCBT", self)
        self.label.setFixedWidth(500)
        self.label.setFont(label_font)
        self.label.move(170, 350)

        self.button = QPushButton("Enter", self)
        self.button.move(170, 470)
        self.button.setFont(label_font)
        self.button.setStyleSheet("border: 1.5px solid darkgreen; background-color: darkgreen; color: white;  font-size: 15px; border-radius: 15px")

        self.button.clicked.connect(self.navigate_to_url)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

    def navigate_to_url(self):
        url = "http://"
        url_bar_text = self.url_bar.text()
        main_url = url.__add__(url_bar_text)
        self.browser_window = BrowserWindow(main_url)

        self.browser_window.show()
        self.window().close()


# starting app

if app is not None:
    app.exit(1)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(basedir, 'jamb-logo.ico')))
QApplication.setApplicationName('FlashCBT Browser')
window = StartWindow()
window.show()
app.exec_()
