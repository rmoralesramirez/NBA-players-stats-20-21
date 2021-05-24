# IMPORTS

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="dark")
sns.set_palette("viridis_r")

# DATA PREPARATION

data = ""

with open(r"...\players-stats.csv") as file:
    data = file.read().replace("\\", ",").replace("?", "c")
with open(
    r"...\players-stats-2.csv", "w"
) as file:
    file.write(data)
players_stats = pd.read_csv(
    r"...\players-stats-2.csv", encoding="latin-1"
)

players_stats.rename(columns={"Player": "Id", "Rk": "Player"}, inplace=True)

players_stats["PTS36M"] = round((players_stats.PTS / players_stats.MP) * 36, 1)
players_stats["OFFR"] = round(
    players_stats.ORB
    + players_stats.PTS
    + players_stats.AST
    - players_stats.TOV
    - players_stats.FGA
    + players_stats.FG,
    1,
)
players_stats["OFFR36M"] = round((players_stats.OFFR / players_stats.MP) * 36, 1)
players_stats["DEFR"] = round(
    players_stats.DRB + players_stats.STL + players_stats.BLK - players_stats.PF, 1
)
players_stats["DEFR36M"] = round((players_stats.DEFR / players_stats.MP) * 36, 1)
players_stats["OFFDEFRATE"] = round(players_stats.OFFR36M + players_stats.DEFR36M, 1)
players_stats["ASTPERD"] = round((players_stats.AST / players_stats.TOV), 1)
players_stats["BLKPF"] = round((players_stats.BLK / players_stats.PF), 1)
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
)
players_stats["RATETOT"] = round((players_stats.RATE * players_stats.G))
players_stats["FGA20P"] = round((players_stats.FGA / players_stats.PTS) * 20, 1)
players_stats["MP10R"] = round((players_stats.MP / players_stats.TRB) * 10, 1)
players_stats["MP10A"] = round((players_stats.MP / players_stats.AST) * 10, 1)
players_stats["MP20P"] = round((players_stats.MP / players_stats.PTS) * 20, 1)

i = players_stats[
    ((players_stats.Player == "James Harden") & (players_stats.Tm == "TOT"))
].index
print(i)
players_stats.drop(i)

# FILTERING
min10 = (players_stats["MP"] > 10) & (players_stats["G"] > 30)
min10_25 = (
    (players_stats["MP"] > 10) & (players_stats["MP"] < 25) & (players_stats["G"] > 30)
)
players10 = players_stats[min10]
players10_25 = players_stats[min10_25]
top5MP20P = players10.nsmallest(5, "MP20P")
top5MP20P10 = players10.nsmallest(10, "MP20P")

top5def36m = players10.nlargest(6, "DEFR36M")
top5pts36m = players10.nlargest(5, "PTS36M")
topoffdefrate = players10.nlargest(10, "OFFDEFRATE")
topoffdefrateunder25 = players10_25.nlargest(10, "OFFDEFRATE")
top5ratetot = players10.nlargest(5, "RATETOT")
top5mp10r = players10.nsmallest(5, "MP10R")
top5mp10a = players10.nsmallest(6, "MP10A")

# VARIABLES PREPARATION
top5mp20p = top5MP20P.MP20P.tolist()
top5mp20players = top5MP20P.Player.tolist()
top5mp20fga = top5MP20P["FGA20P"].tolist()
top5mp20players2 = top5MP20P["Player"].tolist()

top10mp20p = top5MP20P10.MP20P.tolist()
top10mp20players = top5MP20P10.Player.tolist()
top10mp20fga = top5MP20P10["FGA20P"].tolist()
top10mp20players2 = top5MP20P10["Player"].tolist()

top5def36mplayers = top5def36m.Player.tolist()
top5def36mrate = top5def36m.DEFR36M.tolist()

topoffdefrateplayers = topoffdefrate.Player.tolist()
topoffdefratedefrate36m = topoffdefrate.DEFR36M.tolist()
topoffdefrateoffrate36m = topoffdefrate.OFFR36M.tolist()
topoffdefrateplayers2 = topoffdefrate["Player"].tolist()

top5ratetotplayers = top5ratetot.Player.tolist()
top5ratetot = top5ratetot.RATETOT.tolist()

