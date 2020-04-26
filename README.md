# autopy-lot
A github action to perform automatic conversion from jupyter notebooks to markdown, python scripts and lot more.

This action uses [jupytext](https://github.com/mwouts/jupytext) internally for the conversions.

## conversions:
1. .ipynb -> .md
2. .ipynb -> .py
3. .py -> .ipynb

### NOTE
> ``R`` support will be added soon. Please don't try to convert R files for now.

## USAGE

create a ``autopy-lot.yml`` file under ``.github/workflows`` with the following contents:
### Default configuration
```workflow
name: autopy-lot
on: [push]

jobs:
  build:
    name: autopy-lot
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - name: autopy-lot 
        uses: deep5050/autopy-lot@1.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN}}
```
### Advanced configuration

```workflow
name: autopy-lot
on: [push]

jobs:
  build:
    name: autopy-lot
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - name: autopy-lot 
        uses: deep5050/autopy-lot@1.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN}}
          check:
          input_type:
          comment_magics:
          split_at_heading:
          output_type:
          output_dir:


```
### Inputs

``check``  :``all`` to convert all specified files on every run. ``latest`` to convert only the files changed on last commit.

``input_types``: ``py`` ``ipynb`` ``r``

``comment_magics`` : ``true`` see jupytext documentation for further details.

``split_at_heading: ``true`` see jupytext documentation for further details.


``output_type`` : ``py`` ``markdown`` ``r`` ``ipynb``


``output_dir``: give a output directory name where all the converted outputs will be stored.

