#!/usr/bin/env python3

# PODCAST HANDLER by Claudio Barca (Copyright 2020 Claudio Barca)
# This software is distributed under GPL v. 3 license.
# See LICENSE file for details.

import traceback
import os
import datetime
import time
from mpd import MPDClient
import curses
from curses import wrapper

from podcasthnd.media import Media
from podcasthnd.item import Item
import podcasthnd.constants as constants

class WinMain:  # main window
    def __init__(self):
        begin_x = 2; begin_y = 2
        height = 20; width = (curses.COLS - 4)
        self.win = curses.newwin(height, width, begin_y, begin_x)

    def create(self):
        global item, media
        self.win.clear()
        self.win.addstr(1,   5, str('PODCAST HANDLER ver. ' + constants.version), curses.A_BOLD)
        self.win.addstr(3,   5, str('Host: ' + media.host), curses.A_BOLD)
        self.win.addstr(4,   5, str('Item: ' + item.url), curses.A_BOLD)

        self.win.addstr( 7,  5, 'Press p to toggle play/pause', curses.A_NORMAL)
        self.win.addstr( 8,  5, 'Press < to seek -10 secs', curses.A_NORMAL)
        self.win.addstr( 9,  5, 'Press > to seek +30 secs', curses.A_NORMAL)
        self.win.addstr(10,  5, 'Press s to seek for a position', curses.A_NORMAL)
        
        self.win.addstr(13,  5, 'Press r to restart item', curses.A_NORMAL)
        self.win.addstr(15,  5, 'Press b to close this screen and play in background', curses.A_NORMAL)
        self.win.addstr(16,  5, 'Press q to close this screen and stop audio', curses.A_NORMAL)
        
        if media.notseekable_flag:
            self.win.addstr( 5,12, '(Not seekable)', curses.A_BOLD)
        self.win.refresh()

    def get_value(self,question,line):  # prompt for a generic new value
        global media
        self.win.addstr(line, 5, question , curses.A_BOLD)
        self.win.refresh()
        self.win.nodelay(False)
        curses.echo()
        answer = self.win.getstr(line, 27 , 6)
        curses.noecho()
        self.win.nodelay(True)
        self.win.clear()
        self.create()
        return str(answer)[2:-1]

    def new_position(self):  # set new position
        question = 'Insert time (mm:ss):'
        line = 19               # line number of the text 
        s = self.get_value(question, line).split(':')
        hours   = int(str(s[0]))
        minutes = int(str(s[1]))
        newpos = (hours * 60) + minutes
        media.seek(newpos)

    def loop(self):
        global item, media, bar
        while True:
            self.win.nodelay(True)
            ch = self.win.getch()

            if ch == ord('q'):
                media.close()  #  stop and close mpd connectio
                break
            
            if ch == ord('b'):
                media.client.close()  # close mpd connection
                break

            if ch == ord('p'):
                media.toggle()
                self.win.refresh()

            if ch == ord('<'):
                media.seek('-10')
                self.win.refresh()

            if ch == ord('>'):
                media.seek('+30')
                self.win.refresh()

            if ch == ord('s'):  # get new position
                self.new_position()
                self.win.refresh()

            if ch == ord('r'):  # restart podcast
                media.client.play()
                media.seek('1')

            if media.client.status()['state'] == "play":
                my_time = media.time()
                bar.update(my_time[0], my_time[1])

            elif media.client.status()['state'] == "stop":
                media.client.close()
                break

            time.sleep(0.9)

class WinBar:  #  progress bar window
    def __init__(self):
        self.begin_x = 2 
        self.begin_y = (curses.LINES - 4)
        self.height = 3
        self.width = (curses.COLS - 4)
        self.win = curses.newwin(self.height, self.width, self.begin_y, self.begin_x)
        self.win.border(0)

    def create(self):
        self.win.refresh()

    def update(self, position, total):
        try:
            rangex = ((int(self.width - 20 ) * (int(position) + 1)) / int(total))
        except:
            rangex = 1
        pos = int(rangex) + 9
        for pp in range(9,pos):
            self.win.addstr(1, pp, "=")
        self.win.addstr(1, 1, str(datetime.timedelta(seconds=int(position))))
        self.win.addstr(1, (self.width -9 ), str(datetime.timedelta(seconds=int(total))))
        self.win.addstr(1, pos, ">")
        self.win.refresh()

def main(stdscr):
    global bar
    bar = WinBar()
    bar.create()
    info = WinMain()
    info.create()
    info.loop()

def start_gui(host):
    global media, item
    media = Media(host)
    item = Item(media.client.currentsong()['file'])
    wrapper(main)
