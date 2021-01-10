# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 20:41:41 2021

@author: Henry
"""

import pymysql
from sqlalchemy import create_engine
import os

class database:
    def __init__(self):
        user = os.environ.get('MYSQL_USER')
        database = os.environ.get('DATABASE')
        password = os.environ.get('MYSQL_PASSWORD')
        self.db = pymysql.connect(user=user, password=password,
                              host='localhost',
                              db=database)
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def create_stats_table(self, table):
        sql = (
        f"CREATE TABLE `{table}` ("
        "`id` INT AUTO_INCREMENT PRIMARY KEY,"
        "`rank` INT,"
        "`player` VARCHAR(255),"
        "`year` INT,"
        "`pos` VARCHAR(10),"
        "`age` INT,"
        "`team_id` VARCHAR(10),"
        "`g` INT,"
        "`gs` INT,"
        "`mp_per_g` DECIMAL(3,1),"
        "`fg_per_g` DECIMAL(3,1),"
        "`fga_per_g` DECIMAL(3,1),"
        "`fg_pct` DECIMAL(4,3),"
        "`fg3_per_g` DECIMAL(3,1),"
        "`fg3a_per_g` DECIMAL(3,1),"
        "`fg3_pct` DECIMAL(4,3),"
        "`fg2_per_g` DECIMAL(3,1),"
        "`fg2a_per_g` DECIMAL(3,1),"
        "`fg2_pct` DECIMAL(4,3),"
        "`efg_pct` DECIMAL(4,3),"
        "`ft_per_g` DECIMAL(3,1),"
        "`fta_per_g` DECIMAL(3,1),"
        "`ft_pct` DECIMAL(4,3),"
        "`orb_per_g` DECIMAL(3,1),"
        "`drb_per_g` DECIMAL(3,1),"
        "`trb_per_g` DECIMAL(3,1),"
        "`ast_per_g` DECIMAL(3,1),"
        "`stl_per_g` DECIMAL(3,1),"
        "`blk_per_g` DECIMAL(3,1),"
        "`tov_per_g` DECIMAL(3,1),"
        "`pf_per_g` DECIMAL(3,1),"
        "`pts_per_g` DECIMAL(3,1)"
        ") ENGINE=InnoDB")
        self.cursor.execute(sql)
    
    def create_physical_table(self, table):
        sql = (
        f"CREATE TABLE `{table}` ("
        "`id` INT AUTO_INCREMENT PRIMARY KEY,"
        "`player` VARCHAR(255),"
        "`team` VARCHAR(10),"
        "`position` VARCHAR(10),"
        "`weight` VARCHAR(20),"
        "`height` VARCHAR(20)"
        ") ENGINE=InnoDB")
        self.cursor.execute(sql)
    
    def drop_table(self, table):
        sql = f"DROP TABLE `{table}`"
        self.cursor.execute(sql)
    
    def insert_stat(self, table, stats):
        sql = (f"INSERT INTO `{table}` "
               "(`rank`, `player`, `year`, `pos`, `age`, `team_id`, `g`, `gs`, `mp_per_g`, `fg_per_g`, `fga_per_g`,"
               " `fg_pct`, `fg3_per_g`, `fg3a_per_g`, `fg3_pct`, `fg2_per_g`, `fg2a_per_g`, `fg2_pct`,"
               " `efg_pct`, `ft_per_g`, `fta_per_g`, `ft_pct`, `orb_per_g`, `drb_per_g`, `trb_per_g`,"
               " `ast_per_g`, `stl_per_g`, `blk_per_g`, `tov_per_g`, `pf_per_g`, `pts_per_g`) "
               "VALUES (%(rank)s, %(player)s, %(year)s, %(pos)s, %(age)s, %(team_id)s, %(g)s,"
               " %(gs)s, %(mp_per_g)s, %(fg_per_g)s, %(fga_per_g)s, %(fg_pct)s, %(fg3_per_g)s,"
               " %(fg3a_per_g)s, %(fg3_pct)s, %(fg2_per_g)s, %(fg2a_per_g)s, %(fg2_pct)s,"
               " %(efg_pct)s, %(ft_per_g)s, %(fta_per_g)s, %(ft_pct)s, %(orb_per_g)s,"
               " %(drb_per_g)s, %(trb_per_g)s, %(ast_per_g)s, %(stl_per_g)s, %(blk_per_g)s,"
               " %(tov_per_g)s, %(pf_per_g)s, %(pts_per_g)s)")        
        self.cursor.executemany(sql, stats)

    def insert_physical(self, table, stats):
        sql = (f"INSERT INTO `{table}` "
               "(`player`, `team`, `position`, `height`, `weight`) "
               "VALUES (%(player)s, %(team)s, %(position)s, %(height)s, %(weight)s)")
        self.cursor.executemany(sql, stats)

    def insert_df(self, table, df):
        user = os.environ.get('MYSQL_USER')
        db = os.environ.get('DATABASE')
        pw = os.environ.get('MYSQL_PASSWORD')
        engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")
        df.to_sql(con=engine, name=table, if_exists='replace')
        engine.dispose()
    
    def delete_by_id(self, table, id):
        sql = ("DELETE "
               f"FROM `{table}`"
               f"WHERE id = {id}")
        self.cursor.execute(sql)

    def select(self, table, *args):
        to_select = "*" if len(args) == 0 else ", ".join(args)
        sql = f"SELECT {to_select} FROM {table}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit (self):
        self.db.commit()
        
    def close(self):
        self.cursor.close()
        self.db.close()

if __name__ == "__main__":
    db = database()
    db.create_physical_table("testing")
    db.close()