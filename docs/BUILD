files(name="source", sources=["source/**"])

shell_command(
    name="generate-site",
    execution_dependencies=[":source", "//optimeering_beta:optimeering_beta","//:pyproject"],
    tools=["sphinx-build"],
    command="sphinx-build -M html docs/source generated-site",
    output_files=["generated-site/**"],
    workdir="",
)

run_shell_command(
    name="build-docs",
    execution_dependencies=[":generate-site"],
    command="""rm -rf docs/site
    mkdir docs/site
    cp -r {chroot}/generated-site/html/ docs/site
    """,
    workdir="",
)
