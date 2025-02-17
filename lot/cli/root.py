import yaml
import os
import typer
from typing_extensions import Annotated

from lot._lot.park import park


app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def push(
    target: Annotated[str, typer.Option(
        "--target", "-t",
        help="namespace/environment:tag to push to"
    )],

):
    """Push an environment to park"""
    park_url = os.environ.get("PARK_URL")
    api = park.Park(park_url)

    namespace = target.split("/")[0]
    env_tag = target.split("/")[1]
    environment = env_tag.split(":")[0]
    tag = env_tag.split(":")[1]

    # assume environment spec is in the cwd and is called environment.yaml
    env_yaml_raw = ""
    if os.path.exists("./environment.yaml"):
        with open("./environment.yaml", "rb") as f:
            env_yaml_raw = f.read()
    env_yaml = yaml.load(env_yaml_raw, yaml.FullLoader)

    # assume environment lockfile is in the cwd and is called conda-lock.yml
    conda_lock_raw = ""
    if os.path.exists("./conda-lock.yml"):
        with open("./conda-lock.yml", "rb") as f:
            conda_lock_raw = f.read()
    conda_lock = yaml.load(conda_lock_raw, yaml.FullLoader)

    data = {
        "environment": env_yaml,
        "conda-lock": conda_lock,
    }

    api.push(namespace, environment, tag, data)


@app.command()
def pull(
    target: Annotated[str, typer.Option(
        "--target", "-t",
        help="namespace/environment:tag to pull from"
    )],
    rev: str = typer.Option(
        help="uuid of the revision to pull"
    ),

):
    """Pull an environment from park"""
    park_url = os.environ.get("PARK_URL")
    api = park.Park(park_url)

    namespace = target.split("/")[0]
    env_tag = target.split("/")[1]
    environment = env_tag.split(":")[0]
    tag = env_tag.split(":")[1]

    checkpoint_data = api.pull(namespace, environment, tag)
    checkpoint_dict = yaml.load(checkpoint_data, yaml.FullLoader)

    # TODO
