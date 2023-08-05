from typing import Dict, Optional
from src.chess_stats.models.player import Player


class Game:
    """A chess game result.
    """

    def __init__(
        self,
        url=None,
        pgn=None,
        time_control=None,
        end_time=None,
        is_rated=None,
        fen=None,
        time_class=None,
        rules=None,
        white_player=None,
        black_player=None,
    ) -> None:
        white_player = Player() if white_player is None else white_player
        black_player = Player() if black_player is None else black_player
        self.url = url
        self.pgn = pgn
        self.time_control = time_control
        self.time_class = time_class
        self.end_time = end_time
        self.is_rated = is_rated
        self.fen = fen
        self.rules = rules
        self.white_player = white_player
        self.black_player = black_player

    @property
    def winning_player(self) -> Optional[Player]:
        """Get the winner of the game.

        :return: The winning player or None if the result was a draw or stalemate.
        """
        if self.white_player.result == "win":
            return self.white_player
        elif self.black_player.result == "win":
            return self.black_player
        else:
            return None

    @property
    def losing_player(self) -> Optional[Player]:
        """Get the loser of the game.

        :return: The losing player or None if the result was a draw or stalemate.
        """
        winner = self.winning_player
        if winner is None:
            return None
        return (
            self.white_player
            if winner.username == self.black_player.username
            else self.black_player
        )

    @staticmethod
    def from_json(game_json: Dict[str, str]) -> "Game":
        """Create a GameResult instance from a JSON representation.

        :param game_json: The game JSON deserialized into a dictionary.
        :return: A GameResult object instantiated with the JSON data.
        """
        white_result = game_json["white"]["result"]
        white_username = game_json["white"]["username"]
        white_rating = game_json["white"]["rating"]
        black_result = game_json["black"]["result"]
        black_username = game_json["black"]["username"]
        black_rating = game_json["black"]["rating"]

        white_player = Player(
            username=white_username, rating=white_rating, result=white_result
        )
        black_player = Player(
            username=black_username, rating=black_rating, result=black_result
        )

        game = Game(
            url=game_json["url"],
            pgn=game_json["pgn"],
            time_control=game_json["time_control"],
            time_class=game_json["time_class"],
            end_time=game_json["end_time"],
            is_rated=game_json["rated"],
            fen=game_json["fen"],
            rules=game_json["rules"],
            white_player=white_player,
            black_player=black_player,
        )
        return game
