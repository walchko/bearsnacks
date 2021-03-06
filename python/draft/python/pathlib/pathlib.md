---
title: Pathlib
date: 12 Nov 2020
---

`pathlib` has a lot of cool stuff, here is a little sample:

```python
>>> from pathlib import Path
>>> Path.home() / "tmp"
PosixPath('/Users/kevin/tmp')

>>> Path(".").glob("*.py")
<generator object Path.glob at 0x11b40ce40>

>>> list(Path(".").glob("*.py"))
[PosixPath('sim.py'),
PosixPath('vo.py'),
PosixPath('utils.py'),
PosixPath('mov.py')]

>>> list(Path.home().joinpath("github").glob("*.sh"))
[PosixPath('/Users/kevin/github/pull-all.sh'),
PosixPath('/Users/kevin/github/git-pull.sh')]
 
```

```python
Path.is_dir()
Path.is_file()
Path.is_mount()
Path.is_symlink()
...
```

```python
>>> p = Path('setup.py')
>>> with p.open() as f:
...     f.readline()
```

## References

- python docs: [pathlib](https://docs.python.org/3/library/pathlib.html)
- more [pathlib examples](https://rednafi.github.io/digressions/python/2020/04/13/python-pathlib.html)

