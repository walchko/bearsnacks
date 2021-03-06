---
title: Python Modules
date: 2017-06-21
abstract: Making a Python package for Pypi
---

![](https://imgs.xkcd.com/comics/python_environment.png)

Module Setup
-------------------

```
module_name
  -- LICENSE
  -- setup.py
  -- README.rst
  -- module
     -- __init__.py
     -- script1.py
     -- script2.py
```

`setup.py`
~~~~~~~~~~~~~~

```python

#!/usr/bin/env python

from setuptools import setup
from cool_name import __version__ as VERSION

ENTRY_POINTS = {
	'console_scripts': [
		'something = cool_name/something:main',
	],
}


README_FILE = 'README.rst'

def get_long_description():
	with open(README_FILE, 'r') as fd:
		desc = fd.read()
	return desc


setup(
	author='Kevin Walchko',
	author_email='kevin.walchko@outlook.com',
	name='cool_name',
	version=VERSION,
	description='A library to do cool things',
	long_description=get_long_description(),
	url='http://github.com/walchko/cool_name',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Libraries :: Application Frameworks'
	],
	license='MIT',
	keywords='cool name stuff',
	packages=['cool_name'],
	install_requires=['pyserial'],
	entry_points=ENTRY_POINTS
)
```

`__init__.py`
~~~~~~~~~~~~~~~~~~

```python

	#!/usr/bin/env python

	__version__ = '1.2.3'
```

`pip` Commands
---------------------


Commands |                   Purpose
|---|---|
`pip install module`   |   install from PyPi
`pip install -e .`     |  install local for development
`pip install -U module` |  upgrade module from PyPi
`pip uninstall module` |   uninstall module


PyPi
-----

Some good resources are [Python Packaging
Guide](https://packaging.python.org/en/latest/distributing.html#uploading-your-project-to-pypi)
and [Tom Christie](https://tom-christie.github.io/articles/pypi/) for
more info.

1. Create an account at pypi.org
2. Create a package repository at pypi.org using the [web
   form](https://pypi.python.org/pypi?%3Aaction=submit_form) and
   uploading the PKG-INFO file
3. `python setup.py test`
4. `python setup.py sdist`
5. `twine upload dist/*`

Twine can be installed using `pip install twine` which will secure
your upload and protect your password. Also the username and password
are stored in a `.pypirc` in your home directory.

The structure of a `.pypirc` file is pretty simple

```
[distutils]
index-servers = pypi

[pypi]
repository: https://www.python.org/pypi
username: <username>
password: <password>
```

Wheel and Eggs
----------------

They are basically just zip files

```
$ unzip -l /path/to/file.egg
$ unzip -l /path/to/file.whl
```
