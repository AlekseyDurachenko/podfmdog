#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2015, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from podfmdog_downloader import *


def init(db):
    db.create_tables()
    sys.exit(0)


def get_prop_download_directory(db):
    print("property[download_directory] = %s" %
          (db.get_property("download_directory",)))
    sys.exit(0)


def set_prop_download_directory(db, download_directory):
    db.set_property("download_directory", download_directory)
    sys.exit(0)


def channel_list(db):
    dl_dir = db.get_property("download_directory",)
    for channel in db.get_channels():
        print("* %s (%s) -> %s" % (channel['link'],
                                   channel['subdir'],
                                   os.path.join(dl_dir, channel['subdir'])))
    sys.exit(0)


def channel_add(db, link, subdir):
    if not db.add_channel(link, subdir):
        print("the channel is already exists")
    sys.exit(0)


def channel_edit(db, link, subdir):
    if not db.edit_channel(link, subdir):
        print("the channel is not exists")
    sys.exit(0)


def channel_remove(db, link):
    db.remove_channel(link)
    sys.exit(0)


def print_usage():
    print("""=== podfmdog conOAtrol v.0.1.0 ===
Usage:
    podfmdog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                            -- init the database
    set download_directory <path>   -- set the download directory
    get download_directory          -- show the download directory
    channel add <rss_url> <subdir>  -- add the podcast
    channel edit <rss_url> <subdir> -- change the podcast directory
    channel remove <rss_url>        -- remove the podcast
    channel list                    -- show the podcast list
""")
    sys.exit(-1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        podfmDb = PodfmPodcastDb()

        # init
        if sys.argv[1] == "init":
            init(podfmDb)
        # get <property>
        elif sys.argv[1] == "get" and len(sys.argv) > 2:
            # get download_directory
            if sys.argv[2] == "download_directory":
                get_prop_download_directory(podfmDb)
        # set <property>
        elif sys.argv[1] == "set" and len(sys.argv) > 2:
            # set download_directory
            if sys.argv[2] == "download_directory" and len(sys.argv) == 4:
                set_prop_download_directory(podfmDb, sys.argv[3])
        # podcast <command>
        elif sys.argv[1] == "channel" and len(sys.argv) > 2:
            # podcast add <rss_url> <subdir>
            if sys.argv[2] == "add" and len(sys.argv) == 5:
                channel_add(podfmDb, sys.argv[3], sys.argv[4])
            # podcast edit <rss_url> <subdir>
            if sys.argv[2] == "edit" and len(sys.argv) == 5:
                channel_edit(podfmDb, sys.argv[3], sys.argv[4])
            # podcast remove <rss_url>
            elif sys.argv[2] == "remove" and len(sys.argv) == 4:
                channel_remove(podfmDb, sys.argv[3])
            # podcast list
            elif sys.argv[2] == "list":
                channel_list(podfmDb)
    # invalid
    print_usage()
