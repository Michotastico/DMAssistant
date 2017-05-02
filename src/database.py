#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

from src.utilities import valid_roll, roll_to_val

__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Database:
    def __init__(self, db_name):
        self.db = db_name
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        sql = 'create table if not exists Shortcuts (shortcut text, roll text, PRIMARY KEY (shortcut))'
        c.execute(sql)
        conn.commit()

        c.close()
        conn.close()

    def add_shortcut(self, shortcut, roll):
        if valid_roll(roll):
            try:
                conn = sqlite3.connect(self.db)
                conn.execute("INSERT INTO Shortcuts(shortcut, roll) values (?, ?)", (shortcut, roll))
                conn.commit()
                conn.close()
                return True
            except sqlite3.Error:
                return False
        return False

    def remove_shortcut(self, shortcut):
        try:
            conn = sqlite3.connect(self.db)
            conn.execute("DELETE FROM Shortcuts WHERE shortcut=?", [shortcut])
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def apply_shortcut(self, shortcut):
        try:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute("SELECT roll from Shortcuts WHERE shortcut=?", [shortcut])
            value = cur.fetchone()[0]
            cur.close()
            conn.close()
            return roll_to_val(value)
        except TypeError:
            return None

    def get_shortcuts(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('select shortcut, roll from Shortcuts')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

