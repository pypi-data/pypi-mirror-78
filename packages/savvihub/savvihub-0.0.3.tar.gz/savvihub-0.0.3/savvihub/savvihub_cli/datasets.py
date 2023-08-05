import os

import grequests
import typer

from savvihub.savvihub_cli.config import config
from savvihub.savvihub_cli.savvihub import SavviHubClient, SavviDatasetFile

dataset_app = typer.Typer()


def parse_dataset_arg(dataset_arg):
    workspace, rest = dataset_arg.split("/")
    if ":" in rest:
        dataset, ref = rest.split(":")
    else:
        dataset = rest
        ref = "latest"
    return workspace, dataset, ref


@dataset_app.callback()
def main():
    return


@dataset_app.command()
def create():
    return


@dataset_app.command()
def push(
    dataset_arg: str = typer.Option(..., "-r"),
    path_arg: str = typer.Argument("."),
):
    workspace, dataset, ref = parse_dataset_arg(dataset_arg)

    client = SavviHubClient(config.token)

    dirs = []
    files = []

    def deepwalk(path):
        for root, dirs_, files_ in os.walk(path_arg):
            for name in dirs_:
                dirs.append(os.path.join(root, name))
                deepwalk(os.path.join(root, name))
            for name in files_:
                files.append(os.path.join(root, name))

    rs = [grequests.post(f'/api/workspaces/{workspace}') for dir in dirs]
    pass


@dataset_app.command()
def pull(
    dataset_arg: str = typer.Option(..., "-r"),
    path_arg: str = typer.Argument("."),
):
    workspace, dataset, ref = parse_dataset_arg(dataset_arg)

    client = SavviHubClient(config.token)
    files = client.dataset_file_list(workspace, dataset, ref=ref)

    def download_file(file: SavviDatasetFile, pg):
        def fn(resp):
            path = os.path.join(path_arg, file.path)
            with open(path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            pg.update(1)
        return fn

    with typer.progressbar(length=len(files)) as progress:
        rs = [grequests.get(file.download_url.url, stream=True, callback=download_file(file, progress)) for file in files]
        grequests.map(rs, size=config.parallel)
    typer.echo(f'Downloaded {len(files)} in {os.path.abspath(path_arg)}')


if __name__ == "__main__":
    dataset_app()