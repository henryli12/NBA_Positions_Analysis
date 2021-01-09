# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:33:40 2021

@author: Henry
"""
from database import database
import pandas as pd

if __name__ == "__main__":
    years = [2021, 2020, 2019]
    dfs = dict()
    db = database()
    for year in years:
        data = db.select(f"players_stats_{year}")
        dfs[year] = pd.DataFrame(data)
    
    print(dfs[2021].isnull().sum())
    # Some players have missing *_pct because they have never taken those type of shot
    # Treat missing *_pct as 0 percent
    pct_columns = ['fg_pct', 'fg3_pct', 'fg2_pct', 'efg_pct', 'ft_pct']
    for year in years:
        temp_df = dfs[year]
        for col in pct_columns:
            temp_df.loc[temp_df[col].isnull(), col] = 0
    
    # Some rows is the combination stats of players that have played in multiple teams
    # Remove the combination rows
    for year in years:
        temp_df = dfs[year]
        drop_indices = temp_df.loc[temp_df['team_id'] == "TOT"].index
        temp_df.drop(drop_indices, inplace=True)
    
    # Convert data type from decimal to float
    # Only intended to help with better reading data in spyder
    for year in years:
        temp_df = dfs[year]
        temp_df.iloc[:, 8:] = temp_df.iloc[:, 8:].astype(float)
    
    # Saving Cleaned data to database
    for year in years:
        temp_df = dfs[year]
        table = f"player_stats_{year}_cleaned"
        db.insert_df(table, temp_df)
    
    db.close()