# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 20:41:41 2021

@author: Henry
"""

import mysql.connector as sql_db
import os

class database:
    def __init__(self):
        user = os.environ.get('MYSQL_USER')
        database = os.environ.get('DATABASE')
        password = os.environ.get('MYSQL_PASSWORD')
        self.db = sql_db.connect(user=user, password=password,
                              host='127.0.0.1',
                              database=database,
                              auth_plugin='mysql_native_password')
        self.cursor = self.db.cursor()
        self.cursor.execute("SHOW DATABASES")
        for x in self.cursor:
            print(x)
    
    def close(self):
        self.db.close()

if __name__ == "__main__":
    db = database()
    db.close()