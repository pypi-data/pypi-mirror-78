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

import random
from typing import List
from betbot.api.Bet import Bet
from betbot.api.Match import Match
from betbot.prediction.Predictor import Predictor


class DrawPredictor(Predictor):
    """
    Class that always predicts 0:0, 1:1, 2:2 or 3:3
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the predictor
        """
        return "draw"

    def predict(self, matches: List[Match]) -> List[Bet]:
        """
        Performs the prediction
        :param matches: The matches to predict
        :return: The predictions as Bet objects
        """
        bets = []
        for match in matches:
            goals = random.randint(0, 3)
            bets.append(Bet(match.id, goals, goals))
        return bets
