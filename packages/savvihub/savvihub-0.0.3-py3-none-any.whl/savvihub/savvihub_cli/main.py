import requests
import typer

from savvihub.savvihub_cli.config import config
from savvihub.savvihub_cli.constants import HOST_URL, DEFAULT_SAVVI_DIR, DEFAULT_CONFIG_PATH
from savvihub.savvihub_cli.datasets import dataset_app
from savvihub.savvihub_cli.errors import get_error_message
from savvihub.savvihub_cli.experiments import experiment_app
from savvihub.savvihub_cli.utils import *

app = typer.Typer()
app.add_typer(experiment_app, name="experiments")
app.add_typer(dataset_app, name="datasets")
__version__ = '0.0.3'


def version_callback(value: bool):
    if value:
        typer.echo(f"Savvihub CLI Version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
    token: str = typer.Option(None, "--token"),
    parallel: int = typer.Option(20, "--parallel"),
):
    """
    Savvihub command line interface
    """
    if token:
        config.token = token
    if parallel:
        config.parallel = parallel

    return


@app.command()
def ping():
    """
    Ping to server
    """
    res = requests.get(HOST_URL + '/v1/api/ping/')
    typer.echo(f"Response code: {res.status_code}, Response text: {res.text}")


@app.command()
def login():
    """
    Login command
    """
    email = typer.prompt("Email")
    password = typer.prompt("Password")
    data = {
        'email': email,
        'passowrd': password,
    }

    headers = {'Content-Type': 'application/json'}
    res = requests.post(
        url=f'{HOST_URL}/v1/api/accounts/signin/',
        headers=headers,
        data=json.dumps(data),
    )

    res_data = res.json()
    if res.status_code == 400:
        typer.echo(get_error_message(res_data))
        return

    token = res_data.get('token')
    typer.echo("Initialize with this token")
    typer.echo(f"token: {token}")
    return


@app.command()
def init():
    """
    Initialize with token
    """
    data = {
        'token': typer.prompt('token')
    }

    make_dir(DEFAULT_SAVVI_DIR)
    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

    typer.echo(f"Token successfully saved in {DEFAULT_CONFIG_PATH}")
