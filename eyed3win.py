#!/usr/bin/python3
# -*- encoding:utf-8 -*-

__version__ = 0.2

from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import *
from eyed3 import id3
from time import sleep
from threading import Thread
from about import About
import os
import sys
import ttips
import gettext
import eyed3
import webbrowser

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

"""pid = os.getpid()
pidfile = os.path.expanduser('~/AppData/Local/Temp/eyed3.tmp')
if not os.path.exists(pidfile):
    os.system(f'Dir > {pidfile}')
    os.system(f'echo {pid} >> {pidfile}')
else:
    sys.exit(-1)"""


class EyedWin:
    def __init__(self, master=None):
        Thread(target=self.user_check_updates, daemon=True).start()

        # preparing containers
        c1 = Frame(master)
        c1['pady'] = 20
        c1.pack()

        c2 = Frame(master)
        c2.pack()

        c3 = Frame(master)
        c3['pady'] = 20
        c3.pack()

        c4 = Frame(master)
        c4.pack()

        c5 = Frame(master)
        c5.pack()

        c6 = Frame(master)
        c6.pack()

        c7 = Frame(master)
        c7.pack()

        # Menubar
        menubar = Menu(window, tearoff=0, bd=0, bg='#d9d9d9')
        file = Menu(menubar, tearoff=0, bd=0)
        menubar.add_cascade(label=_('File'), menu=file)
        file.add_command(label=_('Load audio file...'), accelerator='Ctrl+O', command=lambda: self.btnLoadAudio())
        file.add_command(label=_('Save all tags'), accelerator='Ctrl+S', command=lambda: self.btnSaveTags())
        file.add_separator()
        file.add_command(label=_('Exit'), accelerator='Ctrl+Q', command=lambda: window.destroy())

        help = Menu(menubar, tearoff=0, bd=0)
        menubar.add_cascade(label=_('Help'), menu=help)
        help.add_command(label='GitHub', accelerator='Ctrl+G', command=lambda: window.bind('<Button-1>', webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui')))
        help.add_command(label=_('License'), accelerator='Ctrl+I', command=lambda: window.bind('<Button-1>', webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/blob/master/LICENSE')))
        help.add_command(label=_('Documentation'), accelerator='Ctrl+D', command=lambda: window.bind('<Button-1>', webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui#eyed3-gtk-gui')))
        help.add_command(label=_('Search for new updates...'), accelerator='Ctrl+N', command=lambda: self.check_updates())
        help.add_separator()
        help.add_command(label=_('About'), accelerator='Ctrl+H', command=lambda: About.about(self, window=window))

        window.config(menu=menubar)

        # preparing interface
        self.lbtitle = Label(c1, text=_('Title'))
        self.lbtitle.pack(side=LEFT, padx=5)
        self.txttitle = Entry(c1, width=40, bg='white', fg='black')
        self.txttitle.pack(side=LEFT)

        self.lbartist = Label(c1, text=_('Artist'))
        self.lbartist.pack(side=LEFT, padx=5)
        self.txtartist = Entry(c1, width=40, bg='white', fg='black')
        self.txtartist.pack(side=LEFT)

        self.lbtrack_num = Label(c1, text=_('Track Number'))
        self.lbtrack_num.pack(side=LEFT, padx=5)
        self.txttrack_num = Entry(c1, width=4, bg='white', fg='black')
        self.txttrack_num.pack(side=LEFT)

        self.lbalbum = Label(c2, text=_('Album'))
        self.lbalbum.pack(side=LEFT, padx=5)
        self.txtalbum = Entry(c2, width=36, bg='white', fg='black')
        self.txtalbum.pack(side=LEFT)

        self.lbalbum_artist = Label(c2, text=_('Album Artist'))
        self.lbalbum_artist.pack(side=LEFT, padx=5)
        self.txtalbum_artist = Entry(c2, width=36, bg='white', fg='black')
        self.txtalbum_artist.pack(side=LEFT)

        self.btnremove_all_tags = Button(c2, text=_('Remove All Tags'), width=15, command=self.btnRemoveAllTags)
        self.btnremove_all_tags.pack(side=LEFT, padx=5)
        ttips.Create(self.btnremove_all_tags, text=_('Remove completly all tags from audio'))

        self.lbgenre = Label(c3, text=_('Genre'))
        self.lbgenre.pack(side=LEFT, padx=5)
        self.txtgenre = Entry(c3, width=15, bg='white', fg='black')
        self.txtgenre.pack(side=LEFT)

        self.lbyear = Label(c3, text=_('Year'))
        self.lbyear.pack(side=LEFT, padx=5)
        self.txtyear = Entry(c3, width=5, bg='white', fg='black')
        self.txtyear.pack(side=LEFT)

        self.txtlyrics = Entry(c3, width=31, bg='white', fg='black')
        self.txtlyrics.pack(side=LEFT, padx=5)
        ttips.Create(self.txtlyrics, text=_('Select a txt file with lyrics by clicking the button'))
        self.btnlyrics = Button(c3, text=_('Lyrics'), command=self.btnLoadLyrics)
        self.btnlyrics.pack(side=LEFT)
        ttips.Create(self.btnlyrics, text=_('Select a txt file with lyrics'))

        self.txtcover = Entry(c3, width=31, bg='white', fg='black')
        self.txtcover.pack(side=LEFT, padx=5)
        ttips.Create(self.txtcover, text=_('Select an image file as front cover by clicking the button'))
        self.btncover = Button(c3, text=_('Cover'), command=self.btnLoadCover)
        self.btncover.pack(side=LEFT)
        ttips.Create(self.btncover, text=_('Select an image file as front cover'))

        self.lbcommposer = Label(c4, text=_('Composer(s)'))
        self.lbcommposer.pack(side=LEFT)
        self.txtcomposer = Entry(c4, width=102, bg='white', fg='black')
        self.txtcomposer.pack(side=LEFT, padx=5)

        self.lbcomment = Label(c5, text=_('Comments'))
        self.lbcomment.pack(side=LEFT, padx=5)
        self.txtcomment = Text(c5, width=105, height=5, bg='white', fg='black')
        self.txtcomment.pack(side=LEFT, pady=15)

        self.txtload_audio = Entry(c6, width=53, bg='white', fg='black')
        self.txtload_audio.pack(side=LEFT, padx=5, pady=2)
        ttips.Create(self.txtload_audio, text=_('Select an audio file by clicking the button'))
        self.btnload_audio = Button(c6, text=_('Load Audio'), width=15, command=self.btnLoadAudio)
        self.btnload_audio.pack(side=LEFT)
        ttips.Create(self.btnload_audio, text=_('Select an audio file, Ctrl+O'))

        self.btnclear_fields = Button(c6, text=_('Clear Fields'), width=15, command=self.btnClearFields)
        self.btnclear_fields.pack(side=LEFT, padx=5)
        ttips.Create(self.btnclear_fields, text=_('Clear all fields, Ctrl+L'))

        self.btnsave_tags = Button(c6, text=_('Save Tags'), width=16, command=self.btnSaveTags)
        self.btnsave_tags.pack(side=LEFT)
        ttips.Create(self.btnsave_tags, text=_('Save all tags into the audio file, Ctrl+S'))

        self.bgimg = PhotoImage(file='icons/bg.png')

        self.bg = Label(c7, image=self.bgimg)
        self.bg.pack(pady=30)
        self.bg.image = self.bgimg

        self.mouseMenu = Menu(window, tearoff=0)
        self.mouseMenu.add_command(label=_('Cut'))
        self.mouseMenu.add_command(label=_('Copy'))
        self.mouseMenu.add_command(label=_('Paste'))

        # Binds
        window.bind('<Control-O>', lambda e: self.btnLoadAudio())
        window.bind('<Control-o>', lambda e: self.btnLoadAudio())
        window.bind('<Control-S>', lambda e: self.btnSaveTags())
        window.bind('<Control-s>', lambda e: self.btnSaveTags())
        window.bind('<Control-Q>', lambda e: window.destroy())
        window.bind('<Control-q>', lambda e: window.destroy())
        window.bind('<Control-G>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui'))
        window.bind('<Control-g>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui'))
        window.bind('<Control-I>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/blob/master/LICENSE'))
        window.bind('<Control-i>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/blob/master/LICENSE'))
        window.bind('<Control-D>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui#eyed3-gtk-gui'))
        window.bind('<Control-d>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui#eyed3-gtk-gui'))
        window.bind('<Control-N>', lambda e: self.check_updates())
        window.bind('<Control-n>', lambda e: self.check_updates())
        window.bind('<Control-H>', lambda e: About.about(self, window=window))
        window.bind('<Control-h>', lambda e: About.about(self, window=window))
        window.bind('<Control-L>', lambda e: self.btnClearFields())
        window.bind('<Control-l>', lambda e: self.btnClearFields())
        window.bind('<Button-3><ButtonRelease-3>', self.mouse)

    # mouse menu
    def mouse(self, event):
        w = event.widget
        self.mouseMenu.entryconfigure(_("Cut"), command=lambda: w.event_generate('<<Cut>>'))
        self.mouseMenu.entryconfigure(_("Copy"), command=lambda: w.event_generate('<<Copy>>'))
        self.mouseMenu.entryconfigure(_("Paste"), command=lambda: w.event_generate('<<Paste>>'))
        self.mouseMenu.tk_popup(event.x_root, event.y_root)

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
        composer = self.txtcomposer.get()
        comment = str(self.txtcomment.get(1.0, END))
        if audio == '':
            showerror(title=_('Fail'), message=_('You need to load an audio file to save tags.'))
        else:
            mp3 = eyed3.load(audio)
            mp3.initTag(version=(2, 4, 0))
            mp3.tag.title = title
            mp3.tag.artist = artist
            mp3.tag.album = album
            mp3.tag.album_artist = albumartist
            mp3.tag.genre = genre
            mp3.tag.track_num = tracknum
            mp3.tag.recording_date = year
            mp3.tag.release_date = year
            mp3.tag.original_release_date = year
            mp3.tag.composer = composer
            mp3.tag.comments.set(comment.replace('\n', ' '))
            if lyrics == '':
                pass
            if lyrics != '':
                mp3.tag.lyrics.set(open(lyrics).read())
            if cover == '':
                showinfo(title=_('Error'), message=_("Cover file wasn't selected."))
            if cover != '':
                imageData = open(cover, 'rb').read()
                mp3.tag.images.set(3, imageData, 'image/jpg')
                mp3.tag.save()
                sleep(0.2)
                self.btnClearFields()
                showinfo(title='Status', message=_('All audio tags are saved.'), detail=_('Reaload the audio file to make sure the new tags were set.'))

    # audio file chooser
    def btnLoadAudio(self):
        audio = askopenfilename(title=_('Open an audio file'), initialdir='~/Music', filetypes={'audio .mp3'})
        mp3 = eyed3.load(audio).tag
        mp3.parse(audio, [2, 4, 0])
        mp3.save(audio)
        sleep(0.2)
        self.btnClearFields()
        self.txtload_audio.insert(INSERT, audio)
        self.displayinfo()

    # lyrics file chooser
    def btnLoadLyrics(self):
        lyrics = askopenfilename(title=_('Open a text file with lyrics'), initialdir='~/', filetypes={'text .txt'})
        if self.txtlyrics.get() == '':
            self.txtlyrics.insert(INSERT, lyrics)
            #self.txtlyrics.insert(1, '\\')
        else:
            self.txtlyrics.delete(0, END)
            self.txtlyrics.insert(INSERT, lyrics)

    # cover file chooser and buttons
    def btnLoadCover(self):
        cover = askopenfilename(title=_('Choose an image file as cover'), initialdir='~/Pictures', filetypes={('images', ('.jpg', '.jpeg', '.png'))})
        if self.txtcover.get() == '':
            self.txtcover.insert(INSERT, cover)
            #self.txtcover.insert(1, '\\')
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
        self.txtcomposer.delete(0, END)
        self.txtcomment.delete(1.0, END)

    # display existing tags when load audio
    def displayinfo(self):
        tag = id3.Tag()
        tag.parse(self.txtload_audio.get())
        self.txttitle.insert(INSERT, str(tag.title))
        self.txtartist.insert(INSERT, str(tag.artist))
        self.txtalbum.insert(INSERT, str(tag.album))
        self.txtalbum_artist.insert(INSERT, str(tag.album_artist))
        self.txtgenre.insert(INSERT, str(tag.genre))
        self.txtcomposer.insert(INSERT, str(tag.composer))
        if str(tag.track_num):
            self.txttrack_num.insert(INSERT, str(tag.track_num[0]).replace('None', '0'))
        else:
            self.txttrack_num.insert(INSERT, str(tag.track_num[2]))

        self.txtyear.insert(INSERT, str(tag.recording_date).replace('None', ''))
        self.txtcomment.insert(INSERT, str(tag.comments[0].text))

    def btnRemoveAllTags(self):
        audio = self.txtload_audio.get()
        if audio == '':
            showerror(title=_('Fail'), message=_('You need to load an audio file to remove tags.'))
        else:
            id3.tag.Tag.remove(audio)
            mp3 = eyed3.id3.Tag()
            mp3.parse(audio, [2, 4, 0])
            mp3.save(audio)
            self.txttitle.delete(0, END)
            self.txtartist.delete(0, END)
            self.txtalbum.delete(0, END)
            self.txtalbum_artist.delete(0, END)
            self.txtgenre.delete(0, END)
            self.txtyear.delete(0, END)
            self.txttrack_num.delete(0, END)
            self.txtlyrics.delete(0, END)
            self.txtcover.delete(0, END)
            self.txtcomposer.delete(0, END)
            self.txtcomment.delete(1.0, END)

    def check_updates(self):
        from urllib.request import urlopen
        actual_version = __version__
        new_version = urlopen('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/version').read()
        if float(new_version) > float(actual_version):
            showinfo(title=_('New update'), message=_("There's a new software version available to download."))
            webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/releases')
        if float(new_version) == float(actual_version):
            showinfo(title=_('Updated'), message=_('Software has the last version installed.'))
        else:
            pass

    def user_check_updates(self):
        from urllib.request import urlopen
        actual_version = __version__
        new_version = urlopen('https://raw.githubusercontent.com/Alexsussa/eyed3-gtk-gui/master/version').read()
        if float(new_version) > float(actual_version):
            showinfo(title=_('New update'), message=_("There's a new software version available to download."))
            Thread(target=webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/releases')).start()
        else:
            pass


window = Tk()
EyedWin(window)
icon_win = PhotoImage(file='icons/eyed3.png')
window.tk.call('wm', 'iconphoto', window._w, icon_win)
window.title('eyeD3')
window.resizable(False, False)
#window.geometry('800x550')
window.mainloop()
"""if window.destroy or window.quit:
    os.unlink(pidfile)"""
