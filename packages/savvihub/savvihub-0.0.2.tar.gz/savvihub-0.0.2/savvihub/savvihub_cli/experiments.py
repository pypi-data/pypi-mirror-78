import requests
import typer
from savvihub.savvihub_cli.constants import DEFAULT_CONFIG_PATH, HOST_URL, CUR_DIR
from savvihub.savvihub_cli.errors import get_error_message
from savvihub.savvihub_cli.utils import *
from savvihub.savvihub_cli.yml_loader import YmlLoader, experiment_conf

experiment_app = typer.Typer()


@experiment_app.callback()
def main():
    """
    Perform your experiment with Savvihub
    """
    return


@experiment_app.command()
def init():
    """
    Initialize a new experiment configuration file
    """
    data = {
        'workspace_slug': typer.prompt('workspace name'),
        'project_slug': typer.prompt('project name'),
        'image_id': int(typer.prompt('image')),
        'resource_spec_id': int(typer.prompt('resource spec')),
        'start_command': typer.prompt('start command'),
    }

    config_file_path = os.path.join(CUR_DIR, "savvihubfile.yml")
    with open(config_file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

    typer.echo(f"Experiment config successfully made in {config_file_path}")


@experiment_app.command()
def run(
        file: str = typer.Option("savvihubfile.yml", "--file", "-f"),
):
    """
    Run an experiment in Savvihub
    """
    token = get_token_from_config(DEFAULT_CONFIG_PATH)
    headers = get_json_headers_with_token(token)

    yml_loader = YmlLoader(file, experiment_conf)

    # TODO:: dynamically binding the following data fields
    yml_loader.data['branch'] = 'master'
    yml_loader.data['dataset_id_refs'] = {'id': 1, 'ref': 'latest'}

    workspace_slug = yml_loader.pop_val_by_key('workspace_slug')
    project_slug = yml_loader.pop_val_by_key('project_slug')

    res = requests.post(
        url=f'{HOST_URL}/v1/api/workspaces/{workspace_slug}/projects/{project_slug}/experiments/',
        headers=headers,
        data=json.dumps(yml_loader.data),
    )

    res_data = res.json()
    if res.status_code == 400:
        typer.echo(get_error_message(res_data))
        return

    experiment_number = res_data.get('expriment').get('number')
    typer.echo(f"Experiment {experiment_number} is running. Check the experiment status at below link")
    # TODO:: Experiment status URL
    typer.echo(f"URL:")
    return


if __name__ == "__main__":
    experiment_app()
