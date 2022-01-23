from urllib.parse import quote
import re
import itertools
import unicodedata


class LeagueoflegendsTeam(object):

    def __init__(self, name):

        self.__image_base_url = "https://liquipedia.net"
        self.name = name

    @staticmethod
    def process_team_name(team_name):

        team_name = team_name.replace(" ", "_")
        team_name = quote(team_name)

        return team_name

    def get_team_infobox(self, soup):

        team = {}
        try:
            image_url = soup.find("div", {"class": "infobox-image"}).find("img").get("src")
            team["image"] = self.__image_base_url + image_url
        except AttributeError:
            team["image"] = ""

        info_boxes = soup.find_all("div", {"class": "infobox-cell-2"})
        for i in range(0, len(info_boxes), 2):
            attribute = info_boxes[i].get_text().replace(":", "")
            if attribute == "Sponsor":
                value_list = []
                values = info_boxes[i+1].find_all("a")
                for value in values:
                    value_list.append({
                        "name": value.get_text().strip(),
                        "url": value["href"]
                    })

                team[attribute.lower()] = value_list
            elif attribute in ["Location", "Region"]:
                values = info_boxes[i+1].find_all("a")
                for value in values:
                    team[attribute.lower()] = value.get_text().strip()
            elif attribute in ["City", "Total Earnings"]:
                team[attribute.lower()] = info_boxes[i+1].get_text().strip()
            elif attribute in ["Coaches", "Manager"]:
                values = info_boxes[i+1].get_text().split(",")
                if len(values) > 0:
                    team[attribute.lower()] = list(map(lambda item: item.strip(), values))
            else:
                team[attribute.lower()] = unicodedata.normalize("NFKD", info_boxes[i + 1].get_text().strip())

        return team

    @staticmethod
    def get_team_links(soup):

        team_links = []

        try:
            links = soup.find("div", {"class": "infobox-icons"}).find_all("a")
        except AttributeError:
            return team_links

        for link in links:
            team_links.append({
                "name": link.i["class"][-1].split("-")[-1],
                "link": link["href"]
            })

        return team_links

    @staticmethod
    def has_history_link(soup, value):

        history_link = False
        link = soup.find_all("a", {"title": value})
        if len(link) > 0:
            history_link = True

        return history_link

    def get_history(self, soup):

        history_title = soup.find("span", {"id": "History"})
        if history_title:
            history = history_title.parent
