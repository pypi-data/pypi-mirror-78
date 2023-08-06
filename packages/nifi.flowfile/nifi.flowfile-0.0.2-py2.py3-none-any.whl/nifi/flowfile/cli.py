"""Console script for nifi.flowfile."""
import os
import click

import configparser

from .stream import FlowFileStreamReader


@click.group()
def flowfile():
    """NiFi's FlowFile Stream v3 Pack/Unpack."""
    return 0


@flowfile.command()
def pack():
    """packs content."""
    return 0


@flowfile.command()
@click.option(
    "-C",
    "--directory",
    metavar="DIR",
    help="change to directory DIR",
    default=".",
    show_default=True,
    type=click.Path(file_okay=False, resolve_path=True),
)
@click.option("-v", "--verbose", count=True)
@click.argument("file", type=click.File(mode="rb"))
def unpack(directory, verbose, file):
    """unpacks content.

    \b
    FILE: Path to FlowFile Stream v3 file.
    """

    for attributes, data in FlowFileStreamReader(file):
        path = os.path.abspath(os.path.join(directory, attributes["path"]))
        os.makedirs(path, exist_ok=True)

        filename = attributes["filename"]
        abs_filename = os.path.abspath(os.path.join(path, filename))
        with open(abs_filename, mode="wb") as f:
            if verbose:
                click.echo("{}".format(f.name))
            f.write(data)

        with open(abs_filename + ".ffa.ini", mode="wt") as f:
            if verbose:
                click.echo("{}".format(f.name))
            config = configparser.ConfigParser()
            config["attributes"] = attributes
            config.write(f)

    return 0
