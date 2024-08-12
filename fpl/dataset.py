# packages from third party
import os
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import re


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
        players["cost_bin"] = players.now_cost.apply(lambda x: np.floor(x / 10))
        data = pd.concat([data, players], ignore_index=True)

    return data


def make_available_players_df(THIS_SEASON, LAST_SEASON):
    LAT_SEASON = LAST_SEASON[LAST_SEASON.minutes > 0]
    LAST_SEASON = LAST_SEASON[["full_name", "total_points"]]
    LAST_SEASON.rename(columns={"total_points": "total_points_last_season"}, inplace=True)

    AVAILABLE = pd.merge(THIS_SEASON, LAST_SEASON, on="full_name", how="left")

    condition = (AVAILABLE["total_points"] > 0) & (AVAILABLE["total_points_last_season"].isna())
    AVAILABLE.loc[condition, "total_points_last_season"] = AVAILABLE.loc[condition, "total_points"]

    AVAILABLE["total_points_last_season"] = AVAILABLE["total_points_last_season"].fillna(0)

    return AVAILABLE


def histogram_plots(df):
    fig = plt.figure(figsize=(16, 9))

    # Create subplots
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, sharex=ax1, sharey=ax1)
    ax3 = fig.add_subplot(2, 2, 3, sharex=ax1, sharey=ax1)
    ax4 = fig.add_subplot(2, 2, 4, sharex=ax1, sharey=ax1)
    # Plotting each subplot
    for ax, position, label in zip(
        [ax1, ax2, ax3, ax4], ["FWD", "MID", "DEF", "GK"], ["FWD", "MID", "DEF", "GK"]
    ):
        data = players_24_25[players_24_25.element_type_name == position].total_points
        sns.histplot(data, kde=True, ax=ax, label=label, stat="density", kde_kws={"cut": 3})
        ax.axvline(np.mean(data), color="red", label="mean")
        ax.axvline(np.median(data), color="orange", label="median")
        ax.set_title(label)
        ax.legend()

    plt.tight_layout()
    plt.show()


def impute_missing_values(players_df, impute_cols):

    positions = set(players_df.element_type_name)
    costs = set(players_df.now_cost)

    medians = {}
    stds = {}

    # Calculate medians and standard deviations
    for position in positions:
        medians[str(position)] = {}
        stds[str(position)] = {}

        for cost in costs:
            medians[str(position)][str(cost)] = {}
            stds[str(position)][str(cost)] = {}

            for col in impute_cols:
                filtered_df = players_df[
                    (players_df.total_points != 0)
                    & (players_df.minutes != 0)
                    & (players_df.element_type_name == position)
                    & (players_df.now_cost == cost)
                ]

                if filtered_df.shape[0] > 0:
                    median = np.median(filtered_df[col].astype(np.float32))
                    std = np.std(filtered_df[col].astype(np.float32))
                else:
                    median = 0
                    std = 0

                medians[str(position)][str(cost)][str(col)] = median
                stds[str(position)][str(cost)][str(col)] = std

    # Impute missing values
    for idx, row in players_df[
        (players_df.total_points == 0) & (players_df.minutes == 0)
    ].iterrows():
        for col in impute_cols:
            median_value = medians[str(row["element_type_name"])][str(row["now_cost"])][str(col)]
            std_value = stds[str(row["element_type_name"])][str(row["now_cost"])][str(col)]
            players_df.loc[idx, col] = median_value + np.abs((np.random.randn() / 1.5) * std_value)

    return players_df.round(1)


path = "data\\raw\\"
years = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
impute_cols = [
    "saves",
    "penalties_saved",
    "clean_sheets",
    "goals_conceded",
    "bonus",
    "bps",
    "creativity",
    "influence",
    "threat",
    "goals_scored",
    "assists",
    "minutes",
    "own_goals",
    "yellow_cards",
    "red_cards",
    "penalties_missed",
    "points_per_game",
    "total_points",
]
clean_data = clean_fpl(path, years)
last_season = clean_data[clean_data["season"] == "2023-24"]
this_season = clean_data[clean_data["season"] == "2024-25"]
players_24_25 = make_available_players_df(this_season, last_season)
histogram_plots(players_24_25)
players_24_25_impute = impute_missing_values(players_24_25, impute_cols)
histogram_plots(players_24_25_impute)
players_24_25_impute.to_csv("data\\processed\\players.csv")
