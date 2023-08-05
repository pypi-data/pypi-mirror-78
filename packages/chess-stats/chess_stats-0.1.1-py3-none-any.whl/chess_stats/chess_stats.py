from typing import List, Dict
from datetime import datetime
from chess_stats.models import ChessDotComClient, AnnualSummary, Game


def fetch_games_for_year(username: str, year: int) -> List[Game]:
    """Query the Chess.com API for all games that the given user played in a given year.

    :param username: The Chess.com player's username
    :param year: The year of games to fetch
    :return: A list of Games
    """
    if not isinstance(year, int):
        raise ValueError("Year must an integer")
    num_months = datetime.now().month if year == datetime.now().year else 12
    cdc = ChessDotComClient()
    games = []
    for month in range(1, num_months + 1):
        games.extend(cdc.fetch_games(username, year, month))
    return games


def create_annual_summary(username: str, year: int) -> AnnualSummary:
    """Create an annual summary of a Chess.com user's games.

    :param username: The Chess.com player's username
    :param year: The year of games to fetch
    :return: A summary of the player's games
    """
    games = fetch_games_for_year(username, year)
    wins = 0
    losses = 0
    draws = 0
    for game in games:
        if game.winning_player is None:
            draws += 1
        elif game.losing_player.username == username:
            losses += 1
        else:
            wins += 1

    return AnnualSummary(year, wins, losses, draws)


def create_annual_summary_graph(summary: AnnualSummary) -> List[str]:
    """Create a bar graph representation of a player's games.

    :param summary: A summary of the player's games
    :return: A list of the graph's rows
    """
    graph = []
    title = f"\nYour {summary.year} Chess.com Year in Review\n"
    graph.append(title)

    data = {
        "Wins": summary.wins,
        "Losses": summary.losses,
        "Draws": summary.draws,
    }
    label_space_control = max((len(label) for label in data.keys()))
    value_space_control = max((len(str(value)) for value in data.values())) + 1
    scaled_data = _scale_values(data)
    for (label, value), scaled_value in zip(data.items(), scaled_data.values()):
        num_bars, remainder = divmod(scaled_value, 8)
        bar = "█" * num_bars
        remainder_bar = chr(ord("█") + remainder)
        bar += remainder_bar
        row = f"{label.rjust(label_space_control)} | {str(value).rjust(value_space_control)} {bar}"
        graph.append(row)

    return graph


def _scale_values(data: Dict[str, int]) -> Dict[str, int]:
    """Scale data values to fit a pre-determined width.

    :param data: A dictionary of labels to data values to be scaled
    :return: A dictionary of the provided labels to scaled data values
    """
    graph_max_num_bars = 288  # 36 bars of eighths
    max_data_value = max(data.values())
    if max_data_value > 0:
        scale_factor = graph_max_num_bars / max_data_value
    else:
        return data

    scaled_data = {}
    for label, value in data.items():
        scaled_data[label] = int(value * scale_factor)

    return scaled_data


def print_annual_summary_graph(graph: List[str]) -> None:
    """Print an annual summary graph to the console.

    :param graph: The graph to be printed
    """
    for row in graph:
        print(row)
