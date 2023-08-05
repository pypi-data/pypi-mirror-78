import click

from chess_stats import __version__
from chess_stats import chess_stats as stats


@click.command()
@click.version_option(version=__version__)
@click.argument("username")
@click.argument("year")
def main(username, year):
    """View your Chess.com year in review"""
    summary = stats.create_annual_summary(username, int(year))
    graph = stats.create_annual_summary_graph(summary)
    stats.print_annual_summary_graph(graph)
