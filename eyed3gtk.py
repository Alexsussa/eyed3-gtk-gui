#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys
import locale
import gettext
from eyed3 import id3

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
        self.loadaudio = builder.get_object('loadaudio')
        self.loadlyrics = builder.get_object('loadlyrics')
        self.loadcover = builder.get_object('loadcover')
        self.loading = builder.get_object('spinner')
        self.aviso = builder.get_object('aviso')
        self.lbaviso = builder.get_object('lbaviso')
        self.about = builder.get_object('about')

        # this makes the about window's close button works
        self.about.connect('response', lambda d, r: d.hide())

    # menu help >> about
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

        """mp3 = eyed3.load(audio)
        mp3.tag.title = title
        mp3.tag.artist = artist
        mp3.tag.album = album
        mp3.tag.album_artist = albumartist
        mp3.tag.genre = genre
        mp3.tag.track_num = tracknum
        mp3.tag.save()"""

        os.system(f'eyeD3 -t "{title}" -a "{artist}" -A "{album}" -b "{albumartist}" -G "{genre}" -n "{tracknum}" -Y "{year}" "{audio}"')

        """os.system(f'eyeD3 -a "{artist}" "{audio}"')
        os.system(f'eyeD3 -A "{album}" "{audio}"')
        os.system(f'eyeD3 -b "{albumartist}" "{audio}"')
        os.system(f'eyeD3 -G "{genre}" "{audio}"')
        os.system(f'eyeD3 -n "{tracknum}" "{audio}"')
        os.system(f'eyeD3 -Y "{year}" "{audio}"')"""

        os.system(f'eyeD3 --add-image "{cover}":FRONT_COVER "{audio}"')
        os.system(f'eyeD3 --add-lyrics "{lyrics}" "{audio}"')

        # reopen the last audio file to update fields with the new tags
        self.on_btnclearfields_clicked(button=None)
        self.on_loadaudio_file_activated(button=True)
        self.aviso.show()

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

    def on_btnremove_clicked(self, button):
        audio = self.txtaudio.get_text()
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

    # just destroy main window
    def on_eyed3_destroy(self, window):
        Gtk.main_quit()
        os.unlink(pidfile)


builder = Gtk.Builder()
builder.set_translation_domain(appname)
builder.add_from_file('eyed3.ui')
builder.connect_signals(EyedGtk())
janela = builder.get_object(appname)
janela.show_all()
Gtk.main()
