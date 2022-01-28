from liquipediapy import Leagueoflegends

lol_obj = Leagueoflegends("appname")

# teams = lol_obj.get_teams()
#
# info = lol_obj.get_team_info(teams[0]["team"])
# info = lol_obj.get_team_info("100 Thieves")

# tournaments = lol_obj.get_tournaments("S-Tier")
# print(tournaments)
tournament = lol_obj.get_tournament_info("LPL/2021/Spring")
print(tournament)