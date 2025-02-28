import yaml
import os
import typer
from typing_extensions import Annotated

from lot._lot.park import park
from lot._lot.models import environment


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
    env = env_tag.split(":")[0]
    tag = env_tag.split(":")[1]

    # assume environment.yaml and conda-lock.yaml are in the cwd
    checkpoint = environment.EnvironmentCheckpoint.from_path(os.getcwd(), tag)
    data = checkpoint.model_dump()

    api.push(namespace, env, tag, data)


@app.command()
def pull(
    target: Annotated[str, typer.Option(
        "--target", "-t",
        help="namespace/environment:tag to pull from"
    )],

):
    """Pull an environment from park"""
    park_url = os.environ.get("PARK_URL")
    api = park.Park(park_url)

    namespace = target.split("/")[0]
    env_tag = target.split("/")[1]
    environment = env_tag.split(":")[0]
    tag = env_tag.split(":")[1]

    checkpoint_data = api.pull(namespace, environment, tag)
    conda_lock_yaml = yaml.dump(checkpoint_data.get("conda-lock"))
    environment_yaml = yaml.dump(checkpoint_data.get("environment"))

    # assume environment lockfile is in the cwd and is called conda-lock.yml
    with open("./conda-lock.yml", "w") as f:
        f.write(conda_lock_yaml)

    # assume environment spec is in the cwd and is called environment.yaml
    with open("./environment.yaml", "w") as f:
        f.write(environment_yaml)

