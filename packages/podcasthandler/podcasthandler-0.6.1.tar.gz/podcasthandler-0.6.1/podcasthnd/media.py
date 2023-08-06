#!/usr/bin/env python3

# PODCAST HANDLER by Claudio Barca (Copyright 2020 Claudio Barca)
# This software is distributed under GPL v. 3 license.
# See LICENSE file for details.

# class to handle mpd

from mpd import MPDClient

class Media:
    def __init__(self, host):
        from mpd import MPDClient
        self.client = MPDClient()  
        self.host = host
        self.client.connect(self.host, 6600)  
        self.notseekable_flag = False

    def play(self,url):         # set and play url
        self.url = url
        self.client.clear()
        self.client.repeat(0)
        self.client.random(0)
        self.client.add(url)
        self.client.play()

    def play_at_position(self,url,position):  # start playing an url at position
        self.play(url)
        self.seek(position)

    def toggle(self):           # toggle pause
        self.client.pause()

    def seek(self,position):    # seek for a position
        try:
            self.client.seekcur(position)
            self.notseekable_flag = False
        except:
            self.notseekable_flag = True

    def time(self):             # return a list [ current seconds, total seconds ]
        return self.client.status()['time'].split(':')

    def close(self):            # stop playing and close mpd connection
        self.client.stop()
        self.client.close()
