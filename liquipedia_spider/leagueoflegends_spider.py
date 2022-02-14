from liquipediapy import Leagueoflegends
from core.config import Config
from core.db import MongoObject
import pprint


class LeagueoflegendsSpider(object):

    def __init__(self):

        self._config = Config()
        self.lol_obj = Leagueoflegends()
        self.mongo_obj = MongoObject()
        self.page_url = "https://liquipedia.net/leagueoflegends/"

    @property
    def config(self):

        return self._config.config

    def get_teams(self) -> list:
        """
        Get lol teams;
        And insert to mongodb when configure mongodb;
        :return: teams -> list[dict]
        """

        teams = self.lol_obj.get_teams()
        if len(teams) > 0:
            if self.config.has_section("MONGODB"):
                collection = self.mongo_obj.db["leagueoflegends_teams"]
                for team in teams:
                    collection.update_one({"name": team["name"]}, {"$set": team}, upsert=True)

        return teams

    def get_team_info(self, team: dict) -> dict:
        """
        Get team information;
        And insert to mongo when configure mongodb;
        :param team: dict
        :return: info -> dict
        """

        team_info = self.lol_obj.get_team_info(team["name"])
        team_info.update(team)

        if team_info:
            if self.config.has_section("MONGODB"):
                collection = self.mongo_obj.db["leagueoflegends_teams"]
                collection.update_one({"name": team_info["name"]}, {"$set": team_info}, upsert=True)
            else:
                print(team_info)

        return team_info

    def get_players(self) -> list:
        """
        Get lol players;
        And insert to mongodb when configure mongodb;
        :return: players -> list[dict]
        """

        players = self.lol_obj.get_players()
        if len(players) > 0:
            if self.config.has_section("MONGODB"):
                collection = self.mongo_obj.db["leagueoflegends_players"]
                for player in players:
                    collection.update_one({"name": player["name"]}, {"$set": player}, upsert=True)

        return players

    def get_player_info(self, player: dict) -> dict:
        """
        Get player information;
        And insert to mongo when configure mongodb;
        :param player: dict
        :return: info -> dict
        """

        player_info = self.lol_obj.get_player_info(player["name"])
        player_info.update(player)

        if player_info:
            if self.config.has_section("MONGODB"):
                collection = self.mongo_obj.db["leagueoflegends_players"]
                collection.update_one({"name": player_info["name"]}, {"$set": player_info}, upsert=True)
            else:
                print(player_info)

        return player_info

    def get_tournaments(self, tournament_type=None) -> list:
        """
        Get lol tournaments;
        And insert to mongodb when configure mongodb;
        :return: tournaments -> list[dict]:
        """

        tournaments = self.lol_obj.get_tournaments(tournament_type)
        if len(tournaments) > 0:
            if self.config.has_section("MONGODB"):
                collection = self.mongo_obj.db["leagueoflegends_tournaments"]
                for tournament in tournaments:
                    collection.update_one({"page": tournament["page"]}, {"$set": tournament}, upsert=True)

        return tournaments

    def get_tournament_info(self, tournament: dict) -> dict:
        """
        Get tournament information.
        And insert to mongo when configure mongodb;
        :param tournament: dict
        :return: tournament_info: dict
        """

        page = tournament["page"].replace(self.page_url, "")
        tournament_info = self.lol_obj.get_tournament_info(page)
        tournament_info.update(tournament)

        if tournament_info:
            if self.config.has_section("MONGODB"):
                collection = self.mongo_obj.db["leagueoflegends_tournaments"]
                collection.update_one({"page": tournament_info["page"]}, {"$set": tournament_info}, upsert=True)
            else:
                print(tournament_info)

        return tournament_info

    def main(self):

        # teams = self.get_teams()
        # for team in teams:
        #     self.get_team_info(team)
        #     input("111")
        # players = self.get_players()
        # for player in players:
        #     self.get_player_info(player)
        #     input("111")
        tournaments = self.get_tournaments("S-Tier")
        for tournament in tournaments:
            self.get_tournament_info(tournament)
            print(tournament["page"])


if __name__ == '__main__':
    lol = LeagueoflegendsSpider()
    lol.main()
