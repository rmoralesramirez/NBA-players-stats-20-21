# IMPORTS

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="dark")
sns.set_palette("viridis_r")

# DATA PREPARATION

data = ""

with open(r"...\players-stats.csv") as file:
    data = (
        file.read().replace("\\", ",").replace("?", "c")
    )  # Separation of Player name and ID and correction for Eastern-European c's
with open(
    r"...\players-stats-2.csv",
    "w",  # Creation of an intermediate csv file with first corrections made
) as file:
    file.write(data)
players_stats = pd.read_csv(
    r"...\players-stats-2.csv", encoding="latin-1"  # Encoding from UTF-8 to latin-1
)

players_stats.rename(
    columns={"Player": "Id", "Rk": "Player"}, inplace=True
)  # Renaming of columns previously separated

# Calculated columns
players_stats["PTS36M"] = round(
    (players_stats.PTS / players_stats.MP) * 36, 1
)  # Points per 36 minutes
players_stats["OFFR"] = round(
    players_stats.ORB
    + players_stats.PTS
    + players_stats.AST
    - players_stats.TOV
    - players_stats.FGA
    + players_stats.FG,
    1,
)  # Offensive rate
players_stats["OFFR36M"] = round(
    (players_stats.OFFR / players_stats.MP) * 36, 1
)  # Offensive rate per 36 minutes
players_stats["DEFR"] = round(
    players_stats.DRB + players_stats.STL + players_stats.BLK - players_stats.PF, 1
)  # Defensive rate
players_stats["DEFR36M"] = round(
    (players_stats.DEFR / players_stats.MP) * 36, 1
)  # Defensive rate per 36 minutes
players_stats["OFFDEFRATE"] = round(
    players_stats.OFFR36M + players_stats.DEFR36M, 1
)  # Offensive and defensive rating
players_stats["ASTPERD"] = round(
    (players_stats.AST / players_stats.TOV), 1
)  # Assist per turnover ratio
players_stats["BLKPF"] = round(
    (players_stats.BLK / players_stats.PF), 1
)  # Block per personal foul ratio
players_stats["RATE"] = round(
    (
        players_stats.PTS
        + players_stats.AST
        + players_stats.TRB
        + players_stats.STL
        + players_stats.BLK
        - players_stats.PF
        - players_stats.TOV
        + players_stats.FG
        - players_stats.FGA
        + players_stats.FT
        - players_stats.FTA
    ),
    1,
)  # Overall rating per game
players_stats["RATETOT"] = round(
    (players_stats.RATE * players_stats.G)
)  # Total overall rating
players_stats["FGA20P"] = round(
    (players_stats.FGA / players_stats.PTS) * 20, 1
)  # Field goals attempted to score 20 points
players_stats["MP10R"] = round(
    (players_stats.MP / players_stats.TRB) * 10, 1
)  # Needed minutes to grab 10 rebounds
players_stats["MP10A"] = round(
    (players_stats.MP / players_stats.AST) * 10, 1
)  # Needed minutes to get 10 assists
players_stats["MP20P"] = round(
    (players_stats.MP / players_stats.PTS) * 20, 1
)  # Needed minutes to score 20 points

# FILTERING

min10 = (players_stats["MP"] > 10) & (
    players_stats["G"] > 30
)  # Players with more than 10 minutes per game and more than 30 games played
players10 = players_stats[min10]  # New filtered dataframe
min10_25 = (
    (players_stats["MP"] > 10) & (players_stats["MP"] < 25) & (players_stats["G"] > 30)
)  # Players with more than 10 minutes and less than 25 per game and more than 30 games played
players10_25 = players_stats[min10_25]  # New filtered dataframe

# Tops preparation for graphs limitation
# As some players were traded during the season, some tops have been modified and instead of 
# requiring 5 players for a top 5, they query an extra player as one of the previous appears duplicated
top5MP20P = players10.nsmallest(5, "MP20P")  # Top 5 fastest players to score 20 points
top5MP20P10 = players10.nsmallest(
    10, "MP20P"
)  # Top 10 fastest players to score 20 points
top5def36m = players10.nlargest(6, "DEFR36M")  # Top 5 defensive rate players
topoffdefrate = players10.nlargest(10, "OFFDEFRATE")  # Top 10 offensive rate players
topoffdefrateunder25 = players10_25.nlargest(
    10, "OFFDEFRATE"
)  # Top 10 offensive rate players with less than 25 minutes per game
top5ratetot = players10.nlargest(5, "RATETOT")  # Top 5 players with best total rate
top5mp10r = players10.nsmallest(5, "MP10R")  # Top 5 fastest players to grab 10 rebounds
top5mp10a = players10.nsmallest(6, "MP10A")  # Top 5 fastest players to get 10 assists

# VARIABLES PREPARATION

# Top 5 faster players to score 20 pts by minutes played
top5mp20p = top5MP20P.MP20P.tolist()
top5mp20players = top5MP20P.Player.tolist()
top5mp20fga = top5MP20P["FGA20P"].tolist()
top5mp20players2 = top5MP20P["Player"].tolist()

# Minutes played VS FG attempted to score 20 pts
top10mp20p = top5MP20P10.MP20P.tolist()
top10mp20players = top5MP20P10.Player.tolist()
top10mp20fga = top5MP20P10["FGA20P"].tolist()
top10mp20players2 = top5MP20P10["Player"].tolist()