top5mp10rplayers = top5mp10r.Player.tolist()
top5mp10r = top5mp10r.MP10R.tolist()

top5mp10aplayers = top5mp10a.Player.tolist()
top5mp10a = top5mp10a.MP10A.tolist()

topoffdefrateplayersunder25 = topoffdefrateunder25.Player.tolist()
topoffdefratedefrate36munder25 = topoffdefrateunder25.DEFR36M.tolist()
topoffdefrateoffrate36munder25 = topoffdefrateunder25.OFFR36M.tolist()
topoffdefrateplayers2under25 = topoffdefrateunder25["Player"].tolist()

# VISUALIZATION
# Top 5 faster players to score 20 pts by minutes played
bp = sns.barplot(top5mp20p, top5mp20players)

for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
plt.title("Top 5 fastest players to score 20 pts by minutes played", size=13)
plt.xlabel("Minutes played")
plt.show()

plt.clf()

# Minutes played VS FG attempted to score 20 pts
fig, sc = plt.subplots()
sc.scatter(top10mp20p, top10mp20fga)

for i, top10mp20players2 in enumerate(top5MP20P10["Player"]):
    sc.annotate(
        top10mp20players2, (top10mp20p[i], top10mp20fga[i] + 0.075), ha="center"
    )
plt.title(
    "Minutes played VS FG attempted to score 20 pts (top 10 fastest scorers)", size=13
)
plt.xlabel("Minutes played")
plt.ylabel("FG attempted")
plt.show()
plt.clf()

# Top 5 defenders by rate per 36 min
bp = sns.barplot(top5def36mrate, top5def36mplayers)

for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
plt.title("Top 5 defenders by rate per 36 min", size=13)
plt.xlabel("Defensive rate")
plt.show()

plt.clf()

# Offensive VS Defensive rate
fig, sc = plt.subplots()
sc.scatter(topoffdefrateoffrate36m, topoffdefratedefrate36m)

for i, topoffdefrateplayers2 in enumerate(topoffdefrate["Player"]):
    sc.annotate(
        topoffdefrateplayers2,
        (topoffdefrateoffrate36m[i] + 0.5, topoffdefratedefrate36m[i]),
        ha="center",
        rotation=25,
    )
plt.title("Offensive VS Defensive rate", size=13)
plt.xlabel("Offensive rate per 36 mp")
plt.ylabel("Defensive rate per 36 mp")

plt.show()

# Offensive VS Defensive rate (Players under 25 mp)
fig, sc = plt.subplots()
sc.scatter(topoffdefrateoffrate36munder25, topoffdefratedefrate36munder25)

for i, topoffdefrateplayers2under25 in enumerate(topoffdefrateunder25["Player"]):
    sc.annotate(
        topoffdefrateplayers2under25,
        (topoffdefrateoffrate36munder25[i], topoffdefratedefrate36munder25[i] + 0.075),
        ha="center",
    )
plt.title("Offensive VS Defensive rate (Players under 25 mp)", size=13)
plt.xlabel("Offensive rate per 36 mp")
plt.ylabel("Defensive rate per 36 mp")
plt.show()

# Top 5 total rate
bp = sns.barplot(top5ratetot, top5ratetotplayers)

for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.0f}".format(width),
        ha="center",
        va="center",
    )
plt.title("Top 5 players total rate", size=13)
plt.xlabel("Total rate")
plt.show()

plt.clf()

# Top 5 fastest players to get 10 reb
bp = sns.barplot(top5mp10r, top5mp10rplayers)

for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
plt.title("Top 5 fastest players to get 10 reb", size=13)
plt.xlabel("Minutes played")
plt.show()

plt.clf()

# Top 5 fastest players to get 10 ast
bp = sns.barplot(top5mp10a, top5mp10aplayers)

for p in bp.patches:
    width = p.get_width()
    plt.text(
        0.9 * p.get_width(),
        p.get_y() + 0.55 * p.get_height(),
        "{:1.1f}".format(width),
        ha="center",
        va="center",
    )
plt.title("Top 5 fastest players to get 10 ast", size=13)
plt.xlabel("Minutes played")
plt.show()

plt.clf()

# EXPORTATION

players_stats.to_excel(
    r"...\players-stats-extracted.xlsx",
    index=False,
)
