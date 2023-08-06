#!/usr/bin/env python3

# PODCAST HANDLER by Claudio Barca (Copyright 2020 Claudio Barca)
# This software is distributed under GPL v. 3 license.
# See LICENSE file for details.

import os

# constants

version = "0.6.1"

podcast_cache_dir = ("%s/.cache/podcasthander/" % os.environ['HOME'])
daemon_data_file  = podcast_cache_dir + "daemon_data"
current_file = podcast_cache_dir + "current"
daemon_filename   = "podcasthandlerd"
default_host      = "localhost"

update_time = 10                # seconds between update 
end_time = 15                   # seconds before the end of file to stop updating and delete item
