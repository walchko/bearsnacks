---
title: Python Virtual Environments
---

These virtual environments allow you to keep different libraries separated or
test out new libraries without polluting your OS `site-packages`.

## References

- [Python 3 documents](https://docs.python.org/3/library/venv.html)

# Create a Python3 Virtual Env

Here we are creating a new environment which is housed in
`~/venv` (you could choose any folder name hidden or not) and
setup it up for OpenCV and Jupyter:

    python3 -m venv ${HOME}/venv
    . ~/venv/bin/activate
    pip install -U pip setuptools wheel
    pip install jupyter matplotlib numpy
    pip install opencv-contrib-python

Then adjust your `.bash_profile` or `.bashrc`:

    nano ~/.bash_profile
    source /home/kevin/.venv/bin/activate

To exit the environment: `$ deactivate`

# Upgrading to a Newer Version of Python

So on Ubuntu, the default is 3.6, but there is a package for 3.7.
To set it to the new version, I re-ran the command:

```
python3.7 -m venv /home/kevin/.venv
```

Then I had to change the pointers in `~/.venv/bin` to:

```
ln -s /usr/bin/python3.7 python
ln -s /usr/bin/python3.7 python3
```

The system still had `python3` pointing to the 3.6 version. I didn't want
to change my system at all.

Also, this caused me to have to re-install all of my packages.
