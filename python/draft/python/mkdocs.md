---
title: Making Program Documentation
date: 26 Sept 2019
---

![](https://squidfunk.github.io/mkdocs-material/assets/images/material.png)

Building project documentation using [`mkdocs`](https://www.mkdocs.org/) and the
theme [material](https://squidfunk.github.io/mkdocs-material/)

## Install

```
$ pip install -U mkdocs mkdocs-material
```

## Setup and Creation

```
+- mkdocs.yml
+- docs/
    |
    +- index.md
    +- about.md
```

In your `mkdocs.yml`:

```
site_name: Coolness
nav:
    - Home: index.md
    - About: about.md
theme:
    name: 'material'
```

- Build with: `mkdocs build`
- Clean up with: `mkdocs build --clean
- Deploy to github: `mkdocs gh-deploy`
