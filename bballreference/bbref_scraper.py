__author__ = 'ahmedlawi92@gmail.com'

import json
import string
from enum import Enum
from bs4 import BeautifulSoup
import requests

class BBRefScraper:

    __base_url = 'http://www.basketball-reference.com{s}'
    __url_key = 'info_page'


    def __init__(self, json_file):
        self.players = json.load(file(json_file))

    def get_table(self, player, table_type):
        player_url = self.players[player][self.__url_key]
        page = requests.get(self.__base_url.format(s=player_url))
        soup = BeautifulSoup(page.content, 'html.parser')
        return self.__scrape_table(soup.find('table', id=table_type.value))

    def __scrape_table(self, table):
        columns =  [col.string for col in table.find_all('th')]
        stats = [{columns[i]: self.__format_line(cell) for i, cell in enumerate(row.find_all("td"))} for row in table.tbody.find_all('tr')]
        return stats

    def __format_line(self, v):
        t = v.a.string if v.a is not None else v.string
        if t is None:
            return t
        try:
            t = float(t)
            return t
        except ValueError:
            return t

class TableTypes(Enum):
    TOTALS = 'totals'
    ADVANCED = 'advanced'
    SHOOTING = 'shooting'
    POSSESSION = 'per_poss'
    PER_GAME =  'per_game'
    PER_36 = 'per_minute'


def create_players_info_json():
    base_url  = "http://www.basketball-reference.com/players/{s}"
    players = {}
    letters = string.ascii_lowercase

    for letter in letters:
        page = requests.get(base_url.format(s=letter))
        soup = BeautifulSoup(page.content, 'html.parser')
        player_table = soup.find(id="players")
        if player_table is None:
            continue
        columns =  [col.string for col in player_table.find_all('th')]
        for player_data in player_table.tbody.find_all('tr'):
            name = player_data.td.a.string
            players[name] = {columns[i]: cell.string for i, cell in enumerate(player_data.find_all("td"))}
            players[name]["info_page"] = player_data.td.a['href']

    f = open('players_info.json', 'w')
    f.write(json.dumps(players, sort_keys=True, indent=4))
    f.close
