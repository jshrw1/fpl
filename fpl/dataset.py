# packages from third party
import os
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import re

path = "data\\raw\\"
years = ["2020-21", "2021-22", "2022-23", "2023-24"]


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
        data = pd.concat([data, players], ignore_index=True)

    return data


clean_data = clean_fpl(PATH=path, YEARS=years)

print("\n".join(f"- {col}" for col in clean_data[0].columns))
clean_data.select_dtypes(include=["int64", "float64"]).corr()["total_points"]

a = clean_data[
    (clean_data["total_points"] > 0)
    & (clean_data["season"] == "2022-23")
    & (clean_data["element_type_name"] == "GK")
]
a = a[["full_name", "total_points"]]
