# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 19:38:28 2021

@author: Henry
"""

import requests
from bs4 import BeautifulSoup

def gather_data_by_year(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")
    players = soup.find_all("tr", {"class": "full_table"})
    for player in players:
        temp = dict()
        stats = player.find_all("td")
        for stat in stats:
            temp[stat["data-stat"]] = stat.text
        rank = player.find("th").text
        temp['rank'] = rank
        # Add to database
        all_players[rank] = temp

if __name__ == "__main__":
    years = [2021, 2020, 2019]
    all_players = dict()
    # for year in years:
    #     gather_data_by_year(year)
    url = f"https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")
    players = soup.find_all("tr", {"class": "full_table"})
    for player in players:
        temp = dict()
        stats = player.find_all("td")
        for stat in stats:
            temp[stat["data-stat"]] = stat.text if not stat.text == "" else None
        rank = player.find("th").text
        temp['rank'] = rank
        all_players[rank] = temp
