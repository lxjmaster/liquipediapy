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

    @staticmethod
    def get_overview(soup):

        tournament = {}
        try:
            p_list = []
            infobox_element = soup.find("div", {"class": "fo-nttax-infobox-wrapper infobox-dota2"})
            overview_elements = infobox_element.next_siblings
            for index, overview_element in enumerate(overview_elements):
                if overview_element.name is not None:
                    if index == 1 and overview_element.name != "p":
                        break
                    else:
                        if overview_element.name == "p":
                            p_list.append(overview_element)
                        else:
                            break

            overview_text = [p.get_text().strip().replace("\ax0", " ") for p in p_list]
            tournament["overview"] = "\n".join(overview_text)
        except AttributeError:
            tournament["overview"] = ""

        return tournament

    def get_format(self, soup):

        tournament = {}
        try:
            format_list = []
            format_title = soup.find("span", {"id": "Format"}).parent
            format_elements = format_title.next_siblings
            for format_element in format_elements:
                if format_element.name is not None:
                    if format_element.name in ["h1", "h2", "h3", "h4", "div"]:
                        break
                    else:
                        format_list.append(format_element)

            format_text = "\n".join([text.get_text() for text in format_list])
            tournament["format"] = format_text
        except AttributeError:
            tournament["format"] = ""

        return tournament


