class AnnualSummary:
    """A summary of player's chess statistics for the year.
    """

    def __init__(self, year: int, wins: int, losses: int, draws: int) -> None:
        self.year = year
        self.wins = wins
        self.losses = losses
        self.draws = draws
