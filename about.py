#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from tkinter import *
from threading import Thread
import gettext
import os
import webbrowser

appname = 'eyed3win'
dirname = os.path.join('locale')
gettext.bindtextdomain(appname, dirname)
gettext.textdomain(appname)
_ = gettext.gettext


class About(Thread, Toplevel):
    def __init__(self):
        Thread.__init__(self)

    def about(self, window):
        popup = Toplevel()
        icon_win = PhotoImage(file='icons/eyed3.png')
        popup.tk.call('wm', 'iconphoto', popup._w, icon_win)
        popup.title(_('About'))
        popup.geometry('500x430')
        popup.resizable(0, 0)
        popup.transient(window)
        popup.grab_set()
        popup.focus_force()

        img = PhotoImage(file='icons/eyed3.png')
        bg = Label(popup, image=img, cursor='hand2')
        bg.pack(pady=10)
        bg.image = img

        github = Label(popup, text='GitHub', fg='blue', cursor='hand2', underline=0)
        github.pack(pady=12)

        license = Label(popup, text=_('License'), fg='blue', cursor='hand2', underline=0)
        license.pack()

        copy = Label(popup, text=_('All Rights Reserved © 2020 - 2021'), fg='gray', cursor='hand2')
        copy.pack(side=LEFT, anchor='sw')

        dev = Label(popup, text='Alex Pinheiro', fg='gray', cursor='hand2')
        dev.pack(side=RIGHT, anchor='se')

        # Binds
        bg.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui'))
        github.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui'))
        license.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/blob/master/LICENSE'))
        copy.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/eyed3-gtk-gui/blob/master/LICENSE'))
        dev.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa'))
