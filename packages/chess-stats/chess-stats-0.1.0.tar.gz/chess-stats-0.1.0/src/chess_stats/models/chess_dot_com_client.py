from requests import Session

from typing import List
from .game import Game


class ChessDotComClient:
    """A client for the Chess.com API.

    Chess.com exposes a free JSON based REST API. The relevant endpoint for this project
    returns a list all of the games that a given user played in a month.
    """

    BASE_URL = "https://api.chess.com/pub"
    TIMEOUT = 10

    def __init__(self):
        self.client = Session()

    def fetch_games(self, username: str, year: int, month: int) -> List[Game]:
        """Query the Chess.com API for all games that the given user played in a given month.

        :param username: The Chess.com player's username
        :param year: The year of games to fetch
        :param month: The month of games to fetch
        :return: A list of Games
        """
        url = self.build_url(username, year, month)
        res = self.client.get(url, timeout=self.TIMEOUT)
        res.raise_for_status()
        res_json = res.json()
        games = [Game.from_json(game_json) for game_json in res_json["games"]]
        return games

    @classmethod
    def build_url(cls, username: str, year: int, month: int) -> str:
        """Build the request URL for fetching Chess.com games.

        Note that the Chess.com API expects a 2 digit month.

        :param username: The Chess.com player's username
        :param year: The year of games to fetch
        :param month: The month of games to fetch
        :return: A URL string
        """
        month_str = str(month) if month / 10 >= 1 else f"0{month}"
        return cls.BASE_URL + f"/player/{username}/games/{year}/{month_str}"
