poetry_requirements(
    name="root",
)

python_distribution(
    name="optimeering_beta",
    dependencies=[
        "//optimeering_beta:optimeering_beta",
    ],
    output_path="optimeering-beta",
    provides=python_artifact(
        name="optimeering_beta",
        version="0.0.2",
        description="Optimeering Python Client (Beta)",
        author="Optimeering",
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
    ),
    wheel_config_settings={"--global-option": ["--python-tag", "py37.py38.py39.py310.py311"]},
    repositories=["@optimeering"],
    tags=["client"],
)
