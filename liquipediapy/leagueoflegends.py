import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
from liquipediapy.leagueoflegends_modules.team import LeagueoflegendsTeam
import unicodedata
import re


class Leagueoflegends(object):

    def __init__(self, appname):

        self.appname = appname
        self.liquipedia = liquipediapy(appname, "leagueoflegends")
        self.__image_base_url = "https://liquipedia.net'"

    def get_players(self):

        pass

    def get_player_info(self, player_name, results=False):

        pass

    def get_teams(self):

        soup, __ = self.liquipedia.parse('Portal:Teams')
        teams = []
        templates = soup.find_all('span', class_="team-template-team-standard")
        for team in templates:
            logo_url_element = team.find("span", {"class": "team-template-lightmode"})
            team_item = {
                "team": team.a['title'],
                "logo": logo_url_element.img["src"]
            }
            teams.append(team_item)

        return teams

    def get_team_info(self, team_name, results=False):

        team_object = LeagueoflegendsTeam(team_name)
        team_name = team_object.process_team_name(team_name)
        soup, redirect_value = self.liquipedia.parse(team_name)
        if redirect_value is not None:
            team_name = redirect_value

        team = {}
        team["info"] = team_object.get_team_infobox(soup)
        team["links"] = team_object.get_team_links(soup)

        value = team_object.name + "/History"
        history_link = team_object.has_history_link(soup, value)
        if history_link:
            parse_value = team_name + "/History"
            try:
                soup, __ = self.liquipedia.parse(parse_value)
                team["history"] = team_object.get_link_history(soup)
            except ex.RequestsException:
                team["history"] = ""
        else:
            team["history"] = team_object.get_history(soup)

        # if history:
        #     parse_value = team_name + "/History"
        #     try:
        #         soup, __ = self.liquipedia.parse(parse_value)
        #         team["history"] = team_object.get_history(soup)
        #     except ex.RequestsException:
        #         team["history"] = ""
        # else:
        #     team["history"] = team_object.get_history(soup)
        #
        # if results:
        #     parse_value = team_name + "/Results"
        #     try:
        #         soup, __ = self.liquipedia.parse(parse_value)
        #     except ex.RequestsException:
        #         team["results"] = []
        #     else:
        #         team["results"] = team_object.get_team_achivements(soup)

    def get_tournaments(self, tournament_type=None):

        pass

    def get_tournament_info(self):

        pass
