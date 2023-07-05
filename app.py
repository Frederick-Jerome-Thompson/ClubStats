
import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def TSR(shots_for, shots_against):
  if (shots_against + shots_for) > 0:
    theTSR = shots_for / (shots_against + shots_for)
  else:
    theTSR = 0

  return theTSR

def make_grid(cols,rows):
    grid = [1]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns([1,1])
    return grid


team_pdf = pd.read_csv('DCFC_2022_23_All.csv')
indv_pdf = pd.read_csv('DCFC_2022_23_All_Individual.csv')





#app
st.header("DCFC 2022 Stats")
st.subheader("Presented by the Statistics Commitee")
st.subheader("Chair: Lynne")
st.write('These statistics are limited by the ability of our volunteer statistical recorders.  The volunteers give their best efforts for accuracy, but errors can arise.')



#pick a season
seasonList = list(team_pdf['Season'].unique())
seasonList.append("All")
seasonOption = st.selectbox(
     'Choose Season',
     seasonList)

st.header("%s Totals" % seasonOption)

#st.write('You selected:', seasonOption)

if seasonOption != "All":
    team_pdf = team_pdf[team_pdf['Season']==seasonOption]
    indv_pdf = indv_pdf[indv_pdf['Season']==seasonOption]


#data
games_played = team_pdf['Game'].count()
wins = team_pdf[team_pdf['Goals'] > team_pdf['Goals.1']]['Game'].count()
losses = team_pdf[team_pdf['Goals'] < team_pdf['Goals.1']]['Game'].count()
draws = games_played - wins -losses
st.write('games: %s wins: %s draws: %s losses: %s' % (games_played,wins,draws,losses))




team_pdf['TSR_Shots'] = team_pdf.apply(lambda row : TSR(row['Shots'],
                     row['Shots.1']), axis = 1)

team_pdf['TSR_Shots_OG'] = team_pdf.apply(lambda row : TSR(row['On Goal'],
                     row['On Goal.1']), axis = 1)

team_pdf['TSR_Shots_XG'] = team_pdf.apply(lambda row : TSR(row['XG'],
                     row['XG.1']), axis = 1)


team_pdf['GoalDiff'] = team_pdf['Goals'] - team_pdf['Goals.1']
team_pdf['XGDiff'] = team_pdf['XG'] - team_pdf['XG.1']


total_pdf = team_pdf[['Goals', 'Shots', 'On Goal', 'Corners', 'Fouls', 'Yellow', 'Red', 'XG', \
                   'Goals.1', 'Shots.1', 'On Goal.1', 'Corners.1', 'Fouls.1', 'Yellow.1', 'Red.1', 'XG.1']].sum().reset_index()

total_pdf.columns = ['index','value']
total_pdf = total_pdf.set_index('index')
total_pdf = total_pdf.transpose()
total_pdf['TSR'] = TSR(total_pdf['Shots'].value,total_pdf['Shots.1'].value)
total_pdf['TSR_OG'] = TSR(total_pdf['On Goal'].value,total_pdf['On Goal.1'].value)
total_pdf['TSR_XG'] = TSR(total_pdf['XG'].value,total_pdf['XG.1'].value)

total_pdf = total_pdf.transpose()

#defensive Stats

defensiveStats = ['Saves', 'Block', 'Interception', 'Tackle', 'Steal', 'Clear Defensive', 'Clear Side']
seasonDefensive = indv_pdf[defensiveStats].sum().reset_index()
seasonDefensive = seasonDefensive.set_index('index')




#show data
mygrid = make_grid(2,7)

mygrid[0][0].subheader("Us")
mygrid[0][1].subheader("Them")
mygrid[1][0].metric("Goals",round(total_pdf.loc["Goals"],0))
mygrid[1][1].metric("Goals Allowed",round(total_pdf.loc["Goals.1"],0))
mygrid[1][0].metric("Shots",round(total_pdf.loc["Shots"],0))
mygrid[1][1].metric("Shots Allowed",round(total_pdf.loc["Shots.1"],0))
mygrid[1][0].metric("Shots On Goal",round(total_pdf.loc["On Goal"],0))
mygrid[1][1].metric("Shots On Goal Allowed",round(total_pdf.loc["On Goal.1"],0))
mygrid[1][0].metric("XG",round(total_pdf.loc["XG"],1))
mygrid[1][1].metric("XG Allowed",round(total_pdf.loc["XG.1"],1))

st.header("Total Shot Ratio")
st.subheader("-ratio of our shots divided by the total shots in game")
st.metric("TSR",round(total_pdf.loc["TSR"],2))
st.subheader("TSR for on goal shots")
st.metric("TSR On Goal", round(total_pdf.loc["TSR_OG"],2))
st.subheader("TSR for Expected Goal")
st.metric("TSR XG", round(total_pdf.loc["TSR_XG"],2))

