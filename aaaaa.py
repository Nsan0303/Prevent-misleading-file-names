import os, sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
import tkinter
from tkinter import filedialog
import glob
import time
from plyer import notification
import threading
import tkinter as tk


def quit_app():
    False
    icon.stop()

def setting_app():
    global idir
    global file_path
    idir = 'C:\\'
    file_path = tkinter.filedialog.askdirectory(initialdir=idir)

def run_app():
    while True:
        list1 = os.listdir(file_path)
        conditions = '最新版'
        for udon in list1:
            if conditions in udon:
                notification.notify(
                    title="最新版撲滅君",
                    message="'ヽ(｀Д´#)ﾉお前、最新版なんてわかりにくい名前を付けんじゃねぇ'",
                    app_name="最新版撲滅君",
                    app_icon="image.ico",
                    timeout=10
                )
                False
                return
            else:
                # print("false")
                time.sleep(1)


def run_app_thread():
    t1 = threading.Thread(target=run_app)
    t1.start()

image = Image.open('image.ico')
menu = Menu(MenuItem('Quit', quit_app), MenuItem('settingdirectory', setting_app), MenuItem('run', run_app_thread))
icon = Icon(name='test', icon=image, title='pystray App', menu=menu)
icon.run()

# https://office54.net/python/app/plyer-notification-banner
# https://wynn-blog.com/file-operation-with-python-gui
#   