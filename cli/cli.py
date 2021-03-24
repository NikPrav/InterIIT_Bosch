#!/usr/bin/env python3

from auth0.v3.authentication import Social,GetToken, Database

import itertools
import os
import sys
import threading
import time
import urllib

import click
import requests
from click_didyoumean import DYMGroup

# import configparser

# config = configparser.ConfigParser()
# config.read('~/.config/.cbtsrc')

########################### CHANGE THESE!1!1!1!1! #############################
AUTHO_ACCOUNT = 'dev-kqx4v2yr.jp.auth0.com'
CLIENT_ID="DBJyWZCoiZFCccUM5C50YYSPrBXn08oL"
CLIENT_SECRET='HnKdfJzvT3YHoiu0hI_rYyWBtUiwujzHBngNp0jYf2eN1WyIfnYK7avlLBl-wYPu'
UTH0_DOMAIN = 'dev-kqx4v2yr.jp.auth0.com'
########################### CHANGE THESE #############################
ACCESS_KEY = os.getenv("ACCESS_KEY")
USERNAME = os.getenv('USERNAME_CLI')
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

@click.option(
    '--reg_stat',
    default = False,
    show_default=True,
    help = 'Set to true to register new user. Make sure that your password has atleast 8 character, a lowercase letter, a special character and a number'
)

@click.password_option()
# Auth0 Commands



def main(debug, gui, json,reg_stat,password):
    click.echo(reg_stat)
    token = ''
    if reg_stat:
        token = reg_new_user(password)
    else:
        token = authHandler(password)
    return

    


@main.command(hidden=True)
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())


@main.command()
def add():
    click.echo("Infer")

# @main.command()
def authHandler(pwd):
    social = Social(AUTHO_ACCOUNT)
    token = GetToken(AUTHO_ACCOUNT)
    url = 'https://dev-kqx4v2yr.jp.auth0.com/oauth/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    # scope = "appstore::apps:r eadwrite"
    grant_type = "client_credentials"
    click.echo(USERNAME)
    data = {
        "grant_type": grant_type,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
        # "scope": scope
    }
    auth = {}
    try:
        auth_token = requests.post(url,data=data,headers = header)
        # auth_token = auth_token.json()
        auth = token.login(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=pwd, realm='Username-Password-Authentication',scope ="read:current_user",audience='https://dev-kqx4v2yr.jp.auth0.com/api/v2/')
        click.echo('Successfully verified!!')
        click.echo(auth)
#         curl --request GET \
#       --url 'https://dev-kqx4v2yr.jp.auth0.com/api/v2/users?q=email%3A%22jane%40exampleco.com%22&search_engine=v3' \
#       --header 'authorization: Bearer YOUR_MGMT_API_ACCESS_TOKEN'
        # tk = auth.get('access_token')
        # uname = urllib.parse.quote(USERNAME)
        # click.echo(f'ename:{uname}')
        # auth_id = requests.get(f'https://dev-kqx4v2yr.jp.auth0.com/api/v2/users?q=email%3A%22{uname}%22&search_engine=v3',
        #     headers = {'Authorization' : f'Bearer {tk}'})
        # click.echo(auth_id)
        # auth_id = auth_id.json()
        # auth_id = auth_id.get('identities').get('user_id')
        # click.echo(auth_id)
    except Exception as e:
        click.echo(e)

    return auth.get('access_token')

def reg_new_user(pwd):
    database = Database(AUTHO_ACCOUNT)
    token = GetToken(AUTHO_ACCOUNT)
    try:
        status = database.signup(client_id=CLIENT_ID, email=USERNAME, password=pwd, connection='Username-Password-Authentication')
        auth = token.login(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=pwd, realm='Username-Password-Authentication',scope ="read:current_user",audience='https://dev-kqx4v2yr.jp.auth0.com/api/v2/')
        click.echo(auth)
        click.echo(f'Success:{status}')
    except Exception as e:
        click.echo(f'Failure:{e}')

    return auth.get('access_token')



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
# @click.argument("src", nargs=-1)
# def augment(ctx, local, src):
#     click.echo(ctx)



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

@main.command()
def sendPrivateReq(token):
    UrlToSendDataTo = 'http://localhost:5000/api/private'
    data = requests.get(url=UrlToSendDataTo,
     headers = {'Authorization' : f'Bearer {token}','UserEmail' : USERNAME})
    click.echo(data)


    

if __name__ == "__main__":
    main()
