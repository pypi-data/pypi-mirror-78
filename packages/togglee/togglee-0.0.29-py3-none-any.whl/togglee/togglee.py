import time
import json
import threading
import requests


class Togglee:
    def __init__(self, url: str, refresh_rate: int, defaults: dict):
        self._url = url
        self._refresh_rate = refresh_rate
        self._toggles = defaults
        self._thread = threading.Thread(target=self._scheduler_event)
        self._thread.start()

    def is_enabled(self, prop: str):
        return self._toggles[prop] if self._toggles is not None and prop in self._toggles else False

    def _scheduler_event(self):
        self._refresh_toggles()
        while True:
            time.sleep(self._refresh_rate)
            self._refresh_toggles()

    def _refresh_toggles(self):
        response = requests.get(self._url)
        self._toggles = response.json()
