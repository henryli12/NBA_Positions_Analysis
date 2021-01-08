# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 19:38:28 2021

@author: Henry
"""

import requests
from bs4 import BeautifulSoup
from database import database
import csv
import os

def export_to_csv(data, filename):
    if not os.path.exists('data'):
        os.makedirs('data')
    csv_file = f"data/{filename}.csv"
    try:
        csv_columns = data[0].keys()
        with open(csv_file, 'w', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, lineterminator = '\n')
            writer.writeheader()
            for player in data:
                writer.writerow(player)
    except IOError:
        print("I/O error")

def gather_data_by_year(year, db):
    table = f"players_stats_{year}"
    try:
        db.create_table(table)
    except:
        add = input(f"{table} table already exist. Do you want to append to this table?[y/n]\n")
        if not add.lower() == 'y':
            return
    all_stats = []
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    print(f"Scraping data for {year}...")
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")
    players = soup.find_all("tr", {"class": "full_table"})
    for player in players:
        player_stat = dict()
        rank = player.find("th").text
        player_stat['rank'] = rank
        stats = player.find_all("td")
        for stat in stats:
            player_stat[stat["data-stat"]] = stat.text if not stat.text=="" else None
        db.insert(table, player_stat)
        all_stats.append(player_stat)
    # Commit to database
    db.commit()
    # Saves data to csv
    export_to_csv(all_stats, table)
    
if __name__ == "__main__":
    years = [2021, 2020, 2019]
    db = database()
    for year in years:
        gather_data_by_year(year, db)
    db.close()
    
