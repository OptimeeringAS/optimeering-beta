poetry_requirements(
    name="root",
)

python_distribution(
    name="optimeering_beta",
    dependencies=[
        "//optimeering_beta:optimeering_beta",
        ":root#orjson",
    ],
    long_description_path="README.md",
    output_path="optimeering-beta",
    provides=python_artifact(
        name="optimeering_beta",
        version="0.0.7",
        description="Optimeering Python Client (Beta)",
        long_description_content_type="text/markdown",
        author="Optimeering",
        classifiers=[
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
    ),
    wheel_config_settings={"--global-option": ["--python-tag", "py310.py311"]},
)

file(name="pyproject", source="pyproject.toml")

python_sources(
    name="0",
)
