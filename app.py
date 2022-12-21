from argparse import ArgumentParser
from datetime import datetime
from os import system
from pathlib import Path
from random import shuffle
from sys import argv
from xml.etree import ElementTree as ET


def draw(filename: str = "white_elephant.txt") -> list[str]:
    """Draws players from names listed in a text file.

    Draws players from a provided list of strings and also a newline separated list of strings in a text file and returns them.
    """
    players: list[str] = list()
    with open(filename) as file:
        players = [
            player.partition("#")[0].strip()
            for player in file.readlines()
            if player.partition("#")[0].strip() != ""
        ]
    shuffle(players)
    return players


def write_html(
    players: list[str] = None,
    theme: str = "white_elephant.css",
    output: str = "white_elephant.html",
) -> str:
    """Writes the list of players to a file with a specified theme."""
    timestamp = datetime.now().strftime("%m/%d/%Y at %H:%M:%S%p")
    with open(theme, encoding="UTF-8") as file:
        css = file.read()
    html = ET.Element("html")
    head = ET.SubElement(html, "head")
    ET.SubElement(head, "meta", {"charset": "UTF-8"})
    ET.SubElement(head, "title").text = "White Elephant"
    # ET.SubElement(head, "link", {"rel": "stylesheet", "href": "white_elephant.css"})
    # Embedding the stylesheet in the html makes the file portable.
    ET.SubElement(head, "style", {"type": "text/css"}).text = css
    body = ET.SubElement(html, "body")
    ET.SubElement(body, "h1").text = "White Elephant"
    ol = ET.SubElement(body, "ol")
    for name in players:
        ET.SubElement(ol, "li").text = name
    ET.SubElement(body, "p").text = f"Names drawn on {timestamp}."
    with Path(output) as file:
        file.write_text(
            ET.tostring(html, method="html", encoding="unicode"), encoding="UTF-8"
        )
        return file.name


def parse_arguments(arguments: list[str] = None):
    """Process the command line arguments."""
    parser = ArgumentParser()
    parser.add_argument("--count", "-c", type=int, help="The number of manes to draw.")
    parser.add_argument(
        "--input",
        "-i",
        default="white_elephant.txt",
        help="The name of the file from which to draw names.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="white_elephant.html",
        help="The name of the output file.",
    )
    parser.add_argument(
        "--theme",
        "-t",
        default="white_elephant.css",
        help="Format the output with colors in the theme.",
    )
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    path = write_html(
        draw(arguments.input)[: arguments.count],
        theme=arguments.theme,
        output=arguments.output,
    )
    system(f"start {path}")


if __name__ == "__main__":
    main()