# Top 5 defenders by rate per 36 min
top5def36mplayers = top5def36m.Player.tolist()
top5def36mrate = top5def36m.DEFR36M.tolist()

# Offensive VS Defensive rate
topoffdefrateplayers = topoffdefrate.Player.tolist()
topoffdefratedefrate36m = topoffdefrate.DEFR36M.tolist()
topoffdefrateoffrate36m = topoffdefrate.OFFR36M.tolist()
topoffdefrateplayers2 = topoffdefrate["Player"].tolist()

# Offensive VS Defensive rate (Players under 25 mp)
topoffdefrateplayersunder25 = topoffdefrateunder25.Player.tolist()
topoffdefratedefrate36munder25 = topoffdefrateunder25.DEFR36M.tolist()
topoffdefrateoffrate36munder25 = topoffdefrateunder25.OFFR36M.tolist()
topoffdefrateplayers2under25 = topoffdefrateunder25["Player"].tolist()

# Top 5 total rate
top5ratetotplayers = top5ratetot.Player.tolist()
top5ratetot = top5ratetot.RATETOT.tolist()

# Top 5 fastest players to grab 10 reb
top5mp10rplayers = top5mp10r.Player.tolist()
top5mp10r = top5mp10r.MP10R.tolist()

# Top 5 fastest players to get 10 ast
top5mp10aplayers = top5mp10a.Player.tolist()
top5mp10a = top5mp10a.MP10A.tolist()

# VISUALIZATION

# Top 5 faster players to score 20 pts by minutes played
bp = sns.barplot(top5mp20p, top5mp20players)
# Addition of data point labels
for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
# Graph details
plt.title("Top 5 fastest players to score 20 pts by minutes played", size=13)
plt.xlabel("Minutes played")
plt.show()
plt.clf()

# Minutes played VS FG attempted to score 20 pts
fig, sc = plt.subplots()
sc.scatter(top10mp20p, top10mp20fga)
# Addition of data point labels
for i, top10mp20players2 in enumerate(top5MP20P10["Player"]):
    sc.annotate(
        top10mp20players2, (top10mp20p[i], top10mp20fga[i] + 0.075), ha="center"
    )
# Graph details
plt.title(
    "Minutes played VS FG attempted to score 20 pts (top 10 fastest scorers)", size=13
)
plt.xlabel("Minutes played")
plt.ylabel("FG attempted")
plt.show()
plt.clf()

# Top 5 defenders by rate per 36 min
bp = sns.barplot(top5def36mrate, top5def36mplayers)
# Addition of data point labels
for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
# Graph details
plt.title("Top 5 defenders by rate per 36 min", size=13)
plt.xlabel("Defensive rate")
plt.show()
plt.clf()

# Offensive VS Defensive rate
fig, sc = plt.subplots()
sc.scatter(topoffdefrateoffrate36m, topoffdefratedefrate36m)
# Addition of data point labels
for i, topoffdefrateplayers2 in enumerate(topoffdefrate["Player"]):
    sc.annotate(
        topoffdefrateplayers2,
        (topoffdefrateoffrate36m[i] + 0.5, topoffdefratedefrate36m[i]),
        ha="center",
        rotation=25,
    )
# Graph details
plt.title("Offensive VS Defensive rate", size=13)
plt.xlabel("Offensive rate per 36 mp")
plt.ylabel("Defensive rate per 36 mp")
plt.show()

# Offensive VS Defensive rate (Players under 25 mp)
fig, sc = plt.subplots()
sc.scatter(topoffdefrateoffrate36munder25, topoffdefratedefrate36munder25)
# Addition of data point labels
for i, topoffdefrateplayers2under25 in enumerate(topoffdefrateunder25["Player"]):
    sc.annotate(
        topoffdefrateplayers2under25,
        (topoffdefrateoffrate36munder25[i], topoffdefratedefrate36munder25[i] + 0.075),
        ha="center",
    )
# Graph details
plt.title("Offensive VS Defensive rate (Players under 25 mp)", size=13)
plt.xlabel("Offensive rate per 36 mp")
plt.ylabel("Defensive rate per 36 mp")
plt.show()

# Top 5 total rate
bp = sns.barplot(top5ratetot, top5ratetotplayers)
# Addition of data point labels
for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.0f}".format(width),
        ha="center",
        va="center",
    )
# Graph details
plt.title("Top 5 players total rate", size=13)
plt.xlabel("Total rate")
plt.show()
plt.clf()

# Top 5 fastest players to grab 10 reb
bp = sns.barplot(top5mp10r, top5mp10rplayers)
# Addition of data point labels
for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
# Graph details
plt.title("Top 5 fastest players to grab 10 reb", size=13)
plt.xlabel("Minutes played")
plt.show()
plt.clf()

# Top 5 fastest players to get 10 ast
bp = sns.barplot(top5mp10a, top5mp10aplayers)
# Addition of data point labels
for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
# Graph details
plt.title("Top 5 fastest players to get 10 ast", size=13)
plt.xlabel("Minutes played")
plt.show()
plt.clf()

# EXPORTATION

players_stats.to_csv(
    r"...\players-stats-extracted.csv",
    index=False,
)
