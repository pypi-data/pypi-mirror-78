class Player:
    """A player in a chess game.
    """

    def __init__(self, rating=None, username=None, result=None) -> None:
        self.rating = rating
        self.username = username
        self.result = result
