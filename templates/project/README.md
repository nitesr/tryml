# Project template

A cookiecutter template to create new project in this mono-repo.

## How to use
Load the monorepo's top-level sandbox, that contains cookiecutter:

```
# From the monorepo root
# Create the sandbox (only do that the first time)
python3 -m venv .venv; source .venv/bin/activate
pip install -r pip-requirements.txt
pip install -r dev-requirements.txt

# if you hit any error try this and rerun above two steps
python -m ensurepip --upgrade
python -m pip install --upgrade setuptools

# Load the sandbox (todo every time)
source .venv/bin/activate
```

Then run cookiecutter _from the root directory of the monorepo_:

```
cookiecutter templates/project --output-dir projects/
```

Notes:

- When entering a app name, do not include a 'nitesr-' prefix.
- When entering your github handle, include the '@' prefix


