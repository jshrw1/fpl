# packages from third party
import os
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import re

path = "data\\raw\\"
years = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]


'''Happy This Work'''
def clean_fpl(PATH, YEARS):

    data = pd.DataFrame()

    for year in YEARS:
        # Load in player data for each year
        raw = pd.read_csv(f"{PATH}{year}\\players_raw.csv")
        raw["element_type_name"] = raw["element_type"].map({1: "GK", 2: "DEF", 3: "MID", 4: "FWD"})
        raw["full_name"] = raw.first_name + " " + raw.second_name

        # Clean player data for imputation and optimisations
        players = pd.DataFrame()
        items = [
            "full_name",
            "first_name",
            "second_name",
            "element_type",
            "element_type_name",
            "id",
            "team",
            "team_code",
            "web_name",
            "saves",
            "penalties_saved",
            "clean_sheets",
            "goals_conceded",
            "bonus",
            "bps",
            "creativity",
            "ep_next",
            "influence",
            "threat",
            "goals_scored",
            "assists",
            "minutes",
            "own_goals",
            "yellow_cards",
            "red_cards",
            "penalties_missed",
            "selected_by_percent",
            "now_cost",
            "points_per_game",
            "total_points",
        ]
        players = raw.loc[:, items]
        players["season"] = year
        players['cost_bin'] = players.now_cost.apply(lambda x: np.floor(x/10))
        data = pd.concat([data, players], ignore_index=True)

    return data


'''Needs some work'''
''' Currently comparing 2023 - 24  to infer. Could porbably average andd weight over seasons'''
def make_available_players_df(THIS_SEASON, LAST_SEASON):
    LAST_SEASON = LAST_SEASON[LAST_SEASON.minutes > 0]
    LAST_SEASON = LAST_SEASON[['full_name', "total_points"]]
    LAST_SEASON.rename(columns={'total_points': "total_points_last_season"},inplace=True)
    AVAILABLE = pd.merge(THIS_SEASON, LAST_SEASON, on='full_name', how='left')

    return AVAILABLE


'''Happy This Work'''
def histogram_plots(df):
    fig = plt.figure(figsize=(16, 9))

    # Create subplots
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, sharex=ax1, sharey=ax1)
    ax3 = fig.add_subplot(2, 2, 3, sharex=ax1, sharey=ax1)
    ax4 = fig.add_subplot(2, 2, 4, sharex=ax1, sharey=ax1)
    # Plotting each subplot
    for ax, position, label in zip([ax1, ax2, ax3, ax4], ['FWD', 'MID', 'DEF', 'GK'], ['FWD', 'MID', 'DEF', 'GK']):
        data = players_24_25[players_24_25.element_type_name == position].total_points
        sns.histplot(data, kde=True, ax=ax, label=label, stat="density", kde_kws={"cut": 3})
        ax.axvline(np.mean(data), color='red', label='mean')
        ax.axvline(np.median(data), color='orange', label='median')
        ax.set_title(label)
        ax.legend()

    plt.tight_layout()
    plt.show()


clean_data = clean_fpl(path, years)

last_season = clean_data[clean_data['season'] == "2023-24"]
this_season = clean_data[clean_data['season'] == "2024-25"]
players_24_25 = make_available_players_df(this_season, last_season)
histogram_plots(players_24_25)


'''print("\n".join(f"- {col}" for col in players.columns))
#AVAILABLE['total_points_last_season'] = AVAILABLE['total_points_last_season'].fillna(AVAILABLE['total_points'])'''


'''



def imputation(DF)


impute_cols = ['saves','penalties_saved', 'clean_sheets', 'goals_conceded', 'bonus', 'bps',
               'creativity', 'influence', 'threat', 'goals_scored','assists', 'minutes', 'own_goals',
               'yellow_cards', 'red_cards','penalties_missed','points_per_game', 'total_points']
positions = set(pdata.element_type_name)
costs = set(pdata.now_cost)
medians = {}; stds = {}

for i in positions:
    medians['{}'.format(i)] = {}
    stds['{}'.format(i)] = {}
    for c in costs:
        medians['{}'.format(i)]['{}'.format(c)] = {}
        stds['{}'.format(i)]['{}'.format(c)] = {}
        for j in impute_cols:
            if pdata[(pdata.total_points!=0)&(pdata.minutes!=0)&(pdata.element_type_name==str(i))&(pdata.now_cost==c)].shape[0] > 0:
                median = np.median(pdata[(pdata.total_points!=0)&(pdata.minutes!=0)&(pdata.element_type_name==i)&(pdata.now_cost==c)][j].astype(np.float32))
                std = np.std(pdata[(pdata.total_points!=0)&(pdata.minutes!=0)&(pdata.element_type_name==i)&(pdata.now_cost==c)][j].astype(np.float32))
                medians['{}'.format(i)]['{}'.format(c)]['{}'.format(j)] = median
                stds['{}'.format(i)]['{}'.format(c)]['{}'.format(j)] = std
            else:
                medians['{}'.format(i)]['{}'.format(c)]['{}'.format(j)] = 0
                stds['{}'.format(i)]['{}'.format(c)]['{}'.format(j)] = 0

for idx, row in pdata[(pdata.total_points==0)&(pdata.minutes==0)].iterrows():
    for col in impute_cols:
        pdata.loc[idx,col] = medians[str(row['element_type_name'])][str(row['now_cost'])][str(col)] 
                            + np.abs((np.random.randn()/1.5)*stds[str(row['element_type_name'])][str(row['now_cost'])][str(col)])

'''