#per game
st.subheader('per Game Totals')
mygrid2 = make_grid(2,7)

mygrid2[0][0].subheader("Us")
mygrid2[0][1].subheader("Them")
mygrid2[1][0].metric("Goals",round(total_pdf.loc["Goals"]/games_played,1))
mygrid2[1][1].metric("Goals Allowed",round(total_pdf.loc["Goals.1"]/games_played,1))
mygrid2[1][0].metric("Shots",round(total_pdf.loc["Shots"]/games_played,1))
mygrid2[1][1].metric("Shots Allowed",round(total_pdf.loc["Shots.1"]/games_played,1))
mygrid2[1][0].metric("Shots On Goal",round(total_pdf.loc["On Goal"]/games_played,1))
mygrid2[1][1].metric("Shots On Goal Allowed",round(total_pdf.loc["On Goal.1"]/games_played,1))
mygrid2[1][0].metric("XG",round(total_pdf.loc["XG"]/games_played,2))
mygrid2[1][1].metric("XG Allowed",round(total_pdf.loc["XG.1"]/games_played,2))



#defensive Stats
st.header("Defensive Stats")
st.write('These were difficult to define and monitor.  As such, they were not recorded for all games.')

mygridD = make_grid(2,8)
mygridD[0][0].subheader("Season")
mygridD[0][1].subheader("per Game")

mygridD[1][0].metric("Saves", seasonDefensive.loc['Saves'])
mygridD[1][0].metric("Blocks", seasonDefensive.loc['Block'])
mygridD[1][0].metric("Interceptions", seasonDefensive.loc['Interception'])
mygridD[1][0].metric("Tackles", seasonDefensive.loc['Tackle'])
mygridD[1][0].metric("Steals", seasonDefensive.loc['Steal'])
mygridD[1][0].metric("Defensive Clears", seasonDefensive.loc['Clear Defensive'])
mygridD[1][0].metric("Sideline Clears", seasonDefensive.loc['Clear Side'])

mygridD[1][1].metric("Saves", round(seasonDefensive.loc['Saves']/games_played,1))
mygridD[1][1].metric("Blocks", round(seasonDefensive.loc['Block']/games_played,1))
mygridD[1][1].metric("Interceptions", round(seasonDefensive.loc['Interception']/games_played,1))
mygridD[1][1].metric("Tackles", round(seasonDefensive.loc['Tackle']/games_played,1))
mygridD[1][1].metric("Steals", round(seasonDefensive.loc['Steal']/games_played,1))
mygridD[1][1].metric("Defensive Clears", round(seasonDefensive.loc['Clear Defensive']/games_played,1))
mygridD[1][1].metric("Sideline Clears", round(seasonDefensive.loc['Clear Side']/games_played,1))



#scatter plot viz
fig_scatter, ax_scatter = plt.subplots()

#plt.title("Actual Goals vrs Expected Goals", loc="left")
usXG = list(team_pdf['XG'].values)
themXG = list(team_pdf['XG.1'].values)

usGoals = list(team_pdf['Goals'].values)
themGoals = list(team_pdf['Goals.1'].values)

#plot xg=actual goals line
# Creating a sample data for x-values
x = np.arange(0, 7, 0.1)

# Provide parameters of the linear function
m, c = 1.0, 0.0

# Calculating the y-values for all the x'-values
y = (m * x) + c

# Plotting the line created by the linear function
ax_scatter.plot(x, y, 'c', linewidth=2)


ax_scatter.scatter(usXG,usGoals,color='red',label="DCFC")
ax_scatter.scatter(themXG,themGoals,color='grey',label="opponent")
ax_scatter.set_xlabel("XG")
ax_scatter.set_ylabel("Actual Goals")
ax_scatter.legend()

st.header("Actual vs Expected Goals")
st.subheader("-for each team in each game")
st.pyplot(fig_scatter)

#data table
st.header("Data Table")
team2 = team_pdf.set_index("Game")
st.dataframe(team2)

#GD versus TSR
fig_GDvTSR, ax_GDvTSR = plt.subplots()

st.header("Goal Difference vs TSR")
st.subheader("-for each game (outliers: Reds tournament in Red)")
GD = list(team_pdf['GoalDiff'].values)
TSR = list(team_pdf['TSR_Shots'].values)
colors = ['red' if 'Reds' in game else 'blue' for game in list(team_pdf['Game'])]
ax_GDvTSR.scatter(TSR,GD,color=colors)
ax_GDvTSR.set_xlabel('TSR')
ax_GDvTSR.set_ylabel('GD')

st.pyplot(fig_GDvTSR)
