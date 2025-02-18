# Lot

The goal of this demo project is to show:
* how to package up conda and pixi environemnts to push to park
* how to retrieve environments from park and use them locally

## Dev env

To setup your dev env, create a conda env

```
$ conda env create -f environment.yml 

$ conda activate lot-dev
```

## Try it out

Make sure you have 
* a [park server](https://github.com/soapy1/park) running and 
* the `PARK_URL` env var set to the park server urls

### Create and push an environment

```
# create an environment.yaml with your dependencies and
# use conda-lock to create the lock file
$ conda-lock -f environment.yaml -p osx-64 -p linux-64

# push the environment to park
$ lot push -t soph/lot:v1.0.0
```

### Pull and install an environment

```
# pull the environment from park
$ lot pull -t soph/lot:v1.0.0

# install the environment locally to /tmp/test
$ conda-lock install -p /tmp/test conda-lock.yml         

# activate the environment
$ conda activate /tmp/test
```