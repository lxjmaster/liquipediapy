from liquipediapy import Leagueoflegends
import time

lol_obj = Leagueoflegends()

# teams = lol_obj.get_teams()
#
# info = lol_obj.get_team_info(teams[0]["team"])
info = lol_obj.get_team_info("suning")
print(info)

# tournament_info = lol_obj.get_tournament_info("LPL/2018/Spring")
# print(tournament_info)

# tournaments = lol_obj.get_tournaments("S-Tier")
# print(tournaments)
# for tournament in tournaments:
#     name = tournament["page"].replace("https://liquipedia.net/leagueoflegends/", "")
#     tournament_info = lol_obj.get_tournament_info(name)
#     print(name, tournament_info)
#     time.sleep(35)
