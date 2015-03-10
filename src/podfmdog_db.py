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
import sqlite3
import os


class PodfmPodcastDb:
    """This class used for access the database. The database structure:

--------------------------------------------------------------|
| TProperty (the property table)                              |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| name      | string   | unique         | property name       |
| value     | string   |                | property value      |
--------------------------------------------------------------|

--------------------------------------------------------------|
| TChannel (the podfm channel)                                |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| link      | string   | unique         | link to channel rss |
| subdir    | string   |                | subdir for files    |
| active    | integer  |                | 0 - inactive        |
| comment   | string   |                | description         |
--------------------------------------------------------------|

--------------------------------------------------------------|
| TPodcast (the downloaded podcast)                           |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| TChannelId| integer  | unique         |                     |
| link      | integer  | unique         | link to podcast     |
--------------------------------------------------------------|
    """
    __conn = None

    def __init__(self):
        path = os.path.expanduser("~")          \
                + os.path.sep + ".config"       \
                + os.path.sep + "podfmdog"
        if not os.path.exists(path):
            os.makedirs(path)
        self.__conn = sqlite3.connect(os.path.join(path, 'podfmdog.db'))
        self.__conn.text_factory = str

    def create_tables(self):
        cursor = self.__conn.cursor();
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TProperty(
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL);""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TChannel(
                id INTEGER PRIMARY KEY NOT NULL,
                link TEXT NOT NULL,
                subdir TEXT NOT NULL,
                active INTEGER NOT NULL,
                comment TEXT NOT NULL,
                UNIQUE(link));""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TPodcast(
                id INTEGER PRIMARY KEY NOT NULL,
                TChannelId INTEGER NOT NULL,
                link TEXT NOT NULL,
                UNIQUE(TChannelId, link));""")
        self.__conn.commit()

    def set_property(self, name, value):
        cursor = self.__conn.cursor()
        try:
            cursor.execute("INSERT INTO TProperty(name, value) VALUES(?, ?)",
                           (name, value))
        except sqlite3.IntegrityError:
            cursor.execute("UPDATE TProperty SET value = ? WHERE name = ?",
                           (value, name))
        self.__conn.commit()

    def get_property(self, name):
        cursor = self.__conn.cursor()
        for row in cursor.execute(
                "SELECT value FROM TProperty WHERE name = ?", (name,)):
            return row[0]
        return None

    def add_channel(self, link, subdir, comment=""):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(
                "INSERT INTO TChannel(link, subdir, active, comment) "
                "VALUES(?, ?, ?, ?)", (link, subdir, 1, comment))
            self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def edit_channel(self, link, subdir, comment=""):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(
                "UPDATE TChannel SET subdir = ? "
                "WHERE link = ?", (subdir, link))
            self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def remove_channel(self, link):
        cursor = self.__conn.cursor()
        cursor.execute("DELETE FROM TChannel WHERE link = ?", (link,))
        self.__conn.commit()

    def add_podcast(self, channel_link, podcast_link):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO TPodcast(TChannelId, link) "
                           "VALUES((SELECT id FROM TChannel WHERE link = ?),"
                           "?)", (channel_link, podcast_link))
            self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def remove_podcast(self, channel_link, podcast_link):
        cursor = self.__conn.cursor()
        cursor.execute("DELETE FROM TPodcast WHERE "
                       "TChannelId = (SELECT id FROM TChannel WHERE link = ?) "
                       "AND link = ?", (channel_link, podcast_link))
        self.__conn.commit()

    def get_podcasts(self, channel_link):
        cursor = self.__conn.cursor()
        return [row[0] for row in cursor.execute(
                "SELECT link FROM TPodcast WHERE TChannelId = "
                "(SELECT id FROM TChannel WHERE link = ?)", (channel_link,))]

    def get_channels(self):
        cursor = self.__conn.cursor()
        return [{"link": row[0], "subdir": row[1], "active": row[2]}
                for row in cursor.execute("SELECT link, subdir, active "
                                          "FROM TChannel")]
