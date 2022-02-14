import time

import liquipediapy.exceptions as ex
from core.db import RedisObject
from urllib.parse import quote
from core.config import Config
from bs4 import BeautifulSoup
import requests
import json


class Response(object):

	def __init__(self, resource, status_code=200):

		self.resource = resource
		self.__status_code = status_code

	@property
	def status_code(self):

		return self.__status_code

	def json(self):

		return json.loads(self.resource)


class Request(object):

	def __init__(self, url, headers=None):

		self.config = Config()
		self.url = url
		self.headers = headers if headers else {
			"Host": "liquipedia.net",
			"Origin": "https://liquipedia.net",
			"Referer": "https://liquipedia.net//leagueoflegends/Special:ApiSandbox",
			"accept-language": "zh-CN,zh;q=0.9",
			'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
			'Accept-Encoding': 'gzip, deflate, br'
		}

	def get(self):

		try:
			getattr(self.config, "redis_caches")
			redis_client = RedisObject()
			cache = redis_client.client.get(f"url:{self.url.replace('https://', '')}")
			if cache is not None:
				response = Response(cache, 201)
			else:
				response = requests.get(self.url, headers=self.headers)
				redis_client.client.set(f"url:{self.url.replace('https://', '')}", response.text, ex=7 * 24 * 60 * 60)
				self.delay()
		except AttributeError:
			response = requests.get(self.url, headers=self.headers)
			self.delay()

		return response

	def delay(self):
		"""
		Delay request time why mediawiki api blocks ip addresses.
		:return:
		"""

		if hasattr(self.config, "debug") and getattr(self.config, "debug") == "False":
			if hasattr(self.config, "delay_time"):
				time.sleep(getattr(self.config, "delay_time"))


class Liquipediapy(object):

	def __init__(self, game):

		self.game = game
		self.__base_url = 'https://liquipedia.net/' + game + '/api.php?'

	def parse(self, page):

		url = self.__base_url + 'action=parse&format=json&page=' + page
		response = Request(url).get()
		# response = requests.get(url, headers=self.__headers)
		if response.status_code in [200, 201]:
			try:
				page_html = response.json()['parse']['text']['*']
			except KeyError:
				raise ex.RequestsException(response.json(), response.status_code)
			soup = BeautifulSoup(page_html, features="lxml")
			redirect = soup.find('ul', class_="redirectText")
			if redirect is None:
				return soup, None
			else:
				redirect_value = soup.find('a').get_text()
				redirect_value = quote(redirect_value)
				soup, __ = self.parse(redirect_value)
				return soup, redirect_value
		else:
			raise ex.RequestsException(response.json(), response.status_code)

	def dota2webapi(self, matchId):

		if self.game == 'dota2':
			url = self.__base_url + 'action=dota2webapi&data=picks_bans|players|kills_deaths|duration|radiant_win|teams|start_time&format=json&matchid=' + matchId
			response = Request(url).get()
			# response = requests.get(url, headers=self.__headers)
			if response.status_code in [200, 201]:
				res = response.json()
				if res['dota2webapi']['isresult'] >= 1:
					return res['dota2webapi']['result']
				else:
					return res['dota2webapi']['result']['error']
			else:
				raise ex.RequestsException(response.json(), response.status_code)
		else:
			raise ex.RequestsException('set game as dota2 to access this api', 0)

	def search(self, serachValue):

		url = self.__base_url + 'action=opensearch&format=json&search=' + serachValue
		response = Request(url).get()
		# response = requests.get(url, headers=self.__headers)
		if response.status_code in [200, 201]:
			return response.json()
		else:
			raise ex.RequestsException(response.json(), response.status_code)
