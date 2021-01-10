# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:33:40 2021

@author: Henry
"""
from database import database
import pandas as pd

if __name__ == "__main__":
    db = database()
    ingame_data = db.select("player_ingame_stats")
    df_ingame = pd.DataFrame(ingame_data)
    
    print(df_ingame.isnull().sum())
    # Some players have missing *_pct because they have never taken those type of shot
    # Treat missing *_pct as 0 percent
    pct_columns = ['fg_pct', 'fg3_pct', 'fg2_pct', 'efg_pct', 'ft_pct']
    for col in pct_columns:
        df_ingame.loc[df_ingame[col].isnull(), col] = "0"
    
    # Some rows is the combination stats of players that have played in multiple teams
    # Remove the combination rows
    drop_indices = df_ingame.loc[df_ingame['team_id'] == "TOT"].index
    df_ingame.drop(drop_indices, inplace=True)
    
    # Convert data type from decimal to float
    # Only intended to help with better reading data in spyder
    # df_ingame.iloc[:, 8:] = df_ingame.iloc[:, 8:].astype(float)
    
    # Saving Cleaned data to database
    table = f"player_ingame_stats_cleaned"
    db.insert_df(table, df_ingame)
    
    db.close()