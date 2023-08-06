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

from typing import Dict, Any


class Match:
    """
    Class that encapsulates information about a Match
    """

    def __init__(
            self,
            _id: int,
            matchday: int,
            home_team: str,
            away_team: str
    ):
        """
        Initializes the Match
        :param _id: The ID of the match
        :param matchday: The matchday of the match
        :param home_team: The name of the home team
        :param away_team: The name of the away team
        """
        self.id = _id
        self.matchday = matchday
        self.home_team = home_team
        self.away_team = away_team

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]):
        """
        Generates a Match object from JSON data
        :param json_data: The JSON data
        :return: The generated Match
        """
        return cls(
            json_data["id"],
            json_data["matchday"],
            json_data["home_team"]["abbreviation"],
            json_data["away_team"]["abbreviation"]
        )
