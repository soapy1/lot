import yaml
import os
import typer
from typing_extensions import Annotated

from lot._lot import park


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

    # TODO
    data = {}

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
