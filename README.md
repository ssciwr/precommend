# Welcome to precommit-recommendations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This a small utility that creates a `.pre-commit-config.yaml` based on the files
in your current working directory and the recommendations of the Scientific Software Center.

## Installation

The Python package can be installed with

```
git clone https://github.com/ssciwr/precommit-recommendations.git
cd precommit-recommendations
python -m pip install .
```

## Usage

Head to a directory that you want to add a config file to and run

```bash
precommit_recommendations
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
