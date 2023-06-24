from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from eyed3 import id3
import gettext
import os

APPNAME = 'eyed3'
LOCATION = os.path.abspath('/usr/share/locale')

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


    def displayAudioTags(self):
        tag = id3.Tag()
        tag.parse(self.loadAudio_txt.text())
        self.title_txt.setText(str(tag.title))
        self.artist_txt.setText(str(tag.artist))
        self.album_txt.setText(str(tag.album))
        self.albumArtist_txt.setText(str(tag.album_artist))
        self.genre_txt.setCurrentText(str(tag.genre))

        if str(tag.title) == 'None':
            self.title_txt.setText('')
        else:
            self.title_txt.setText(str(tag.title))

        if str(tag.artist) == 'None':
            self.artist_txt.setText('')
        else:
            self.artist_txt.setText(str(tag.artist))

        if str(tag.album) == 'None':
            self.album_txt.setText('')
        else:
            self.album_txt.setText(str(tag.album))

        if str(tag.album_artist) == 'None':
            self.albumArtist_txt.setText('')
        else:
            self.albumArtist_txt.setText(str(tag.album_artist))

        if str(tag.genre) == 'None':
            self.genre_txt.setCurrentText('')
        else:
            self.genre_txt.setCurrentText(str(tag.genre))

        if str(tag.release_date) == 'None':
            self.year_txt.setText('')
        else:
            self.year_txt.setText(str(tag.release_date))

        if str(tag.composer) == 'None':
            self.composer_txt.setText('')
        else:
            self.composer_txt.setText(str(tag.composer))

        if str(tag.track_num[0]) == 'None':
            self.trackNumber_txt.setText('')
        elif tag.track_num[0] == 0:
            self.trackNumber_txt.setText('')
        else:
            self.trackNumber_txt.setText(str(tag.track_num[0]))

        try:
            if str(tag.comments[0].text):
                self.comments_txt.setText(str(tag.comments[0].text))

        except IndexError:
            self.comments_txt.setText('')
