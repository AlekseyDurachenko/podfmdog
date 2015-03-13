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
import feedparser
import urllib.parse
import urllib.request
import shutil
import sys
import notify2
from podfmdog_db import *


class PodfmPodcastDownloader:
    __db = None

    def __init__(self, db):
        notify2.init("podfmdog")
        self.__db = db

    def download_directory(self):
        return self.__db.get_property("download_directory")

    def parse_url(self, url):
        return urllib.parse.urlparse(url).path.split('/')[-1]

    def parse_rss(self, podcast_rss):
        try:
            d = feedparser.parse(podcast_rss)
            return [{"media_url": link.href, "podcast_url": entry.link,
                     "rss_entry": entry}
                    for entry in d.entries
                    for link in entry.links
                    if link.type == "audio/mpeg"]
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            return None

    def dst_filename(self, url, subdir):
        return os.path.join(
            self.download_directory(), subdir, self.parse_url(url))

    def download_url(self, url, dst_filename):
        dir = os.path.dirname(dst_filename)
        if not os.path.exists(dir):
            os.makedirs(dir)

        try:
            print("Download url: %s" % (url,))
            tmp_filename, h = urllib.request.urlretrieve(url)
            print("Download complete! Temporary filename: %s" % (tmp_filename,))
            shutil.move(tmp_filename, dst_filename)
            print("Moving complete! Permanent filename: %s" % (dst_filename,))
            return True
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            return False

    def create_description(self, rss_entry):
        desc = "<br>"
        for desc_variant in rss_entry["content"]:
            if desc_variant["type"] == "text/plain":
                desc += desc_variant["value"].strip()
        return "<center><b>%s: %s</b></center>%s" % \
               (rss_entry["author"].strip(),
                rss_entry["title"].strip(), desc)

    def download_podcast(self, link, subdir):
        podcasts = self.parse_rss(link)
        if podcasts is None:
            print("Can't parse the rss feed: %s" %(link,))
            return None
        exists_podcasts = set(self.__db.get_podcasts(link))

        for podcast in podcasts:
            if podcast["podcast_url"] not in exists_podcasts:
                if self.download_url(
                        podcast["media_url"],
                        self.dst_filename(podcast["media_url"], subdir)):
                    self.__db.add_podcast(link, podcast["podcast_url"])
                    rss_entry = podcast["rss_entry"]
                    notify = notify2.Notification(
                        "New podcast is available",
                        self.create_description(rss_entry))
                    notify.show()

    def download_channels(self):
        for channel in self.__db.get_channels():
            if channel["active"]:
                self.download_podcast(channel["link"], channel["subdir"])
