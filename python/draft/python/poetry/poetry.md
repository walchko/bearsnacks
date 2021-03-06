---
title: Poetry and The New Way to Maintain a Project
date: 20 Jan 2020
---

## Commands

![](install.gif)

| Command                           | Description |
|-----------------------------------|-------------|
| poetry new [package-name]	        | Start a new Python Project.| 
| poetry init	                    | Create a pyproject.toml file interactively.| 
| poetry install	                | Install the packages inside the pyproject.toml file.| 
| poetry add [package-name]	        | Add a package to a Virtual Environment. | 
| poetry add -D [package-name]	    | Add a dev package to a Virtual Environment. | 
| poetry remove [package-name]	    | Remove a package from a Virtual Environment. | 
| poetry remove -D [package-name]	| Remove a dev package from a Virtual Environment. | 
| poetry self:update	            | Update poetry to the latest stable version. | 

### Poetry Broken

Unfortunately `poetry` is **broken** and misbehaving. I default to versio 1.0.0

```
poetry self update 1.0.0
```

### Authentication

1. Setup an API token in PyPi, example token: `pypi-12345`
1. Then run: `poetry config pypi-token.pypi pypi-12345`

### Development

For developing a package you could do `pip install -e .` with `pip`. Poetry does a
similar thing with just doing `poetry install`.

### Nice things

- Reduces all of the various config files (`setup.py`, `requirements.txt`, `setup.cfg`, etc) 
to one `pyproject.toml` in [PEP518](https://www.python.org/dev/peps/pep-0518/) so it is *official*
- Poetry is designed to use the new toml file and reduce the headache of packaging

### Not so nice things

-  Install doesn't use `pip` but rather a script you pull with curl: `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`
    - This allows `poetry` to isolate itself from the system distro ... which isn't a bad thing

## Other Run Commands 

- `Flake8`: linting
- [`Black`](https://github.com/psf/black): code formatter to make our stuff [PEP8](https://www.python.org/dev/peps/pep-0008/) compliant
- `pytest`: it appears that `nose` is dead but there is some movement on [`nose2`](https://github.com/nose-devs/nose2) ... moving on

# References

- PyPi [api token](https://pypi.org/help/#apitoken)
- Poetry [credential setup](https://python-poetry.org/docs/repositories/#configuring-credentials)
- Poetry [website](https://python-poetry.org/)
- Poetry [github](https://github.com/python-poetry/poetry)
- Overview and thoughts of poetry in a [blog](https://hackersandslackers.com/python-poetry/)
- Another [overview](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1/)
