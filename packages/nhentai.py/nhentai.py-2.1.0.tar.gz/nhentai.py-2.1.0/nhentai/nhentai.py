from collections import namedtuple
from typing import List
from enum import Enum
import requests

_TYPE_TO_EXTENSION = { 
	'j' : 'jpg',
	'p' : 'png',
	'g' : 'gif'
}

class Doujin():
	"""
	Class representing a doujin.

	:ivar int id:			Doujin id.
	:ivar dict titles:		Doujin titles (language:title).
	:ivar Doujin.Tag tags:	Doujin tag list.
	:ivar str cover:		Doujin cover image url.
	:ivar str thumbnail:	Doujin thumbnail image url.
	"""
	Tag = namedtuple("Tag", ["id", "type", "name", "url", "count"])

	def __init__(self, data):
		self.id = data["id"]
		self.media_id = data["media_id"]
		self.titles = data["title"]
		images = data["images"]

		self.pages = [Doujin.Page(self.media_id, num, **_) for num, _ in enumerate(images["pages"], start=1)]
		self.tags = [Doujin.Tag(**_) for _ in data["tags"]]

		thumb_ext = _TYPE_TO_EXTENSION[images["thumbnail"]["t"]]
		self.thumbnail = f"https://t.nhentai.net/galleries/{self.media_id}/thumb.{thumb_ext}"

		cover_ext = _TYPE_TO_EXTENSION[images["cover"]["t"]]
		self.cover = f"https://t.nhentai.net/galleries/{self.media_id}/cover.{cover_ext}"

	def __getitem__(self, key:int):
		"""
		Returns a page by index.

		:rtype: Doujin.Page 
		"""
		return self.pages[key]

	class Page():
		def __init__(self, media_id:int, num:int, t:str, w:int, h:int):
			self.width = w
			self.height = h
			self.url = f"https://i.nhentai.net/galleries/{media_id}/{num}.{_TYPE_TO_EXTENSION[t]}"

_SESSION = requests.Session()

def _get(endpoint, params={}):
	return _SESSION.get("https://nhentai.net/api/" + endpoint, params=params).json()

def search(query:str, page:int=1, sort_by:str="date") -> List[Doujin]:
	"""
	sSearch doujins by keyword.

	:param str query: Search term. (https://nhentai.net/info/)
	:param int page: Page number. Defaults to 1.
	:param str sort_by: Method to sort search results by (popular/date). Defaults to date.

	:returns list[Doujin]: Search results parsed into a list of nHentaiDoujin objects
	"""
	galleries = _get('galleries/search', {"query" : query, "page" : page, "sort" : sort_by})["result"]
	results = []
	for d in galleries:
		results.append(Doujin(d))
	return results

def search_tagged(tag_id:int, page:int=1, sort_by:str="date") -> List[Doujin]:
	"""
	Search doujins by tag id.

	:param int tag_id: Tag id to use.
	:param int page: Page number. Defaults to 1.
	:param str sort_by: Method to sort search results by (popular/date). Defaults to date.

	:returns list[Doujin]: Search results parsed into a list of nHentaiDoujin objects
	"""
	try:
		galleries = _get('galleries/tagged', {"tag_id" : tag_id, "page" : page, "sort" : sort_by})["result"]
	except KeyError:
		raise ValueError("There's no tag with the given tag_id.")
	
	results = []
	for d in galleries:
		results.append(Doujin(d))
	return results

def get_homepage(page:int=1) -> List[Doujin]:
	"""
	Get recently uploaded doujins from the homepage.

	:param int page: Page number. Defaults to 1.

	:returns list[Doujin]: Search results parsed into a list of nHentaiDoujin objects
	"""
	results = []
	for d in _get('galleries/all', {"page" : page})["result"]:
		results.append(Doujin(d))
	return results

def get_doujin(id:int) -> Doujin:
	"""
	Get a doujin by its id.

	:param int id: A doujin's id.

	:rtype: Doujin
	"""
	try:
		return Doujin(_get('gallery/%d' % id))
	except KeyError:
		raise ValueError("A doujin with the given id wasn't found")

def get_random_id() -> int:
	"""
	Get an id of a random doujin.

	:returns int: A random existing doujin id.
	"""
	redirect = _SESSION.head("https://nhentai.net/random/").headers["Location"]
	return int(redirect[3:-1])

