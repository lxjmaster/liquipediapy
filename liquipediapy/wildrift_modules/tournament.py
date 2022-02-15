import re
import unicodedata
from bs4 import BeautifulSoup


class WildRiftTournament(object):

    def __init__(self, page):

        self.__image_base_url = "https://liquipedia.net"
        self.page = page

    def get_tournament_infobox(self, soup):
        """
        获取infobox的数据
        :param soup:
        :return:
        """

        tournament = {}
        try:
            image_url = soup.find("div", {"class": "infobox-image"}).find("img").get("src")
            tournament["image"] = self.__image_base_url + image_url
        except AttributeError:
            tournament["image"] = ""

        info_boxes = soup.find_all("div", {"class": "infobox-cell-2"})
        for i in range(0, len(info_boxes), 2):
            attribute = info_boxes[i].get_text().replace(":", "")
            if attribute in ["Sponsor", "Sponsor(s)"]:
                value_list = []
                values = info_boxes[i+1].find_all("a")
                for value in values:
                    value_list.append({
                        "name": value.get_text().strip(),
                        "url": value["href"]
                    })

                if attribute == "Sponsor(s)":
                    attribute = "Sponsor"

                tournament[attribute.lower()] = value_list
            elif attribute in ["Liquipedia Tier", "Pro Circuit Tier"]:
                tournament[attribute.lower().replace(" ", "_")] = \
                    info_boxes[i + 1].a.get_text().strip().replace("\xa0", " ")
            elif attribute == "Location":
                tournament[attribute.lower().replace(" ", "_")] = \
                    [value for value in info_boxes[i + 1].get_text().strip().replace("\xa0", " ").split(" ") if value]
            elif attribute in ["Venue", "Format"]:
                new_soup = BeautifulSoup(str(info_boxes[i+1]).replace("<br/>", "\n"), "lxml")
                tournament[attribute.lower().replace(" ", "_")] = new_soup.get_text().strip().replace("\xa0", " ")
            elif attribute in ["Organizer", "Organizers"]:

                if attribute == "Organizers":
                    attribute = "Organizer"

                values = info_boxes[i+1].find_all("a")

                if len(values) > 0:
                    tournament[attribute.lower().replace(" ", "_")] = [
                        value.get_text().strip().replace("\xa0", " ") for value in values
                    ]
                else:
                    new_soup = BeautifulSoup(str(info_boxes[i+1]).replace("<br/>", "\n"), "lxml")
                    tournament[attribute.lower().replace(" ", "_")] = new_soup.get_text().split("\n")
            elif attribute in ["Series", "Game Version"]:
                tournament[attribute.lower().replace(" ", "_")] = info_boxes[i + 1].get_text().strip().replace("\xa0", " ")
            elif attribute in ["Type", "Number of Teams", "Prize Pool", "Start Date", "End Date"]:
                tournament[attribute.lower().replace(" ", "_")] = \
                    info_boxes[i + 1].get_text().strip().replace("\xa0", " ")
            else:
                try:
                    tournament[attribute.lower().replace(" ", "_")] = \
                        unicodedata.normalize("NFKD", info_boxes[i + 1].get_text().strip()).replace("\xa0", " ")

                except IndexError:
                    pass

        return tournament

    @staticmethod
    def get_overview(soup):
        """
        获取简介
        :param soup:
        :return:
        """

        tournament = {}
        try:
            p_list = []
            infobox_elements = soup.find_all("div", {"class": "fo-nttax-infobox-wrapper"})
            if len(infobox_elements) > 0:
                infobox_element = infobox_elements[-1]
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
                tournament["overview"] = re.sub(r"\[[(\d+)(\w+)]+\]", "", "\n".join(overview_text))
            else:
                tournament["overview"] = ""
        except AttributeError:
            tournament["overview"] = ""

        return tournament

    @staticmethod
    def get_format(soup):
        """
        获取赛制
        :param soup:
        :return:
        """

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
                        format_element = BeautifulSoup(str(format_element).replace("<br/>", "\n"), "lxml")
                        format_list.append(format_element)

            format_text = "\n".join([text.get_text() for text in format_list])
            tournament["format"] = format_text
        except AttributeError:
            tournament["format"] = ""

        return tournament

    def get_prize_pool(self, soup):
        """
        获取奖金池
        :param soup:
        :return:
        """

        tournament = {}
        try:
            titles = []
            tables = []
            logos = []

            # 奖金池表格
            prize_pool_table_element = soup.find("table", {"class": "table table-bordered prizepooltable collapsed"})

            # 队伍的logo链接
            logo_elements = prize_pool_table_element.find_all("span", {"class": "team-template-lightmode"})
            for logo_element in logo_elements:
                logos.append(self.__image_base_url + logo_element.a.img["src"])

            prize_pool_table_rows = prize_pool_table_element.find_all("tr")

            # 先获取表头
            table_title_element = prize_pool_table_rows[0]
            for table_title in table_title_element:
                if table_title.name is not None:
                    title = list(table_title.stripped_strings)
                    titles.append("".join(title))

            # 表格数据
            table_rows = []
            for table_row in prize_pool_table_rows[1:]:
                row = []
                cells = table_row.find_all("td")
                for cell in cells:
                    if cell.find("img", {"src": re.compile("GreenCheck.png")}):
                        row.append("晋级")
                    else:
                        row.append("".join(list(cell.stripped_strings)))

                table_rows.append(row)

            for table_row in table_rows:
                if len(table_row) == len(titles):
                    tables.append(table_row)
                else:
                    if len(table_row) == 1:
                        tables.append(tables[-1][:-1] + table_row)
                    elif 0 < len(titles) - len(table_row) < len(titles):
                        tmp_list = ["-"] * (len(titles) - len(table_row))
                        tmp_list.append(table_row.pop())
                        tables.append(table_row + tmp_list)
                    else:
                        raise ValueError("奖池解析错误")

            tournament["prize_pool"] = {
                "titles": titles,
                "tables": tables,
                "team_logos": logos
            }
        except AttributeError:
            tournament["prize_pool"] = {}

        return tournament

    def get_participants(self, soup):
        """
        获取参赛队伍
        :param soup:
        :return:
        """

        tournament = {}
        try:
            teams = []
            team_card_elements = soup.find_all("div", {"class": "teamcard toggle-area toggle-area-1"})
            for team_card_element in team_card_elements:
                team_name_element_a = team_card_element.center.find_all("a")
                team_name_element = [element for element in team_name_element_a if not element.find("img")]
                if len(team_name_element) == 1:
                    team_name_element = team_name_element[0]
                    team_name = team_name_element.get_text()
                    try:
                        team_logo = self.__image_base_url + team_card_element.find("span", {"class": "logo-lightmode"}).img["src"]
                    except TypeError:
                        team_logo = ""

                    teams.append({
                        "team_name": team_name,
                        "team_logo": team_logo
                    })

                tournament["participants"] = teams
        except AttributeError:
            tournament["participants"] = []

        return tournament


