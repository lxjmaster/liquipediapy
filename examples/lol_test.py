from liquipediapy import Leagueoflegends

lol_obj = Leagueoflegends("appname")

teams = lol_obj.get_teams()

info = lol_obj.get_team_info(teams[0]["team"])
