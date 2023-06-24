from PyQt5.QtWidgets import QDialog, QLabel, QMessageBox, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from urllib.request import urlopen
from eyed3 import id3
import eyed3
import os
import gettext
import webbrowser
from drag_n_drop import Audio

APPNAME = 'eyed3'
LOCATION = os.path.abspath('/usr/share/locale')

gettext.bindtextdomain(APPNAME, LOCATION)
gettext.textdomain(APPNAME)
_ = gettext.gettext


class Utils():
    def __init__(self):
        super(Utils, self).__init__()

        self.winIcon = QIcon('/usr/share/icons/hicolor/256x256/apps/eyed3.png')

        self.loadAudio_txt = Audio()

    def saveTags(self):
        title = self.title_txt.text()
        artist = self.artist_txt.text()
        tracknum = self.trackNumber_txt.text()
        album = self.album_txt.text()
        album_artist = self.albumArtist_txt.text()
        genre = self.genre_txt.currentText()
        year = self.year_txt.text()
        lyrics = self.loadLyrics_txt.text()
        cover = self.loadCover_txt.text()
        audio = self.loadAudio_txt.text()
        composer = self.composer_txt.text()
        comments = self.comments_txt.toPlainText()
    
        if audio == '':
            Utils.popup_warning(self, msg=_('You need to load an audio file to save tags.'))
        else:
            mp3 = id3.Tag()
            mp3.parse(audio, [2, 4, 0])
            mp3.title = title
            mp3.artist = artist
            mp3.album = album
            mp3.album_artist = album_artist
            mp3.genre = genre
            mp3.recording_date = year
            mp3.release_date = year
            mp3.original_release_date = year
            mp3.composer = composer
            if comments == '':
                mp3.comments.set('https://github.com/Alexsussa/eyed3-gtk-gui')
            else:
                mp3.comments.set(comments)
            if tracknum == '':
                mp3.track_num = 0
            else:
                mp3.track_num = tracknum
            if lyrics == '':
                pass
            else:
                mp3.lyrics.set(open(lyrics).read())
            if cover == '':
                pass
            else:
                imageData = open(cover, 'rb').read()
                mp3.images.set(3, imageData, 'image/jpg')
            mp3.save(audio, version=(2, 4, 0))

            Utils.clearFields(self)
            Utils.popup_info(self, msg=_('All audio tags are saved.\nReload the audio file to make sure the new tags were set.'))


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


    def removeAllTags(self):
        audio_file = self.loadAudio_txt.text()
        if audio_file == '':
            Utils.popup_warning(self, msg=_('You need to load an audio file to remove tags.'))
        else:
            id3.tag.Tag.remove(audio_file)
            mp3 = id3.Tag()
            mp3.parse(audio_file, [2, 4, 0])
            mp3.save(audio_file)
            Utils.clearFields_2(self)

        
    def loadAudioFile(self, dialog):
        audio_file = dialog.getOpenFileName(caption=_('Open an audio file'), directory=os.path.expanduser(_('~/Music')), filter=_('Audio file (*.mp3)'), options=dialog.DontUseNativeDialog)

        if str(audio_file[0]) == '':
            pass
        else:
            mp3 = eyed3.load(audio_file[0]).tag
            mp3.parse(audio_file[0], [2, 4, 0])
            mp3.save()
            self.loadAudio_txt.setText(audio_file[0])
            Utils.displayAudioTags(self)


    def loadLyricsFile(self, dialog):
        lyrics_file = dialog.getOpenFileName(caption=_('Open a text file containing music lyrics'), directory=os.path.expanduser(_('~/Documents')), filter=_('Text file (*.txt)'), options=dialog.DontUseNativeDialog)
        self.loadLyrics_txt.setText(str(lyrics_file[0]))


    def loadCoverFile(self, dialog):
        cover_file = dialog.getOpenFileName(caption=_('Open a image file'), directory=os.path.expanduser(_('~/Images')), filter=_('Images file (*.png *jpg *.jpeg)'), options=dialog.DontUseNativeDialog)
        self.loadCover_txt.setText(str(cover_file[0]))


    def genreList(self, combo):
        genres = []
        genre_file = open('/usr/share/doc/eyed3gui/genres.txt').readlines()
        for g in genre_file:
            if g not in genres:
                genres.append(str(g).strip())
        combo.addItems(tuple(genres))
        combo.setCurrentText('')


    def clearFields(self):
        self.title_txt.setText('')
        self.artist_txt.setText('')
        self.trackNumber_txt.setText('')
        self.album_txt.setText('')
        self.albumArtist_txt.setText('')
        self.genre_txt.setCurrentText('')
        self.year_txt.setText('')
        self.loadLyrics_txt.setText('')
        self.loadCover_txt.setText('')
        self.loadAudio_txt.setText('')
        self.composer_txt.setText('')
        self.comments_txt.setText('')

    
    def clearFields_2(self):
        self.title_txt.setText('')
        self.artist_txt.setText('')
        self.trackNumber_txt.setText('')
        self.album_txt.setText('')
        self.albumArtist_txt.setText('')
        self.genre_txt.setCurrentText('')
        self.year_txt.setText('')
        self.loadLyrics_txt.setText('')
        self.loadCover_txt.setText('')
        self.composer_txt.setText('')
        self.comments_txt.setText('')


    def popup_warning(self, msg):
        popup = QMessageBox()
        popup.setWindowTitle(_('Warning'))
        popup.setWindowIcon(self.winIcon)
        popup.setIcon(popup.Warning)
        popup.setText(msg)
        popup.exec_()


    def popup_info(self, msg):
        popup = QMessageBox()
        popup.setWindowTitle(_('Information'))
        popup.setWindowIcon(self.winIcon)
        popup.setIcon(popup.Information)
        popup.setText(msg)
        popup.exec_()


    def checkForUpdates(self):
        __version__ = 0.5
        new_version = urlopen('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/version').read()
        if float(new_version) > float(__version__):
            Utils.popup_info(self, msg=_('There is a new software version available.'))
            webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/releases/')
        else:
            Utils.popup_info(self, msg=_('You have the latest software version installed.'))


    def checkAutoUpdates(self):
        __version__ = 0.5
        new_version = urlopen('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/version').read()
        if float(new_version) > float(__version__):
            Utils.popup_info(self, msg=_('There is a new software version available.'))
            webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/releases/')
            

    def aboutEyed3(self):
        logo = QLabel('')
        logo.setStyleSheet('background-image: url(/usr/share/icons/hicolor/256x256/apps/eyed3.png); background-repeat: no-repeat; width: 100%; height: 100%;')
        logo.setWindowIcon(QIcon(self.winIcon))
        logo.setFixedSize(256, 256)
        name = QLabel('eyeD3 Gui')
        name.setFixedHeight(20)
        version = QLabel('v0.5')
        version.setFixedHeight(10)

        license_file = open('/usr/share/doc/eyed3gui/COPYING', 'r').read()
        licen = QTextEdit()
        licen.setReadOnly(True)
        licen.setText(license_file)

        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(name)
        layout.addWidget(version)
        layout.addWidget(licen)

        layout.setAlignment(logo, Qt.AlignHCenter)
        layout.setAlignment(name, Qt.AlignHCenter)
        layout.setAlignment(version, Qt.AlignHCenter)

        about = QDialog()
        about.setWindowTitle(_('About eyeD3 Gui'))
        about.setWindowIcon(self.winIcon)
        about.setFixedSize(450, 500)
        about.setLayout(layout)
        about.exec_()
            

if __name__ == '__main__':
    u = Utils()
    u.aboutEyed3()
