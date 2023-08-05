import threading
import time

import requests


def release_strategy(toggle, _):
    return toggle['value']


strategy_maps = {
    'release': release_strategy
}


class Togglee:
    def __init__(self, url: str, refresh_rate: int, defaults: dict):
        self._url = url
        self._refresh_rate = refresh_rate
        self._toggles = defaults
        self._thread = threading.Thread(target=self._scheduler_event)
        self._thread.start()

    def is_enabled(self, prop: str, context=None):
        return self._get_value(prop, context) if self._toggles is not None and prop in self._toggles else False

    def _get_value(self, prop, context):
        toggle = self._toggles[prop]
        return strategy_maps[toggle['type']](toggle, context)

    def _scheduler_event(self):
        self._refresh_toggles()
        while True:
            time.sleep(self._refresh_rate)
            self._refresh_toggles()

    def _map_json_to_toggles(self, json_toggles):
        mapped_toggles = {}
        for toggle in json_toggles['toggles']:
            mapped_toggles[toggle['name']] = toggle
            mapped_toggles[toggle['name']].pop('name')
        return mapped_toggles

    def _refresh_toggles(self):
        response = requests.get(self._url)
        self._toggles = self._map_json_to_toggles(response.json())
