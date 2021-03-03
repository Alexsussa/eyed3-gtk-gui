#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread
import os
import sys
import locale
import gettext
import webbrowser
from eyed3 import id3

__version__ = 0.2

appname = 'eyed3'
dirname = os.path.join(os.path.realpath('locale'))

locale.bindtextdomain(appname, dirname)
locale.textdomain(appname)

gettext.bindtextdomain(appname, dirname)
gettext.textdomain(appname)
_ = gettext.gettext

pid = str(os.getpid())
pidfile = os.path.join('/tmp/eyed3.pid')
if not os.path.isfile(pidfile):
    os.system(f'touch {pidfile}')
    os.system(f'echo {pid} >> {pidfile}')
else:
    sys.exit(-1)


class EyedGtk(Gtk.Window):
    def __init__(self):
        self.txttitle = builder.get_object('txttitle')
        self.txtartist = builder.get_object('txtartist')
        self.txtalbum = builder.get_object('txtalbum')
        self.txtalbumartist = builder.get_object('txtalbumartist')
        self.txtgenre = builder.get_object('txtgenre')
        self.txtyear = builder.get_object('txtyear')
        self.txttracknum = builder.get_object('txttracknum')
        self.txtaudio = builder.get_object('txtaudio')
        self.txtlyrics = builder.get_object('txtlyrics')
        self.txtcover = builder.get_object('txtcover')
        self.txtComposer = builder.get_object('txtComposer')
        self.txtComments = builder.get_object('txtComments')
        self.buffComments = builder.get_object('buffComments')
        self.loadaudio = builder.get_object('loadaudio')
        self.loadlyrics = builder.get_object('loadlyrics')
        self.loadcover = builder.get_object('loadcover')
        self.loading = builder.get_object('spinner')
        self.aviso = builder.get_object('aviso')
        self.lbaviso = builder.get_object('lbaviso')
        self.updates = builder.get_object('updates')
        self.lbupdate = builder.get_object('lbupdates')
        self.newupdate = builder.get_object('newupdate')
        self.lbnewupdate = builder.get_object('lbnewupdate')
        self.about = builder.get_object('about')

        self.check_updates()

        # this makes the about window's close button works
        self.about.connect('response', lambda d, r: d.hide())

    # menu file >> submenu
    def on_btnLoadAudio_activate(self, button):
        self.on_btnloadaudio_clicked(button)

    def on_btnSaveAllTags_activate(self, button):
        self.on_btnsavetags_clicked(button)

    def on_btnExit_activate(self, button):
        Gtk.main_quit()
        os.unlink(pidfile)

    # menu help >> about
    def on_btnGitHub_activate(self, button):
        webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui')

    def on_btnLicense_activate(self, button):
        webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/blob/master/LICENSE')

    def on_btnDoc_activate(self, button):
        webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui#eyed3-gtk-gui')

    def on_btnCheckUpdates_activate(self, button):
        from urllib.request import urlopen
        actual_version = __version__
        new_version = urlopen('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/version').read()
        if float(new_version) > float(actual_version):
            self.updates.show()
            self.lbupdate.set_text(_("There's a new software version available to download."))
        if float(new_version) == float(actual_version):
            self.newupdate.show()
            self.lbnewupdate.set_text(_('Software has the last version installed.'))
        else:
            pass

    def on_btnaboutmenu_activate(self, button):
        self.about.show()

    # save all new tags
    def on_btnsavetags_clicked(self, button):
        title = str(self.txttitle.get_text())
        artist = str(self.txtartist.get_text())
        album = str(self.txtalbum.get_text())
        albumartist = str(self.txtalbumartist.get_text())
        genre = str(self.txtgenre.get_text())
        year = self.txtyear.get_text()
        tracknum = self.txttracknum.get_text()
        lyrics = self.txtlyrics.get_text()
        cover = self.txtcover.get_text()
        audio = str(self.txtaudio.get_text())
        composer = str(self.txtComposer.get_text())
        start = self.buffComments.get_start_iter()
        end = self.buffComments.get_end_iter()
        comments = str(self.buffComments.get_text(start, end, False))
        if audio == '':
            self.aviso.show()
            self.lbaviso.set_text(_('You need to load an audio file to save tags.'))
        else:
            os.system(f'eyeD3 -t "{title}" -a "{artist}" -A "{album}" -b "{albumartist}" -G "{genre}" -n "{tracknum}" -Y "{year}" --release-date "{year}" --recording-date "{year}" --composer "{composer}" --comment "{comments}" "{audio}"')

            if lyrics == '':
                pass
            if lyrics != '':
                os.system(f'eyeD3 --add-lyrics "{lyrics}" "{audio}"')
            if cover == '':
                pass
            if cover != '':
                os.system(f'eyeD3 --add-image "{cover}":FRONT_COVER "{audio}"')

            # reopen the last audio file to update fields with the new tags
            self.on_btnclearfields_clicked(button=None)
            self.on_loadaudio_file_activated(button=True)
            self.aviso.show()
            self.lbaviso.set_text(_('All audio tags are saved.'))

    # audio file chooser and buttons
    def on_btnloadaudio_clicked(self, button):
        self.loadaudio.show()

    def on_btnloadaudioopen_clicked(self, button):
        audio = self.loadaudio.get_filename()
        os.system((f'eyeD3 "{audio}" --to-v2.4'))
        self.txtaudio.set_text(audio)
        self.loadaudio.hide()
        self.displayinfo()

    def on_btnloadaudiocance_clicked(self, button):
        self.loadaudio.hide()

    def on_loadaudio_file_activated(self, button):
        audio = self.loadaudio.get_filename()
        os.system((f'eyeD3 "{audio}" --to-v2.4'))
        self.txtaudio.set_text(audio)
        self.loadaudio.hide()
        self.displayinfo()

    # lyrics file chooser and buttons
    def on_btnloadlyrics_clicked(self, button):
        self.loadlyrics.show()

    def on_btnloadlyricsopen_clicked(self, button):
        lyrics = self.loadlyrics.get_filename()
        self.txtlyrics.set_text(lyrics)
        self.loadlyrics.hide()

    def on_btnloadlyricscancel_clicked(self, button):
        self.loadlyrics.hide()

    def on_loadlyrics_file_activated(self, button):
        lyrics = self.loadlyrics.get_filename()
        self.txtlyrics.set_text(lyrics)
        self.loadlyrics.hide()

    # cover file chooser and buttons
    def on_btnloadcover_clicked(self, button):
        self.loadcover.show()

    def on_btnloadcoveropen_clicked(self, button):
        cover = self.loadcover.get_filename()
        self.txtcover.set_text(cover)
        self.loadcover.hide()

    def on_btnloadcovercancel_clicked(self, button):
        self.loadcover.hide()

    def on_loadcover_file_activated(self, button):
        cover = self.loadcover.get_filename()
        self.txtcover.set_text(cover)
        self.loadcover.hide()

    # clear all fields
    def on_btnclearfields_clicked(self, button):
        self.txttitle.set_text(text='')
        self.txtartist.set_text(text='')
        self.txtalbum.set_text(text='')
        self.txtalbumartist.set_text(text='')
        self.txtgenre.set_text(text='')
        self.txtyear.set_text(text='')
        self.txttracknum.set_text(text='')
        self.txtaudio.set_text(text='')
        self.txtlyrics.set_text(text='')
        self.txtcover.set_text(text='')
        self.txtComposer.set_text(text='')
        self.buffComments.set_text(text='')

    def displayinfo(self):
        tag = id3.Tag()
        tag.parse(self.txtaudio.get_text())
        self.txttitle.set_text(str(tag.title))
        self.txtartist.set_text(str(tag.artist))
        self.txtalbum.set_text(str(tag.album))
        self.txtalbumartist.set_text(str(tag.album_artist))
        self.txtgenre.set_text(str(tag.genre))
        if str(tag.track_num):
            self.txttracknum.set_text(str(tag.track_num[0]).replace('None', '0'))
        else:
            self.txttracknum.set_text(str(tag.track_num[2]))

        if str(tag.release_date):
            self.txtyear.set_text(str(tag.release_date).replace('None', '0'))
        else:
            self.txtyear.set_text(str(tag.release_date[:]))

        self.txtComposer.set_text(str(tag.composer))
        self.buffComments.set_text(str(tag.comments[0].text))

    def on_btnremove_clicked(self, button):
        audio = self.txtaudio.get_text()
        if audio == '':
            self.aviso.show()
            self.lbaviso.set_text(_('You need to load an audio file to remove tags.'))
        else:
            os.system(f'eyeD3 "{audio}" --remove-all')
            os.system((f'eyeD3 "{audio}" --to-v2.4'))
            self.txttitle.set_text(text='')
            self.txtartist.set_text(text='')
            self.txtalbum.set_text(text='')
            self.txtalbumartist.set_text(text='')
            self.txtgenre.set_text(text='')
            self.txtyear.set_text(text='')
            self.txttracknum.set_text(text='')
            self.txtlyrics.set_text(text='')
            self.txtcover.set_text(text='')

    def on_btnavisok_clicked(self, button):
        self.aviso.hide()

    def on_btnUpdateOk_clicked(self, button):
        self.updates.hide()
        webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/releases')

    def on_btnUpdateOkNew_clicked(self, button):
        self.newupdate.hide()

    # just destroy main window
    def on_eyed3_destroy(self, window):
        Gtk.main_quit()
        os.unlink(pidfile)

    def check_updates(self):
        from urllib.request import urlopen
        actual_version = __version__
        new_version = urlopen('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/version').read()
        if float(new_version) > float(actual_version):
            self.updates.show()
            self.lbupdate.set_text(_("There's a new software version available to download."))
        else:
            pass


builder = Gtk.Builder()
builder.set_translation_domain(appname)
builder.add_from_file('eyed3.ui')
builder.connect_signals(EyedGtk())
janela = builder.get_object(appname)
janela.show_all()
Gtk.main()
