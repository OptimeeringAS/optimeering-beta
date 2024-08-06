import json

import toml

pyproject = toml.load("../pyproject.toml")

config = {
    "packageName": pyproject["tool"]["poetry"]["packageName"],
    "projectName": pyproject["tool"]["poetry"]["description"],
    "generateSourceCodeOnly": True,
    "packageVersion": pyproject["tool"]["poetry"]["version"],
}

print(json.dumps(config))
