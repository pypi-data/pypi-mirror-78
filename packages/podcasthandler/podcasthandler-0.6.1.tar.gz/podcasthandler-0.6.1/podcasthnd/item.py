#!/usr/bin/env python3

# PODCAST HANDLER by Claudio Barca (Copyright 2020 Claudio Barca)
# This software is distributed under GPL v. 3 license.
# See LICENSE file for details.

import os
import hashlib
import podcasthnd.constants as constants

class Item:
    def __init__(self,url):
        self.url = url
        self.hash = self.get_hash_string()
        self.cache_file = constants.podcast_cache_dir + self.hash    # save the position of a podcast
        self.current_file = constants.current_file

    def db_get_position(self):
        try:
            file = open(self.cache_file,'r') 
            position = int(file.readlines()[0])
            return position
        except:
            return 0

    def db_set_position(self,position):
        file = open(self.cache_file,'w') 
        file.write(position)
        file.close() 

    def db_set_current(self):   # save the current podcast url
        file = open(self.current_file,'w') 
        file.write(self.url)
        file.close() 

    def db_delete_cache_file(self):
        try:
            os.remove(self.cache_file)
        except:
            print('No cache file')

    # the cache filename is a sha256 hash of the url text
    def get_hash_string(self):
        hash = hashlib.sha256(self.url.encode('utf-8')).hexdigest()
        return hash


