# copied from https://github.com/soapy1/fod
# in the future, we can import the fod package

import os
import datetime
from pydantic import BaseModel
import hashlib
import uuid
import yaml


def short_uuid() -> str:
    return uuid.uuid4().hex[:8]


class EnvironmentSpec(BaseModel):
    """Specifies a locked environment from pixi

    spec : str
      The spec file for the environemnt
    
    lockifle : str
      The lock file for the environment

    lockfile_hash : str
      Hash for the content of the lockfile. If the lockfile hash has
      changed, then the environment has been updated. If the spec
      file has changed, it will cause a change in the lockfile as
      well.
    """
    spec: str
    lockfile: str
    lockfile_hash: str


class EnvironmentCheckpoint(BaseModel):
    """An environment at a point in time
    
    Only applys to a particular environment spec
    """
    environment: EnvironmentSpec
    timestamp: str
    # TODO: how do you actually create a uuid?
    uuid: str
    tags: list[str]

    @classmethod
    def from_path(cls, path: str, uuid: str):
        lock_path = f"{path}/conda-lock.yml"
        spec_path = f"{path}/environment.yaml" 
        if not os.stat(lock_path):
          raise Exception("did not find lock file")
        if not os.stat(spec_path):
            raise Exception("did not find spec file")

        lock_data = ""
        with open(lock_path, 'rb') as file:
            lock_data = file.read()

        spec_data = ""
        with open(spec_path, 'rb') as file:
            spec_data = file.read()

        spec = EnvironmentSpec(
            spec = spec_data,
            lockfile = lock_data,
            lockfile_hash = hashlib.sha256(lock_data).hexdigest()
        )

        return cls(
            environment=spec,
            timestamp=str(datetime.datetime.now(datetime.UTC)),
            uuid=uuid,
            tags=[uuid]
        )