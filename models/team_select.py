import re
import pulp
import pandas as pd
from pulp import LpStatus, value

PATH = "data\\processed"
pdata = pd.read_csv(f"{PATH}\\2024-25\\players.csv")
prob = pulp.LpProblem('FantasyTeam', pulp.LpMaximize)

decision_variables = []
pdata['variable'] = None
for rownum, row in pdata.iterrows():
    variable = str('x' + str(rownum))
    variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
    decision_variables.append(variable)
    pdata.loc[rownum, 'variable'] = rownum
print ("Total number of decision_variables: " + str(len(decision_variables)))

total_points_last_season = ""
for rownum, row in pdata.iterrows():
    for i, player in enumerate(decision_variables):
        if rownum == i:
            formula = row['total_points_last_season']*player
            total_points_last_season += formula

prob += total_points_last_season
print("Optimization function: " + str(total_points_last_season))

avail_cash = 830
total_paid = ""
for rownum, row in pdata.iterrows():
    for i, player in enumerate(decision_variables):
        if rownum == i:
            formula = row['now_cost']*player
            total_paid += formula

prob += (total_paid <= avail_cash)

avail_gk = 1
total_gk = ""
for rownum, row in pdata.iterrows():
    for i, player in enumerate(decision_variables):
        if rownum == i:
            if row['element_type_name'] == 'GK':
                formula = 1*player
                total_gk += formula
prob += (total_gk == avail_gk)
print(total_gk)

avail_def = 4
total_def = ""
for rownum, row in pdata.iterrows():
    for i, player in enumerate(decision_variables):
        if rownum == i:
            if row['element_type_name'] == 'DEF':
                formula = 1*player
                total_def += formula

prob += (total_def == avail_def)
print(len(total_def))

avail_mid = 4
total_mid = ""
for rownum, row in pdata.iterrows():
    for i, player in enumerate(decision_variables):
        if rownum == i:
            if row['element_type_name'] == 'MID':
                formula = 1*player
                total_mid += formula

prob += (total_mid == avail_mid)
print(len(total_mid))

avail_fwd = 2
total_fwd = ""
for rownum, row in pdata.iterrows():
    for i, player in enumerate(decision_variables):
        if rownum == i:
            if row['element_type_name'] == 'FWD':
                formula = 1*player
                total_fwd += formula

prob += (total_fwd == avail_fwd)
print(len(total_fwd))

team_dict= {}
for team in set(pdata.team_code):
    team_dict[str(team)]=dict()
    team_dict[str(team)]['avail'] = 3
    team_dict[str(team)]['total'] = ""
    for rownum, row in pdata.iterrows():
        for i, player in enumerate(decision_variables):
            if rownum == i:
                if row['team_code'] == team:
                    formula = 1*player
                    team_dict[str(team)]['total'] += formula

    prob += (team_dict[str(team)]['total'] <= team_dict[str(team)]['avail'])
print(len(team_dict))

prob.writeLP('FantasyTeam.lp')
optimization_result = prob.solve()
prob.objective
assert optimization_result == pulp.LpStatusOptimal
print("Status:", LpStatus[prob.status])
print("Optimal Solution to the problem: ", value(prob.objective))
print("Individual decision_variables: ")

for v in prob.variables():
    print(v.name, "=", v.varValue)

variable_name = []
variable_value = []

for v in prob.variables():
    variable_name.append(v.name)
    variable_value.append(v.varValue)

df = pd.DataFrame({'variable': variable_name, 'value': variable_value})

for rownum, row in df.iterrows():
    value = re.findall(r'(\d+)', row['variable'])
    df.loc[rownum, 'variable'] = int(value[0])

df = df.sort_values(by='variable')
merged_df = pd.merge(df, pdata, on='variable', how='inner')
print(merged_df[merged_df.value==1].sort_values('element_type'))
merged_df[merged_df.value==1].now_cost.sum()
merged_df[merged_df.value==1].total_points.sum()
merged_df[merged_df.value==1].sort_values('total_points', ascending=False)
