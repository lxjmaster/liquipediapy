import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import Liquipediapy
# from liquipediapy.wildrift_modules.team import WildRiftTeam
from liquipediapy.wildrift_modules.tournament import WildRiftTournament
import unicodedata
import re


class WildRift(object):

    def __init__(self):

        self.liquipedia = Liquipediapy("wildrift")
        self.__image_base_url = "https://liquipedia.net"

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
                "name": team.a['title'],
                "logo": self.__image_base_url + logo_url_element.img["src"]
            }
            teams.append(team_item)

        return teams

    def get_team_info(self, team_name, results=False):

        team_object = WildRiftTeam(team_name)
        team_name = team_object.process_team_name(team_name)
        soup, redirect_value = self.liquipedia.parse(team_name)
        if redirect_value is not None:
            team_name = redirect_value

        team = dict()
        team["info"] = team_object.get_team_infobox(soup)
        team["links"] = team_object.get_team_links(soup)

        value = team_object.name + "/History"
        history_link = team_object.has_history_link(soup, value)
        if history_link:
            parse_value = team_name + "/History"
            try:
                soup_tmp, __ = self.liquipedia.parse(parse_value)
                team["history"] = team_object.get_link_history(soup_tmp)
            except ex.RequestsException:
                team["history"] = ""
        else:
            team["history"] = team_object.get_history(soup)

        team["timeline"] = team_object.get_team_timeline(soup)

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

        return team

    def get_tournaments(self, tournament_type=None):

        tournaments = []
        if tournament_type is None:
            page_val = 'Portal:Tournaments'
        elif tournament_type == 'Show Matches':
            page_val = 'Show_Matches'
        elif tournament_type == "Recent Results":
            page_val = "Recent_Results"
        else:
            page_val = tournament_type + '_Tournaments'

        soup, __ = self.liquipedia.parse(page_val)
        div_rows = soup.find_all('div', {"class": re.compile("divRow")})

        for row in div_rows:
            tournament = {"status": "Normal"}
            values = row.find('div', {"class": re.compile("divCell Tournament Header")})
            if tournament_type is None:
                tournament['tier'] = values.a.get_text()
                tournament['name'] = values.b.get_text()
            else:
                tournament['tier'] = tournament_type
                tournament['name'] = values.b.get_text()

            try:
                tournament['logo'] = self.__image_base_url + \
                                     row.find('div', {"class": re.compile("divCell Tournament Header")}).find('img').get('src')
            except AttributeError:
                tournament['logo'] = ""

            try:
                tournament['page'] = self.__image_base_url + values.b.a['href']
            except AttributeError:
                tournament['page'] = ""

            try:
                tournament['date'] = row.find('div', {"class": re.compile("divCell EventDetails Date Header")}).get_text().strip()
            except AttributeError:
                tournament['date'] = ""

            try:
                tournament['prize'] = row.find(
                    'div',
                    {"class": re.compile("divCell EventDetails Prize Header")}
                ).get_text().rstrip()
            except (AttributeError, ValueError):
                tournament['prize'] = ""

            try:
                tournament['team_number'] = re.sub(
                    '[A-Za-z]',
                    '',
                    row.find(
                        'div',
                        {"class": re.compile("divCell EventDetails PlayerNumber Header")}
                    ).get_text()).rstrip()
            except AttributeError:
                tournament['team_number'] = ""

            # try:
            #     location_list = unicodedata.normalize(
            #         "NFKD",
            #         row.find(
            #             'div',
            #             {"class": re.compile("divCell EventDetails Location Header")}
            #         ).find_all("span", attrs={"class": False}).get_text().strip()
            #     ).split(',')
            #
            #     if len(location_list) > 0:
            #         tournament['location'] = location_list
            #     else:
            #         tournament['location'] = []
            # except AttributeError:
            #     tournament['location'] = []

            winner = row.find('div', {"class": re.compile("divCell Placement FirstPlace")})

            if winner:
                try:
                    winner_team = dict()
                    winner_span = winner.find(
                        "span",
                        {"class": re.compile("team-template-lightmode")}
                    )
                    team_short_name = winner.get_text().strip()
                    team_name = winner_span.a["title"]
                    team_logo_url = self.__image_base_url + winner_span.img["src"]
                    team_page = self.__image_base_url + winner_span.a["href"]

                    winner_team.update({
                        "name": team_name,
                        "short_name": team_short_name,
                        "logo": team_logo_url,
                        "page": team_page
                    })

                    tournament['winner'] = winner_team
                except AttributeError:
                    # 如果该场比赛取消，标注一下
                    winner_text = winner.get_text()
                    if winner_text == "Cancelled":
                        tournament["status"] = winner_text

                    tournament['winner'] = {}
            else:
                tournament['winner'] = {}

            runner_up = row.find(
                'div',
                {"class": re.compile("divCell Placement SecondPlace")}
            )
            if runner_up:
                try:
                    runner_up_team = dict()
                    runner_up_span = runner_up.find(
                        "span",
                        {"class": re.compile("team-template-lightmode")}
                    )

                    team_short_name = runner_up.get_text().strip()
                    team_name = runner_up_span.a["title"]
                    team_logo_url = self.__image_base_url + runner_up_span.img["src"]
                    team_page = self.__image_base_url + runner_up_span.a["href"]

                    runner_up_team.update({
                        "name": team_name,
                        "short_name": team_short_name,
                        "logo": team_logo_url,
                        "page": team_page
                    })

                    tournament['runner_up'] = runner_up_team
                except AttributeError:
                    tournament['runner_up'] = {}
            else:
                tournament['runner_up'] = {}

            tournaments.append(tournament)

        return tournaments

    def get_tournament_info(self, tournament_page):

        tournament_object = WildRiftTournament(tournament_page)
        soup, __ = self.liquipedia.parse(tournament_page)

        tournament = dict()
        tournament.update(
            {
                "page": f"{self.__image_base_url}/wildrift/{tournament_page}",
                "info": tournament_object.get_tournament_infobox(soup),
            }
        )
        tournament.update(tournament_object.get_overview(soup))
        tournament.update(tournament_object.get_format(soup))
        tournament.update(tournament_object.get_prize_pool(soup))
        tournament.update(tournament_object.get_participants(soup))

        return tournament
