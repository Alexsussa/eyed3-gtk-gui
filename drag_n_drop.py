from sys import setdlopenflags
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import gettext
import os

APPNAME = 'eyed3'
LOCATION = os.path.abspath('locale')

gettext.bindtextdomain(APPNAME, LOCATION)
gettext.textdomain(APPNAME)
_ = gettext.gettext


class Audio(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadAudio_txt = self

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
        import common
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))

        for item in links:

            if str(item).endswith('.mp3'):
                self.loadAudio_txt.setText(item)
                #common.Utils.displayAudioTags(self)
        else:
            event.ignore()


class Lyrics(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadLyrics_txt = self

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
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))

        for item in links:

            if str(item).endswith('.txt'):
                self.loadLyrics_txt.setText(item)
        else:
            event.ignore()


class Cover(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadCover_txt = self

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
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))

        for item in links:

            if str(item).endswith(('.png', '.jpg', '.jpeg')):
                self.loadCover_txt.setText(item)
        else:
            event.ignore()
