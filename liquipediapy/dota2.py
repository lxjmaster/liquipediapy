import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import Liquipediapy
import re
from liquipediapy.dota2_modules.player import dota_player
from liquipediapy.dota2_modules.team import DotaTeam
from liquipediapy.dota2_modules.pro_circuit import dota_pro_circuit
from liquipediapy.dota2_modules.tournament import Dota2Tournament
import unicodedata


class Dota2(object):

	def __init__(self):
		self.liquipedia = Liquipediapy('dota2')
		self.__image_base_url = 'https://liquipedia.net'

	def get_players(self):

		soup, __ = self.liquipedia.parse('Players_(all)')
		rows = soup.findAll('tr')
		indexes = rows[0]
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(cell.get_text().rstrip())
		players = []
		for row in rows:
			if len(row) > 3:
				player = {}
				cells = row.find_all('td')
				for i in range(0, len(cells)):
					key = index_values[i]
					if key == '':
						key = "country"
						value = cells[i].find('a').get('title')
					elif key == "Links":
						player_links = {}
						links = cells[i].find_all('a')
						for link in links:
							link_list = link.get('href').split('.')
							site_name = link_list[-2].replace('https://', '').replace('http://', '')
							player_links[site_name] = link.get('href')
						value = player_links	
					else:
						value = cells[i].get_text().rstrip()	
					player[key] = value
				if len(player) > 0:
					players.append(player)

		return players
	
	def get_player_info(self, playerName, results=False):

		player_object = dota_player()
		playerName = player_object.process_playerName(playerName)		
		soup, redirect_value = self.liquipedia.parse(playerName)
		if redirect_value is not None:
			playerName = redirect_value
		player = {}
		player['info'] = player_object.get_player_infobox(soup)
		player['links'] = player_object.get_player_links(soup)
		player['history'] = player_object.get_player_history(soup)
		player['achivements'] = player_object.get_player_achivements(soup)
		if results:
			parse_value = playerName + "/Results"
			try:
				soup,__ = self.liquipedia.parse(parse_value)
			except ex.RequestsException:
				player['results'] = []
			else:	
				player['results'] = player_object.get_player_achivements(soup)

		return player

	def get_teams(self):

		soup, __ = self.liquipedia.parse('Portal:Teams')
		teams = []
		templates = soup.find_all('span', class_="team-template-team-standard")
		for team in templates:
			teams.append(team.a['title'])
			
		return teams

	def get_team_info(self, teamName, results=False):

		team_object = DotaTeam()
		teamName = team_object.process_teamName(teamName)	
		soup, redirect_value = self.liquipedia.parse(teamName)
		if redirect_value is not None:
			teamName = redirect_value
		team = {}	
		team['info'] = team_object.get_team_infobox(soup)
		team['links'] = team_object.get_team_links(soup)
		team['cups'] = team_object.get_team_cups(soup)
		team['team_roster'] = team_object.get_team_roster(soup)
		if results:
			parse_value = teamName + "/Results"
			try:
				soup, __ = self.liquipedia.parse(parse_value)
				team['results'] = team_object.get_team_achievements(soup)
			except ex.RequestsException:
				team['results'] = []
		else:
			team['results'] = team_object.get_team_achievements(soup)

		return team	

	def get_transfers(self):

		transfers = []
		soup, __ = self.liquipedia.parse('Portal:Transfers')
		indexes = soup.find('div', class_='divHeaderRow')
		index_values = []
		for cell in indexes.find_all('div'):
			index_values.append(cell.get_text())
		rows = soup.find_all('div', class_='divRow')
		for row in rows:
			transfer = {}
			cells = row.find_all('div', class_='divCell')
			for i in range(0, len(cells)):
				key = index_values[i]
				value = cells[i].get_text()
				if key == "Player":
					value = [val for val in value.split(' ') if len(val) > 0]
				if key == "Previous" or key == "Current":
					try:
						value = cells[i].find('a').get('title')
					except AttributeError:
						value = "None"
				transfer[key] = value
			transfer = {k: v for k, v in transfer.items() if len(k) > 0}	
			transfers.append(transfer)	

		return transfers	

	def get_upcoming_and_ongoing_games(self):

		games = []
		soup, __ = self.liquipedia.parse('Liquipedia:Upcoming_and_ongoing_matches')
		matches = soup.find_all('table', class_='infobox_matches_content')
		for match in matches:
			game = {}
			cells = match.find_all('td')
			try:
				game['team1'] = cells[0].find('span', class_='team-template-image').find('a').get('title')
				game['format'] = cells[1].find('abbr').get_text()
				game['team2'] = cells[2].find('span', class_='team-template-image').find('a').get('title')
				game['start_time'] = cells[3].find('span', class_="timer-object").get_text()
				game['tournament'] = cells[3].find('div').a['title']
				game['tournament_short_name'] = cells[3].find('div').get_text().rstrip()
				try:
					game['twitch_channel'] = cells[3].find('span', class_="timer-object").get('data-stream-twitch')
				except AttributeError:
					pass
				games.append(game)	
			except AttributeError:
				continue		
					
		return games	

	def get_heroes(self):

		heroes = []
		soup, __ = self.liquipedia.parse('Portal:Heroes')
		list_elements = soup.find_all('li')
		for list_element in list_elements:
			hero = {}
			try:
				hero['image'] = self.__image_base_url + list_element.find('img').get('src')
				hero['name'] = list_element.find('span').get_text()
				heroes.append(hero)
			except AttributeError:
				pass

		return heroes

	def get_items(self):

		items = []							
		soup, __ = self.liquipedia.parse('Portal:Items')
		item_divs = soup.find_all('div', class_='responsive')
		for item_div in item_divs:
			item = {}
			item['image'] = self.__image_base_url + item_div.find_all('img')[0].get('src')
			item['name'] = item_div.find_all('a')[1].get_text()
			try:
				item['price'] = item_div.find('b').get_text()
			except AttributeError:
				pass	
			items.append(item)	

		return items

	def get_patches(self):

		patches = []
		soup, __ = self.liquipedia.parse('Portal:Patches')
		tables = soup.find_all('table')	
		for table in tables:
			rows = table.find('tbody').find_all('tr')
			indexes = rows[0]
			index_values = []
			for cell in indexes.find_all('td'):
				index_values.append(cell.get_text().rstrip())
			rows = rows[1:]
			for row in rows:
				patch = {}
				cells = row.find_all('td')
				for i in range(0, len(cells)):
					key = index_values[i]
					value = cells[i].get_text().rstrip()
					if key == "Highlights":
						value = [unicodedata.normalize("NFKD",val) for val in cells[i].get_text().split('\n') if len(val) > 0]
					patch[key] = value
				patches.append(patch)

		return patches		

	def get_tournaments(self, tournament_type=None):

		tournaments = []
		if tournament_type is None:
			page_val = 'Portal:Tournaments'
		elif tournament_type == 'Show Matches':
			page_val = 'Show_Matches'
		elif tournament_type == "Recent Results":
			page_val = "Recent_Tournament_Results"
		else:
			page_val = tournament_type.capitalize() + '_Tournaments'
		soup, __ = self.liquipedia.parse(page_val)
		div_rows = soup.find_all('div', {"class": "divRow"})
		for row in div_rows:
			tournament = {"status": "Normal"}
			values = row.find('div', class_="divCell Tournament Header")
			if tournament_type is None:
				tournament['tier'] = values.a.get_text()
				tournament['name'] = values.b.get_text()
			else:
				tournament['tier'] = tournament_type

			try:
				tournament['logo'] = self.__image_base_url + row.find('div', {"class": "divCell Tournament Header"}).find('img').get('src')
			except AttributeError:
				tournament['logo'] = ""

			try:
				tournament['page'] = self.__image_base_url + values.b.a['href']
			except AttributeError:
				tournament['page'] = ""

			try:
				tournament['date'] = row.find('div', {"class": "divCell EventDetails Date Header"}).get_text().strip()
			except AttributeError:
				tournament['date'] = ""

			try:
				tournament['prize'] = row.find(
					'div',
					{"class": re.compile("divCell EventDetails Prize Header")}).get_text().rstrip()
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

			# location_list = unicodedata.normalize(
			# 	"NFKD",
			# 	row.find(
			# 		'div',
			# 		{"class": "divCell EventDetails Location Header"}
			# 	).get_text().strip()).split(',')
			# tournament['host_location'] = location_list[0]

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

		tournament_object = Dota2Tournament(tournament_page)
		soup, __ = self.liquipedia.parse(tournament_page)

		tournament = dict()
		tournament.update(
			{
				"page": f"{self.__image_base_url}/dota2/{tournament_page}",
				"info": tournament_object.get_tournament_infobox(soup),
			}
		)
		tournament.update(tournament_object.get_overview(soup))
		tournament.update(tournament_object.get_format(soup))
		tournament.update(tournament_object.get_prize_pool(soup))
		tournament.update(tournament_object.get_participants(soup))

		return tournament

	def get_tournament_banner(self, tournament_page):

		try:
			page, __ = self.liquipedia.parse(tournament_page.replace('https://liquipedia.net/dota2/', ''))
			
			return f"https://liquipedia.net{page.find('div', class_='infobox-image').div.div.a.img['src']}"

		except AttributeError:
			pass

	def get_pro_circuit_details(self):

		soup, __ = self.liquipedia.parse('Dota_Pro_Circuit/2018-19/Rankings/Full')
		pro_circuit = {}
		circuit_object = dota_pro_circuit()
		pro_circuit['rankings'] = circuit_object.get_rankings(soup)
		soup, __ = self.liquipedia.parse('Dota_Pro_Circuit/2018-19/Schedule')
		pro_circuit['schedule'] = circuit_object.get_schedule(soup)

		return pro_circuit
