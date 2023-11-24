# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file

    # enter the file name in terminal
    filename = sys.argv[1]

    # open the file then using for to add team and score into a list
    # 1 line is a 1 list iteam
    # it will give us a list of dictionary [{}, {}, {}]
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for team in reader:
            data = dict(team)
            # convert the score from str to int
            data["rating"] = int(team["rating"])
            teams.append(data)
        # print(teams)

    counts = {}
    # TODO: Simulate N tournaments and keep track of win counts
    for i in range(N):
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] += 1
        else:
            counts[winner] = 1
        # print(winner)

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO
    # idk why this will not become a infinite loop
    # I think that it just want to get a True reture and let the def run here
    while len(teams) != 1:
        teams = simulate_round(teams)
    # print (teams[0]["team"])
    return teams[0]["team"]


if __name__ == "__main__":
    main()