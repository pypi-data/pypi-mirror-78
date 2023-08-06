from typing import Any, Dict

import requests

from ._lib import ObjectSetter


class ObjJson(ObjectSetter):
    """
    Calls a url, parses the json it gets and returns the dictionary
    Uses the existing object data as http request parameter.

    Attribute key: jsonsetter

    Configuration:
        - **url**: the url to be called, mandatory
    """
    name = "jsonsetter"

    def __init__(self, cfg: Dict) -> None:
        self.cfg = cfg

    def run(self, data: Dict) -> Any:
        resp = requests.get(url=self.cfg['url'], params=data)
        resp_data = resp.json()
        data.update(resp_data)
        return data
