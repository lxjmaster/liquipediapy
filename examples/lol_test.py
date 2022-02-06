from liquipediapy import Leagueoflegends
import time

lol_obj = Leagueoflegends("appname")

# teams = lol_obj.get_teams()
#
# info = lol_obj.get_team_info(teams[0]["team"])
info = lol_obj.get_team_info("100 Thieves")
print(info)

# tournament_info = lol_obj.get_tournament_info("LCK/2020/Summer")
# print(tournament_info)

# tournaments = lol_obj.get_tournaments("S-Tier")
# for tournament in tournaments:
#     name = tournament["page"].replace("https://liquipedia.net/leagueoflegends/", "")
#     tournament_info = lol_obj.get_tournament_info(name)
#     print(name, tournament_info)
#     time.sleep(35)
