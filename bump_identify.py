import re
import requests

# Fetch the latest version of the packages
identify_version = requests.get("https://pypi.org/pypi/identify/json").json()["info"][
    "version"
]
precommit_version = requests.get("https://pypi.org/pypi/pre-commit/json").json()[
    "info"
]["version"]

# Read the content of the pyproject.toml file
with open("pyproject.toml", "r") as f:
    data = f.read()

# Replace the version of the packages
data = re.sub(f"identify >=.*\n", f'identify >= {identify_version}",\n', data)
data = re.sub(f"pre-commit >=.*\n", f'pre-commit >= {precommit_version}",\n', data)

# Write the new content to the pyproject.toml file
with open("pyproject.toml", "w") as f:
    f.write(data)
