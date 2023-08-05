# SWAP Python SDK

## Prerequisites

You will need to have the following installed:

* Python
* `pip`
* `gcloud`
* `git`

## Clone the repo

To clone the repo, you will need to have access to Cloud Source Repositories and be logged into GCP using the `gcloud` command line tool. Next, run the following command replacing `YOUR_EMAIL` with the email you use to authenticate with GCP:

```bash
git clone ssh://YOUR_EMAIL@source.developers.google.com:2022/p/microservice-pilot/r/swap-python-sdk
```

`cd` into the cloned repo and continue with the rest of this guide.

## Install

Firstly install `pipenv`.

```bash
pip install pipenv
```

This will manage your Python environment and make sure you have the necessary dependencies installed. It uses the `Pipfile` found in the root of the repo to define the required dependencies and the `Pipfile.lock` to keep track of which exact versions have been installed.

To install using `pipenv` run:

```bash
pipenv install --dev
```

Once the install is complete you can run the following to activate the environment:

```bash
pipenv shell
```

Before the library is available on `pip`, you will need to build the library locally:

```bash
make build
```

If you aren't able to run `make` commands, i.e. you are using Windows, you can run the build command manually:

```bash
python setup.py develop sdist bdist_egg bdist_wheel
```

This will create a `dist` repository among others. This is where your wheel file will be created. It will have a name like `dist/swap_python_sdk-0.0-py3-none-any.whl`.

See docs on [building and installing](docs/building_installing.md) for more information.

### Install locally

Once built, you can then install the SDK. In the target repository that you wish to use the SDK, assuming you have `pip` installed replacing `../swa-python-sdk/dist/swa-0.0-py3-none-any.whl` with the path to the built wheel:

```bash
pip install ../swa-python-sdk/dist/swa-0.0-py3-none-any.whl
```

## Next steps

* [API Usage](docs/api_usage.md)
* [Development](docs/development.md)
* Jupyter notebook
* Sample service application
