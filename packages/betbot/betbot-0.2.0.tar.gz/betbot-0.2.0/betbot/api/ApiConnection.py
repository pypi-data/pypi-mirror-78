"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of betbot.

betbot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

betbot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with betbot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import json
import requests
import logging
from typing import List, Dict, Optional, Any
from base64 import b64encode
from betbot.api.Bet import Bet
from betbot.api.Match import Match


class ApiConnection:
    """
    Class that handles API calls to the bundesliga-tippspiel instance
    """

    def __init__(self, username: str, password: str, url: str):
        """
        Intitializes the API connection
        :param username: The username on bundesliga-tippspiel
        :param password: The password for that user
        :param url: The base url to the bundesliga-tippspiel instance
        """
        self.logger = logging.getLogger(__name__)
        self.username = username
        self.password = password
        self.url = os.path.join(url, "api/v2") + "/"
        self.api_key = ""
        self.login()

    @property
    def auth_headers(self) -> Dict[str, str]:
        """
        :return: Authorization headers for API calls
        """
        return {"Authorization": "Basic " + self.api_key}

    def login(self):
        """
        Retrieves an API Key using a username and password if no key
        has been retrieved yet or if the existing key has expired
        :return: None
        """
        if not self.authorized():
            self.logger.info("Requesting new API Key")
            creds = {"username": self.username, "password": self.password}
            data = self.execute_api_call("key", "POST", False, creds)
            api_key = data["data"]["api_key"]
            self.api_key = b64encode(api_key.encode("utf-8")).decode("utf-8")

    def authorized(self) -> bool:
        """
        Checks if the stored API key is valid
        :return: True if valid, False if not (for example because it expired)
        """
        data = self.execute_api_call("authorize", "GET", True)
        return data["status"] == "ok"

    def get_current_matchday_matches(self) -> List[Match]:
        """
        Retrieves a list of matches for the current matchday
        :return: The list of matches
        """
        data = self.execute_api_call("match?matchday=-1", "GET", True)
        return [Match.from_json(x) for x in data["data"]["matches"]]

    def place_bets(self, bets: List[Bet]):
        """
        Places a list of bets
        :param bets: The bets to place
        :return: None
        """
        bet_dict = {}
        for bet in bets:
            bet_dict.update(bet.to_dict())
        data = self.execute_api_call("bet", "PUT", True, bet_dict)
        if data["status"] != "ok":
            self.logger.error("Failed to place bets")
        else:
            new = data["data"]["new"]
            updated = data["data"]["updated"]
            self.logger.info(f"Placed bets ({new} new, {updated} updated) "
                             f"(user:{self.username})")

    def execute_api_call(
            self,
            endpoint: str,
            method: str,
            authorization_required: bool = False,
            json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes an API call
        :param endpoint: The API endpoint
        :param method: The request method
        :param authorization_required: Whether authoirzation is required
        :param json_data: The JSON data to send
        :return: The response JSON
        """
        if authorization_required and endpoint != "authorize":
            self.login()

        extras = {}
        if authorization_required:
            extras["headers"] = self.auth_headers
        if json_data is not None:
            extras["json"] = json_data

        resp = requests.request(method, self.url + endpoint, **extras)
        return json.loads(resp.text)
