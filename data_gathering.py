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
from selenium import webdriver
import unidecode
import time

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
    print(year)
    table = f"player_ingame_stats"
    try:
        db.create_stats_table(table)
    except:
        pass
    all_stats = []
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")
    players = soup.find_all("tr", {"class": "full_table"})
    for player in players:
        player_stat = dict()
        rank = player.find("th").text
        player_stat['rank'] = rank
        player_stat['year'] = year
        stats = player.find_all("td")
        for stat in stats:
            player_stat[stat["data-stat"]] = stat.text if not stat.text=="" else None
        name = player_stat["player"]
        name = unidecode.unidecode(name)
        player_stat["player"] = name
        all_stats.append(player_stat)
    # Commit to database
    db.insert_stat(table, all_stats)
    db.commit()
    print(f"{year} data inserted")
    
    # Saves data to csv
    # export_to_csv(all_stats, table)

def get_player_weight_height(db):
    table = "player_physical_stats"
    try:
        db.create_physical_table(table)
    except:
        pass
    DRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://www.nba.com/players')
    show_historic = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[3]/section/div/div[2]/div[1]/div[6]/label/div/span')
    all_selection = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[3]/section/div/div[2]/div[1]/div[7]/div/div[3]/div/label/div/select/option[1]')
    show_historic.click()
    time.sleep(2)
    all_selection.click()
    trs = driver.find_elements_by_tag_name('tr')
    counter = 1
    bunch = []
    for tr in trs[1:]:
        player = dict()
        tds = tr.find_elements_by_tag_name('td')
        name = tds[0].text.replace('\n', ' ').replace('\r', '')
        player["player"] = name
        player["team"] = tds[1].text
        player["position"] = tds[3].text
        player["height"] = tds[4].text
        player["weight"] = tds[5].text
        bunch.append(player)
        if counter%100 == 0:
            db.insert_physical(table, bunch)
            db.commit()
            bunch = []
            print(f"{counter} rows inserted")
        counter += 1
    if not len(bunch) == 0:
        db.insert_physical(table, bunch)
        db.commit()
        print(f"{counter} rows inserted")
    # driver.quit()

if __name__ == "__main__":        
    years = [2021, 2020, 2019, 2018, 2017]
    db = database()
    try:
        # Get player physical data from https://www.nba.com/players
        # Takes up to 30-60 mins to insert all 4589 rows into database
        get_player_weight_height(db)
        
        # Get per game data from https://www.basketball-reference.com/leagues/NBA_2021_per_game.html
        for year in years:
            gather_data_by_year(year, db)
    except Exception as err:
        print(err)
    db.close()

