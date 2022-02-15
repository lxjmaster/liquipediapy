from liquipediapy import WildRift
import time

wr_obj = WildRift()

# teams = lol_obj.get_teams()
#
# info = lol_obj.get_team_info(teams[0]["team"])
# info = lol_obj.get_team_info("suning")
# print(info)

tournament_info = wr_obj.get_tournament_info("Horizon_Cup/2021")
print(tournament_info)

# tournaments = wr_obj.get_tournaments("S-Tier")
# for tournament in tournaments:
#     print(tournament)
#     name = tournament["page"].replace("https://liquipedia.net/leagueoflegends/", "")
#     tournament_info = lol_obj.get_tournament_info(name)
#     print(name, tournament_info)
#     time.sleep(35)
