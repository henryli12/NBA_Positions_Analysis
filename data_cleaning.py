# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:33:40 2021

@author: Henry
"""
from database import database
import pandas as pd

def find_weight(row, df_physical):
    # For special case where NBA shorten the names
    if row["player"] == 'Wesley Iwundu':
        return "195 lbs"
    elif row["player"] == 'Sviatoslav Mykhailiuk':
        return "205 lbs"
    names = row["player"].split(" ")
    names = names if len(names) < 3 else names[:2]
    reg = ""
    for name in names:
        name = name.replace(".", "")
        reg += f"{name}.*"
    result = df_physical.loc[df_physical["player"].str.contains(reg, regex=True), ["weight"]]
    if not result.empty:
        return result.iloc[0, 0]
    else:
        return "Missing"

def find_height(row, df_physical):
    # For special case where NBA shorten the names
    if row["player"] == 'Wesley Iwundu':
        return "6-6"
    elif row["player"] == 'Sviatoslav Mykhailiuk':
        return "6-7"
    names = row["player"].split(" ")
    names = names if len(names) < 3 else names[:2]
    reg = ""
    for name in names:
        name = name.replace(".", "")
        reg += f"{name}.*"
    result = df_physical.loc[df_physical["player"].str.contains(reg, regex=True), ["height"]]
    if not result.empty:
        return result.iloc[0, 0]
    else:
        return "Missing"

if __name__ == "__main__":
    db = database()
    try:
        ingame_data = db.select("player_ingame_stats")
        df_ingame = pd.DataFrame(ingame_data)
        physical_data = db.select("player_physical_stats")
        df_physical = pd.DataFrame(physical_data)
        
        print(df_ingame.isnull().sum())
        # Some players have missing *_pct because they have never taken those type of shot
        # Treat missing *_pct as 0 percent
        pct_columns = ['fg_pct', 'fg3_pct', 'fg2_pct', 'efg_pct', 'ft_pct']
        for col in pct_columns:
            df_ingame.loc[df_ingame[col].isnull(), col] = 0.0
        
        # Some rows is the combination stats of players that have played in multiple teams
        # Remove the combination rows
        drop_indices = df_ingame.loc[df_ingame['team_id'] == "TOT"].index
        df_ingame.drop(drop_indices, inplace=True)
        
        # Combine ingame data and physical data
        df_combined = pd.merge(left=df_ingame, right=df_physical[['player', 'weight', 'height']], how='left', left_on='player', right_on='player')
        
        print(df_combined.isnull().sum() / len(df_combined))
        
        # Some player have names formatted differently in both sources
        df_combined.loc[df_combined["weight"].isnull(), ["weight"]] = df_combined[df_combined["weight"].isnull()].apply(lambda row: find_weight(row, df_physical), axis=1)
        df_combined.loc[df_combined["height"].isnull(), ["height"]] = df_combined[df_combined["height"].isnull()].apply(lambda row: find_height(row, df_physical), axis=1)

        # Saving Cleaned data to database
        table = "player_all_stats_cleaned"
        db.insert_df(table, df_combined)
        # df_combined.to_csv("testing.csv")

    except Exception as err:
        print(err)
    db.close()
