#!/usr/bin/python3
# -*- encoding:utf-8 -*-

__version__ = 0.1

from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import *
import os
import sys
import ttips
import subprocess
import gettext
import eyed3
from eyed3 import id3

# loads translations
if sys.platform.startswith('win'):
    import locale
if os.getenv('LANG') is None:
    lang, enc = locale.getdefaultlocale()
    os.environ['LANG'] = lang

appname = 'eyed3win'
dirname = os.path.join('locale')
gettext.bindtextdomain(appname, dirname)
gettext.textdomain(appname)
_ = gettext.gettext


class EyedWin:
    def __init__(self, master=None):
        # preparing containers
        c1 = Frame(master)
        c1['pady'] = 30
        c1.pack()

        c2 = Frame(master)
        c2.pack()

        c3 = Frame(master)
        c3['pady'] = 25
        c3.pack()

        c4 = Frame(master)
        c4.pack()

        c5 = Frame(master)
        c5.pack()

        # preparing interface
        self.lbtitle = Label(c1, text=_('Title'))
        self.lbtitle.pack(side=LEFT, padx=5)
        self.txttitle = Entry(c1, width=40)
        self.txttitle.pack(side=LEFT)

        self.lbartist = Label(c1, text=_('Artist'))
        self.lbartist.pack(side=LEFT, padx=5)
        self.txtartist = Entry(c1, width=40)
        self.txtartist.pack(side=LEFT)

        self.lbtrack_num = Label(c1, text=_('Track Number'))
        self.lbtrack_num.pack(side=LEFT, padx=5)
        self.txttrack_num = Entry(c1, width=4)
        self.txttrack_num.pack(side=LEFT)

        self.lbalbum = Label(c2, text=_('Album'))
        self.lbalbum.pack(side=LEFT, padx=5)
        self.txtalbum = Entry(c2, width=36)
        self.txtalbum.pack(side=LEFT)

        self.lbalbum_artist = Label(c2, text=_('Album Artist'))
        self.lbalbum_artist.pack(side=LEFT, padx=5)
        self.txtalbum_artist = Entry(c2, width=36)
        self.txtalbum_artist.pack(side=LEFT)

        self.btnremove_all_tags = Button(c2, text=_('Remove All Tags'), width=15, command=self.btnRemoveAllTags)
        self.btnremove_all_tags.pack(side=LEFT, padx=5)
        ttips.Create(self.btnremove_all_tags, text=_('Remove completly all tags from audio'))

        self.lbgenre = Label(c3, text=_('Genre'))
        self.lbgenre.pack(side=LEFT, padx=5)
        self.txtgenre = Entry(c3, width=15)
        self.txtgenre.pack(side=LEFT)

        self.lbyear = Label(c3, text=_('Year'))
        self.lbyear.pack(side=LEFT, padx=5)
        self.txtyear = Entry(c3, width=5)
        self.txtyear.pack(side=LEFT)

        self.txtlyrics = Entry(c3, width=31)
        self.txtlyrics.pack(side=LEFT, padx=5)
        ttips.Create(self.txtlyrics, text=_('Select a txt file with lyrics by clicking the button'))
        self.btnlyrics = Button(c3, text=_('Lyrics'), command=self.btnLoadLyrics)
        self.btnlyrics.pack(side=LEFT)
        ttips.Create(self.btnlyrics, text=_('Select a txt file with lyrics'))

        self.txtcover = Entry(c3, width=31)
        self.txtcover.pack(side=LEFT, padx=5)
        ttips.Create(self.txtcover, text=_('Select an image file as front cover by clicking the button'))
        self.btncover = Button(c3, text=_('Cover'), command=self.btnLoadCover)
        self.btncover.pack(side=LEFT)
        ttips.Create(self.btncover, text=_('Select an image file as front cover'))

        self.txtload_audio = Entry(c4, width=53)
        self.txtload_audio.pack(side=LEFT, padx=5)
        ttips.Create(self.txtload_audio, text=_('Select an audio file by clicking the button'))
        self.btnload_audio = Button(c4, text=_('Load Audio'), width=15, command=self.btnLoadAudio)
        self.btnload_audio.pack(side=LEFT)
        ttips.Create(self.btnload_audio, text=_('Select an audio file'))

        self.btnclear_fields = Button(c4, text=_('Clear Fields'), width=15, command=self.btnClearFields)
        self.btnclear_fields.pack(side=LEFT, padx=5)
        ttips.Create(self.btnclear_fields, text=_('Clear all fields'))

        self.btnsave_tags = Button(c4, text=_('Save Tags'), width=16, command=self.btnSaveTags)
        self.btnsave_tags.pack(side=LEFT)
        ttips.Create(self.btnsave_tags, text=_('Save all tags into the audio file'))

        self.bgimg = PhotoImage(file='icons/bg.png')

        self.bg = Label(c5, image=self.bgimg)
        self.bg.pack(pady=30)

        self.bg.image = self.bgimg

    # save all new tags
    def btnSaveTags(self):
        title = self.txttitle.get()
        artist = self.txtartist.get()
        album = self.txtalbum.get()
        albumartist = self.txtalbum_artist.get()
        genre = self.txtgenre.get()
        year = self.txtyear.get()
        tracknum = self.txttrack_num.get()
        lyrics = self.txtlyrics.get()
        cover = self.txtcover.get()
        audio = self.txtload_audio.get()

        mp3 = eyed3.load(audio)
        mp3.tag.title = title
        mp3.tag.artist = artist
        mp3.tag.album = album
        mp3.tag.album_artist = albumartist
        mp3.tag.genre = genre
        mp3.tag.track_num = tracknum
        #mp3.tag.release_date = year
        mp3.tag.save()

        subprocess.Popen(f'eyeD3 -Y "{year}" "{audio}"', shell=True)
        subprocess.Popen(f'eyeD3 --add-lyrics "{lyrics}" "{audio}"', shell=True)
        subprocess.Popen(f'eyeD3 --add-image "{cover}":FRONT_COVER "{audio}"', shell=True)

        """os.system(f'eyeD3 -t "{title}" "{audio}"')
        os.system(f'eyeD3 -a "{artist}" "{audio}"')
        os.system(f'eyeD3 -A "{album}" "{audio}"')
        os.system(f'eyeD3 -b "{albumartist}" "{audio}"')
        os.system(f'eyeD3 -G "{genre}" "{audio}"')
        os.system(f'eyeD3 -n "{tracknum}" "{audio}"')"""

        self.btnClearFields()

        popup = showinfo(title='Status', message=_('All audio tags are saved.'), detail=_('Reaload the audio file to make sure the new tags were set.'))

    # audio file chooser
    def btnLoadAudio(self):
        audio = askopenfilename(title=_('Open an audio file'), initialdir='~/', filetypes={'audio .mp3'})
        subprocess.Popen((f'eyeD3 "{audio}" --to-v2.4'), shell=True)
        self.btnClearFields()
        self.txtload_audio.insert(INSERT, audio)
        self.displayinfo()

    # lyrics file chooser
    def btnLoadLyrics(self):
        lyrics = askopenfilename(title=_('Open a text file with lyrics'), initialdir='~/', filetypes={'text .txt'})
        if self.txtlyrics.get() == '':
            self.txtlyrics.insert(INSERT, lyrics)
            self.txtlyrics.insert(1, '\\')
        else:
            self.txtlyrics.delete(0, END)
            self.txtlyrics.insert(INSERT, lyrics)

    # cover file chooser and buttons
    def btnLoadCover(self):
        cover = askopenfilename(title=_('Choose an image file as cover'), initialdir='~/', filetypes={('images', ('.jpg', '.jpeg', '.png', '.gif'))})
        if self.txtcover.get() == '':
            self.txtcover.insert(INSERT, cover)
            self.txtcover.insert(1, '\\')
        else:
            self.txtcover.delete(0, END)
            self.txtcover.insert(INSERT, cover)

    # clear all fields
    def btnClearFields(self):
        self.txttitle.delete(0, END)
        self.txtartist.delete(0, END)
        self.txtalbum.delete(0, END)
        self.txtalbum_artist.delete(0, END)
        self.txtgenre.delete(0, END)
        self.txtyear.delete(0, END)
        self.txttrack_num.delete(0, END)
        self.txtload_audio.delete(0, END)
        self.txtlyrics.delete(0, END)
        self.txtcover.delete(0, END)

    # display existing tags when load audio
    def displayinfo(self):
        tag = id3.Tag()
        tag.parse(self.txtload_audio.get())
        self.txttitle.insert(INSERT, str(tag.title))
        self.txtartist.insert(INSERT, str(tag.artist))
        self.txtalbum.insert(INSERT, str(tag.album))
        self.txtalbum_artist.insert(INSERT, str(tag.album_artist))
        self.txtgenre.insert(INSERT, str(tag.genre))
        if str(tag.track_num):
            self.txttrack_num.insert(INSERT, str(tag.track_num[0]).replace('None', '0'))
        else:
            self.txttrack_num.insert(INSERT, str(tag.track_num[2]))

        if str(tag.release_date):
            self.txtyear.insert(INSERT, str(tag.release_date).replace('None', '0'))
        else:
            self.txtyear.insert(INSERT, str(tag.release_date[:]))

    def btnRemoveAllTags(self):
        audio = self.txtload_audio.get()
        mp3 = eyed3.load(audio)
        subprocess.Popen(f'eyeD3 "{audio}" --remove-all', shell=True)
        subprocess.Popen(f'eyeD3 "{audio}" --to-v2.4', shell=True)
        mp3.tag.remove(filename=audio)
        self.txttitle.delete(0, END)
        self.txtartist.delete(0, END)
        self.txtalbum.delete(0, END)
        self.txtalbum_artist.delete(0, END)
        self.txtgenre.delete(0, END)
        self.txtyear.delete(0, END)
        self.txttrack_num.delete(0, END)
        self.txtlyrics.delete(0, END)
        self.txtcover.delete(0, END)


window = Tk()
EyedWin(window)
icon_win = PhotoImage(file='icons/eyed3.png')
window.tk.call('wm', 'iconphoto', window._w, icon_win)
window.title('eyeD3')
window.resizable(False, False)
window.geometry('800x550')
window.mainloop()
