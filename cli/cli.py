#!/usr/bin/env python3

import itertools
import os
import sys
import threading
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


# https://github.com/click-contrib/click-spinner
class Spinner(object):
    spinner_cycle = itertools.cycle(["-", "/", "|", "\\"])

    def __init__(self, beep=False, disable=False, force=False, stream=sys.stdout):
        self.disable = disable
        self.beep = beep
        self.force = force
        self.stream = stream
        self.stop_running = None
        self.spin_thread = None

    def start(self):
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            self.stream.write(next(self.spinner_cycle))
            self.stream.flush()
            self.stop_running.wait(0.25)
            self.stream.write("\b")
            self.stream.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return False
        self.stop()
        if self.beep:
            self.stream.write("\7")
            self.stream.flush()
        return False


def spinner(beep=False, disable=False, force=False, stream=sys.stdout):
    """This function creates a context manager that is used to display a
    spinner on stdout as long as the context has not exited.
    The spinner is created only if stdout is not redirected, or if the spinner
    is forced using the `force` parameter.
    Parameters
    ----------
    beep : bool
        Beep when spinner finishes.
    disable : bool
        Hide spinner.
    force : bool
        Force creation of spinner even when stdout is redirected.
    Example
    -------
        with spinner():
            do_something()
            do_something_else()
    """
    return Spinner(beep, disable, force, stream)


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
def add():
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
def train():
    click.echo("Infer")


@main.command()
def infer():
    click.echo("Infer")


@main.command()
def show():
    with spinner(disable=True):
        time.sleep(2.4)
        click.echo("Infer")


if __name__ == "__main__":
    main()
