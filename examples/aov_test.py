from liquipediapy import ArenaOfValor


aov_obj = ArenaOfValor()
# tournaments = aov_obj.get_tournaments("A-Tier")
# print(tournaments)
tournament = aov_obj.get_tournament_info("Korea_King_Pro_League/2019/Spring")
print(tournament)
