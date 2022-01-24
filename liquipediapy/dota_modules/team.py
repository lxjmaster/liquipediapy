import re
import itertools
import unicodedata
from urllib.parse import quote


class DotaTeam(object):

	def __init__(self):

		self.__image_base_url = 'https://liquipedia.net'

	@staticmethod
	def process_team_name(team_name):

		team_name = team_name.replace(" ", "_")
		team_name = quote(team_name)

		return team_name

	def get_team_infobox(self, soup):

		team = {}
		try:
			image_url = soup.find('div', class_='img-responsive').find('img').get('src')	
			team['image'] = self.__image_base_url+image_url
		except AttributeError:
			team['image'] = ''			
		info_boxes = soup.find_all('div', class_='infobox-cell-2')
		for i in range(0, len(info_boxes), 2):
			attribute = info_boxes[i].get_text().replace(':', '')
			if attribute == "Sponsor" or attribute == "Location":
				value_list = []
				values = info_boxes[i+1].find_all('a')
				for value in values:
					text = value.get_text()
					if len(text) > 0:
						value_list.append(text)
				team[attribute.lower()] = value_list
			elif attribute == "Total Earnings":
				team['earnings'] = int(info_boxes[i+1].get_text().replace('$', '').replace(', ', ''))
			# not available now
			#elif attribute == "Pro Circuit Rank":
			#	ranking = {}
			#	ranking_list = unicodedata.normalize("NFKD",info_boxes[i+1].get_text()).split()
			#	ranking['rank'] = ranking_list[0].replace('#', '')
			#	ranking['points'] = int(ranking_list[1].replace('(', '').replace(')', '').split(', ')[0])
			#	team['ranking'] = ranking			
			else:
				team[attribute.lower()] = unicodedata.normalize("NFKD",info_boxes[i+1].get_text().strip())

		return team

	@staticmethod
	def get_team_links(soup):
		
		team_links = {}
		try:		
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return team_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[-2].replace('https://', '')
			team_links[site_name] = link.get('href')

		return team_links

	@staticmethod
	def get_team_cups(soup):

		team_cups = []
		info_boxes = soup.find_all('div', class_='infobox-center')
		cups = []
		for boxes in info_boxes:
			cups.append(boxes.find_all('span', class_='league-icon-small-image'))
		cups = list(itertools.chain.from_iterable(cups))
		for cup in cups:
			try:
				league = cup.find('a').get('title')
				team_cups.append(league)
			except AttributeError:
				pass	

		return team_cups

	@staticmethod
	def get_team_roster(soup):

		roster_cards = soup.find_all('table', class_='roster-card')
		team_roster = roster_cards[0]
		rows = team_roster.find_all('tr')
		indexes = rows[1]
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(unicodedata.normalize("NFKD", cell.get_text().rstrip()))	
		rows = rows[2:]
		players = []
		for row in rows:
			player = {}
			cells = row.find_all('td')
			for i in range(0, len(cells)):
				key = index_values[i]
				value = cells[i].get_text().strip()
				if key == "Name":
					value = value.replace('(', '').replace(')', '')
				elif key == "Join Date":
					value = cells[i].find('div', class_="Date").find(text=True)	
				elif key == "Position":
					value = value.split()[-1]
				value = unicodedata.normalize("NFKD", value.rstrip())
				if len(key) > 0:
					player[key] = value
			players.append(player)	
		return players

	@staticmethod
	def get_team_achievements(soup):

		achievements = []
		rows = soup.find_all("tr")
		for row in rows:
			try:
				if len(row) == 8:
					match = {}
					attrs = {"style": "text-align:left"}
					icon = "results-team-icon"

					match["Date"] = row.find("td").get_text()
					place = row.find("font", class_="placement-text").get_text()
					match["Placement"] = re.sub("[A-Za-z]", "", place)
					match["Tier"] = row.find("a").get_text()
					match["Tournament"] = row.find("td", attrs).get_text()
					match["Results"] = row.find("td", class_="results-score").get_text()
					try:
						match["opponent"] = row.find("td", class_=icon).find("a")["title"]
					except TypeError:
						try:
							match["opponent"] = row.find("td", class_=icon).find("abbr")["title"]
						except:
							match["opponent"] = ""

					match["Prize"] = row.find_all("td", attrs)[1].get_text()

					for key, value in match.items():
						match[key] = unicodedata.normalize("NFKD", value)

					match["Placement"] = match["Placement"].replace(" ", "") 
					match["Results"] = match["Results"].replace(" ", "")

					achievements.append(match)
			except AttributeError:
				pass
			
		return achievements

