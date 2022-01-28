from urllib.parse import quote
import unicodedata


class LeagueoflegendsTournament(object):

    def __init__(self, page):

        self.__image_base_url = "https://liquipedia.net"
        self.page = page

    def get_tournament_infobox(self, soup):

        tournament = {}
        try:
            image_url = soup.find("div", {"class": "infobox-image"}).find("img").get("src")
            tournament["image"] = self.__image_base_url + image_url
        except AttributeError:
            tournament["image"] = ""

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

                tournament[attribute.lower()] = value_list
            elif attribute == "Liquipedia Tier":
                tournament[attribute.lower().replace(" ", "_")] = \
                    info_boxes[i + 1].a.get_text().strip().replace("\xa0", " ")
            elif attribute == "Location":
                tournament[attribute.lower().replace(" ", "_")] = \
                    info_boxes[i + 1].get_text().strip().replace("\xa0", " ").split()
            elif attribute in ["Series", "Organizer", "Game Version", "Venue"]:
                # text = ""
                # values = info_boxes[i + 1].find_all("a")
                # for value in values:
                #     text += value.get_text().strip().replace("\xa0", " ")

                tournament[attribute.lower().replace(" ", "_")] = info_boxes[i + 1].get_text().strip().replace("\xa0", " ")
            elif attribute in ["Type", "Format", "Number of Teams", "Prize Pool", "Start Date", "End Date"]:
                tournament[attribute.lower().replace(" ", "_")] = \
                    info_boxes[i + 1].get_text().strip().replace("\xa0", " ")
            else:
                tournament[attribute.lower().replace(" ", "_")] = \
                    unicodedata.normalize("NFKD", info_boxes[i + 1].get_text().strip()).replace("\xa0", " ")

        return tournament

    def get_overview(self, soup):

        tournament = {}
        try:
            infobox_element = soup.find("div", {"class": "fo-nttax-infobox-wrapper infobox-dota2"})
            
        except AttributeError:
            tournament["overview"] = ""
