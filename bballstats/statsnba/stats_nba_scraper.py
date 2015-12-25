__author__ = 'ahmedlawi92@gmail.com'

import json
import requests
import url_constants

class NBAStatsScraper:

    player_ids = {}

    def __init__(self):
        self.populate_players_dict()

    def get_player_tracking_stats(self, **kwargs):
        base, args = self.build_url(url_constants.player_tracking_url)
        self.update_options(args, kwargs)
        response = requests.get(base, args)
        return self.extract_data(response)


    def get_player_shot_tracking_stats(self, **kwargs):
        base, args = self.build_url(url_constants.player_shot_tracking)
        self.update_options(args, kwargs)
        response = requests.get(base, args)
        return self.extract_data(response)

    def get_team_shot_tracking_stats(self, **kwargs):
        base, args = self.build_url(url_constants.team_shot_tracking)
        self.update_options(args, kwargs)
        response = requests.get(base, args)
        return self.extract_data(response)

    def get_lineup_stats(self, **kwargs):
        base, args = self.build_url(url_constants.team_lineups)
        self.update_options(args, kwargs)
        response = requests.get(base, args)
        return self.extract_data(response)

    def get_player_shot_chart_data(self, player, **kwargs):
        kwargs['PlayerID'] = self.player_ids[player.lower()]
        base, args = self.build_url(url_constants.shot_chart_url)
        self.update_options(args, kwargs)
        response = requests.get(base, args)
        return self.extract_data(response)

    def get_player_list(self):
        base, args = self.build_url(url_constants.player_list_url)
        response = requests.get(base, args)
        return self.extract_data(response)

    def extract_data(self, response):
        data = json.loads(response.content)['resultSets'][0]
        header = data['headers']
        return [dict(zip(header, row)) for row in data['rowSet']]

    def build_url(self, url):
        x = url.split('?', 2)
        base = x[0]
        args = {i.split('=')[0] : i.split('=')[1].replace('+', ' ') for i in x[1].split("&")}
        return base, args

    def update_options(self, args, options):
        for key in options.keys():
            if key in args.keys():
                args[key] = options[key]

    def populate_players_dict(self):
        players = self.get_player_list()
        for player in players:
            self.player_ids[player['DISPLAY_LAST_COMMA_FIRST'].lower()] = player['PERSON_ID']

