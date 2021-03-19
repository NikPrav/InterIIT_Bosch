#!/usr/bin/env python3

import itertools
import os
import sys
import time

import click
import requests
from click_didyoumean import DYMGroup

# import configparser

# config = configparser.ConfigParser()
# config.read('~/.config/.cbtsrc')

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                f"--{self.name} is mutually exclusive with "
                + f"--{[*self.mutually_exclusive][0]}."
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


@click.group(context_settings=CONTEXT_SETTINGS, cls=DYMGroup)
@click.option("--debug/--no-debug", default=False, show_default=True)
@click.option(
    "--gui/--no-gui",
    default=False,
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["json"],
)
@click.option(
    "--json/--no-json",
    default=False,
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["gui"],
)
def main(debug, gui, json):
    return


@main.command(hidden=True)
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())


@main.command()
@click.pass_context
def add(ctx):
    click.echo("Infer")


@main.command()
@click.pass_context
@click.option(
    "-l",
    "--local",
    default=False,
    is_flag=True,
    help="Create modified images locally",
    show_default=True,
)
@click.argument("src", nargs=-1)
def augment(ctx, local, src):
    click.echo(ctx)


@main.command()
@click.pass_context
def train(ctx):
    click.echo("Infer")


@main.command()
@click.pass_context
def infer(ctx):
    click.echo("Infer")


@main.group()
@click.pass_context
def show(ctx):
    click.echo("Infer")


@show.command()
@click.pass_context
def dataset(ctx):
    click.echo("Infer")


if __name__ == "__main__":
    main()
