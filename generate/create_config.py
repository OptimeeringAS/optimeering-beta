import json

import toml

pyprojet = toml.load("../pyproject.toml")

config = {
    "packageName": "optimeering_beta",
    "projectName": "Optimeering Python Client",
    "generateSourceCodeOnly": True,
    "packageVersion": pyprojet["tool"]["poetry"]["version"],
}

print(json.dumps(config))
