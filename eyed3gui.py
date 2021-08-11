#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from common import Utils as u
from drag_n_drop import Audio, Lyrics, Cover
import gettext
import webbrowser
import os
import sys

APPNAME = 'eyed3'
LOCATION = os.path.abspath('locale')

gettext.bindtextdomain(APPNAME, LOCATION)
gettext.textdomain(APPNAME)
_ = gettext.gettext


class Eyed3():
    def __init__(self):
        super().__init__()

    def setup_ui(self, MainWindow):
        # Setting images application
        self.winIcon = QIcon('icons/eyed3.png')

        # Setting central widget and main window
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowIcon(self.winIcon)

        # Setting menubar
        self.menuBar = QMenuBar(self.centralwidget)

        self.menuFile = QMenu(_('File'), self.centralwidget)
        self.menuFile.addAction(_('Load audio file...'), lambda: u.loadAudioFile(self, QFileDialog), 'Ctrl+O')
        self.menuFile.addAction(_('Save all tags'), lambda: u.saveTags(self), 'Ctrl+S')
        self.menuFile.addSeparator()
        self.menuFile.addAction(_('Exit'), MainWindow.close, 'Ctrl+Q')

        self.menuHelp = QMenu(_('Help'), self.centralwidget)
        self.menuHelp.addAction(_('GitHub'), lambda: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui'), 'Ctrl+G')
        self.menuHelp.addAction(_('License'), lambda: webbrowser.open('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/LICENSE'), 'Ctrl+K')
        self.menuHelp.addAction(_('Documentation'), lambda: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui#eyed3-gtk-gui'), 'Ctrl+D')
        self.menuHelp.addAction(_('Search for new updates...'), lambda: u.checkForUpdates(self), 'Ctrl+R')
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(_('About'), lambda: u.aboutEyed3(self), 'Ctrl+H')

        self.menuBar.addMenu(self.menuFile)
        self.menuBar.addMenu(self.menuHelp)
        MainWindow.setMenuBar(self.menuBar)

        # Setting widgets
        self.title = QLabel(_('Title'), self.centralwidget)
        self.title.setGeometry(QRect(20, 0, 100, 50))
        self.title_txt = QLineEdit(self.centralwidget)
        self.title_txt.setGeometry(QRect(60, 10, 230, 30))
        self.title_txt.setPlaceholderText(_('Music title...'))
        self.title_txt.setAcceptDrops(False)

        self.artist = QLabel(_('Artist'), self.centralwidget)
        self.artist.setGeometry(QRect(305, 0, 100, 50))
        self.artist_txt = QLineEdit(self.centralwidget)
        self.artist_txt.setGeometry(QRect(350, 10, 230, 30))
        self.artist_txt.setPlaceholderText(_('Artist or band name...'))
        self.artist_txt.setAcceptDrops(False)

        self.trackNumber = QLabel(_('Track Number'), self.centralwidget)
        self.trackNumber.setGeometry(QRect(595, 0, 100, 50))
        self.trackNumber_txt = QLineEdit(self.centralwidget)
        self.trackNumber_txt.setGeometry(QRect(700, 10, 50, 30))
        self.trackNumber_txt.setPlaceholderText(_('Num...'))
        self.trackNumber_txt.setAcceptDrops(False)

        self.album = QLabel(_('Album'), self.centralwidget)
        self.album.setGeometry(QRect(20, 50, 100, 50))
        self.album_txt = QLineEdit(self.centralwidget)
        self.album_txt.setGeometry(QRect(65, 60, 225, 30))
        self.album_txt.setPlaceholderText(_('Album name...'))
        self.album_txt.setAcceptDrops(False)

        self.albumArtist = QLabel(_('Album Artist'), self.centralwidget)
        self.albumArtist.setGeometry(QRect(305, 50, 100, 50))
        self.albumArtist_txt = QLineEdit(self.centralwidget)
        self.albumArtist_txt.setGeometry(QRect(395, 60, 220, 30))
        self.albumArtist_txt.setPlaceholderText(_('Album artist or band...'))
        self.albumArtist_txt.setAcceptDrops(False)

        self.removeTags_btn = QPushButton(_('Remove All Tags'), self.centralwidget, clicked=lambda: u.removeAllTags(self))
        self.removeTags_btn.setGeometry(QRect(620, 60, 130, 30))

        self.genre = QLabel(_('Genre'), self.centralwidget)
        self.genre.setGeometry(QRect(20, 100, 100, 50))
        self.genre_txt = QComboBox(self.centralwidget, editable=True)
        self.genre_txt.setGeometry(QRect(65, 110, 225, 30))
        self.genre_txt.lineEdit().setPlaceholderText(_('Music genre...'))
        self.genre_txt.lineEdit().setAcceptDrops(False)

        self.year = QLabel(_('Year'), self.centralwidget)
        self.year.setGeometry(QRect(305, 100, 100, 50))
        self.year_txt = QLineEdit(self.centralwidget)
        self.year_txt.setGeometry(QRect(335, 110, 50, 30))
        self.year_txt.setPlaceholderText(_('Year...'))
        self.year_txt.setAcceptDrops(False)

        self.loadLyrics_txt = Lyrics(self.centralwidget)
        self.loadLyrics_txt.setGeometry(QRect(395, 110, 250, 30))
        self.loadLyrics_txt.setPlaceholderText(_('Load a text file with lyrics...'))
        self.loadLyrics_txt.setAcceptDrops(True)
        self.loadLyrics_btn = QPushButton(_('Lyrics'), self.centralwidget, clicked=lambda: u.loadLyricsFile(self, QFileDialog))
        self.loadLyrics_btn.setGeometry(QRect(650, 110, 100, 30))

        self.loadAudio_txt = Audio(self.centralwidget)
        self.loadAudio_txt.setGeometry(QRect(20, 160, 270, 30))
        self.loadAudio_txt.setPlaceholderText(_('Load an audio file...'))
        self.loadAudio_txt.setAcceptDrops(True)
        self.loadAudio_btn = QPushButton(_('Load Audio'), self.centralwidget, clicked=lambda: u.loadAudioFile(self, QFileDialog))
        self.loadAudio_btn.setGeometry(QRect(305, 160, 150, 30))

        self.cleanFields_btn = QPushButton(_('Clear Fields'), self.centralwidget,clicked=lambda: u.clearFields(self))
        self.cleanFields_btn.setGeometry(QRect(460, 160, 150, 30))

        self.saveTags = QPushButton(_('Save Tags'), self.centralwidget, clicked=lambda: u.saveTags(self))
        self.saveTags.setGeometry(QRect(615, 160, 135, 30))

        self.composer = QLabel(_('Composer(s)'), self.centralwidget)
        self.composer.setGeometry(QRect(20, 200, 100, 50))
        self.composer_txt = QLineEdit(self.centralwidget)
        self.composer_txt.setGeometry(QRect(115, 210, 250, 30))
        self.composer_txt.setPlaceholderText(_('Composer(s) name(s)...'))
        self.composer_txt.setAcceptDrops(False)

        self.loadCover_txt = Cover(self.centralwidget)
        self.loadCover_txt.setGeometry(QRect(370, 210, 240, 30))
        self.loadCover_txt.setPlaceholderText(_('Load an album cover...'))
        self.loadCover_txt.setAcceptDrops(True)
        self.loadCover_btn = QPushButton(_('Cover'), self.centralwidget, clicked=lambda: u.loadCoverFile(self, QFileDialog))
        self.loadCover_btn.setGeometry(QRect(615, 210, 135, 30))

        self.comments = QLabel(_('Comments'), self.centralwidget)
        self.comments.setGeometry(QRect(20, 250, 100, 50))
        self.comments_txt = QTextEdit(self.centralwidget)
        self.comments_txt.setGeometry(QRect(105, 260, 645, 80))
        self.comments_txt.setPlaceholderText(_('Comments...'))
        self.comments_txt.setAcceptDrops(False)

        self.bg_img = QLabel(self.centralwidget)
        self.bg_img.setGeometry(QRect(256, 355, 256, 256))
        self.bg_img.setStyleSheet('background-image: url(bg.png); background-repeat: no-repeat; width: 100%; height: 100%;')

        # Functions running in background
        u.genreList(self, self.genre_txt)

        self.timer = QTimer()
        self.timer.setInterval(300000)
        self.timer.timeout.connect(lambda: u.checkAutoUpdates(self))
        self.timer.start()

        # Keyboard shortcuts
        clean_fields = QShortcut(QKeySequence('Ctrl+L'), self.cleanFields_btn)
        clean_fields.activated.connect(lambda: u.clearFields(self))

        displayTagsOnDrop = QShortcut(QKeySequence('Ctrl+Return'), self.loadAudio_txt)
        displayTagsOnDrop.activated.connect(lambda: u.displayAudioTags(self))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    #Setting translator
    translator = QTranslator()
    locale = QLocale().system().name()
    library = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load('qt_' + locale, library)
    app.installTranslator(translator)

    MainWindow = QMainWindow()
    MainWindow.setWindowTitle('eyeD3')
    MainWindow.setFixedSize(770, 650)
    ui = Eyed3()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
