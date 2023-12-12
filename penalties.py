"""
USL Championship Penalty Kick Analysis
Luke Berry, Video/Data Analyst - Monterey Bay Football Club
Project started February 15, 2023
"""

import csv  # used for taking in data
import random

import plotly.graph_objects as go

CURRENT_YEAR = 2023
CURRENT_MONTH = 4
PENALTY_TYPE = "Career"  # "Last Season" or "Career" are the two options, changes how the first index of the dictionary values is calculated (penalties taken)

DATA_SHEET = "data/penaltyData.csv"

def calculateTaker():
    CURRENT_TEAM = input("Enter team: ")

    """
    PENALTY SCORES CALCULATION
    Level 1
    - PK taken current year in same team

    Level 2
    - PK taken current year in different team
    - PK taken last year in same team

    Level 3
    - PK taken last year in different team
    - PK taken 2 years ago in same team

    Level 4
    - PK taken 2 years ago in different team
    
    Level 5
    - Any other PK taken

    Other:
    - PK scored: +1
    - PK missed: -2
    """

    LEVEL_ONE = 21
    LEVEL_TWO = 7
    LEVEL_THREE = 3
    LEVEL_FOUR = 2
    LEVEL_FIVE = 1

    GOAL_PK = 1
    MISSED_PK = -2
    

    player_penalty_scores = {}  # dictionary holding penalties taken in {name: PENALTY_TYPE total count, penalty scores]
    with open(DATA_SHEET, newline='') as file:
        scores_reader = csv.reader(file)
        skip = True
        team_penalties = 0
        for line in scores_reader:  # iterates through lines in csv file
            if skip:  # skips first line (column titles)
                skip = False
                continue
            if line[1] == CURRENT_TEAM:
                if line[0] not in player_penalty_scores:  # checks if player is already in dictionary
                    player_penalty_scores[line[0]] = [0, 0]  # new player dictionary index created

                # Total PKs taken (first index of dictionary value)
                player_penalty_scores[line[0]][0] += 1

                # Adding to PK score (second index of dictionary value)
                if CURRENT_YEAR == int(line[4]) and CURRENT_TEAM == line[2]:  # penalties taken in current year
                    player_penalty_scores[line[0]][1] += LEVEL_ONE
                    team_penalties += LEVEL_ONE
                elif CURRENT_YEAR == int(line[4]) and CURRENT_TEAM != line[4] or CURRENT_YEAR - 1 == int(
                        line[4]) and CURRENT_TEAM == line[4]:
                    player_penalty_scores[line[0]][1] += LEVEL_TWO
                    team_penalties += LEVEL_TWO
                elif CURRENT_YEAR - 1 == int(line[4]) and CURRENT_TEAM != line[4] or CURRENT_YEAR - 2 == int(
                        line[4]) and CURRENT_TEAM == line[4]:
                    player_penalty_scores[line[0]][1] += LEVEL_THREE
                    team_penalties += LEVEL_THREE
                elif CURRENT_YEAR - 2 == int(line[4]) and CURRENT_TEAM != line[4]:
                    player_penalty_scores[line[0]][1] += LEVEL_FOUR
                    team_penalties += LEVEL_FOUR
                else:
                    player_penalty_scores[line[0]][1] += LEVEL_FIVE
                    team_penalties += LEVEL_FIVE

                if line[12] != "Goal":
                    player_penalty_scores[line[0]][1] += MISSED_PK
                    team_penalties += MISSED_PK
                else:
                    player_penalty_scores[line[0]][1] += GOAL_PK
                    team_penalties += GOAL_PK

    if not player_penalty_scores:
        print("No data found")
    file.close()
    """
    OUTPUTTING DATA TO CONSOLE
    """
    # Sorts the player scores by total score descending
    sorted_by_score = sorted(player_penalty_scores.items(), key=lambda x: x[1][1], reverse=True)

    # Sets length of players outputted
    if len(sorted_by_score) >= 5:
        total = 5
    else:
        total = len(sorted_by_score)

    # Outputs the top 5 PK takers
    for i in range(total):
        penalty_percentage = round((sorted_by_score[i][1][1] / team_penalties) * 100)
        print(str(i + 1) + ". " + sorted_by_score[i][0] + " " + str(penalty_percentage) + "%")
    print()


def penaltyLocations():
    #Creating shot map
    with open(DATA_SHEET, newline='') as file:
        location_reader = csv.reader(file)
        skip = True
        name = input("Enter player name: ")

        # Creating goal graphic
        fig = go.Figure(go.Scatter(x=[1, 1, 11, 11], y=[0, 4, 4, 0]))
        fig.add_shape(type="rect", x0=1, y0=0, x1=11, y1=4, line=dict(color="Black", width=2), fillcolor="White")
        fig.add_shape(type="rect", x0=2, y0=0, x1=10, y1=3, line=dict(color="Black", width=2), fillcolor="White")

        # Add title to the graph
        fig.update_layout(title="Penalty Kick Locations for {}".format(name))
        
        #Plotting shot map
        for line in location_reader:  # iterates through lines in csv file
            if skip:  # skips first line (column titles)
                skip = False
                continue
            if line[0] == name:
                offset = random.randint(-35, 35) / 100
                if line[12] == "Goal":
                    ball_color = "Green"
                elif line[12] == "Miss":
                    ball_color = "Red"
                elif line[12] == "Save":
                    ball_color = "Yellow"
                else:
                    print("ERROR: Shot result not tracked correctly")
                    
                fig.add_shape(type="circle", xref = "x", yref = "y", fillcolor = ball_color, x0 = int(line[10])+0.30+offset, y0 = int(line[11])+0.35+offset, x1 = int(line[10])+0.70+offset, y1 = int(line[11])+0.65+offset, line_color = "Black")
        fig.show()

    """
    RUNNING PROGRAM
    """


user_continue = True
while user_continue:
    print("-=-=-=-=-=-=-")
    print("1. Penalty kick taker percentage")
    print("2. Penalty kick locations")
    print("-=-=-=-=-=-=-")
    choice = int(input("My choice: "))

    if choice == 1:
        user_continue_1 = True
        while user_continue_1:
            calculateTaker()
            temp_choice = input("Analyze another team? (Y/N): ")
            if not (temp_choice.lower() == "yes" or temp_choice.lower() == "y"):
                user_continue_1 = False
    elif choice == 2:
        user_continue_2 = True
        while user_continue_2:
            penaltyLocations()
            temp_choice = input("Analyze another player? (Y/N): ")
            if not (temp_choice.lower() == "yes" or temp_choice.lower() == "y"):
                user_continue_2 = False


    temp_choice = input("Continue to analyze? (Y/N): ")
    if not (temp_choice.lower() == "yes" or temp_choice.lower() == "y"):
        user_continue = False
