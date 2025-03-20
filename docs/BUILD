files(name="source", sources=["source/**"])

pex_binary(
    name="sphinx",
    dependencies=[
        "//:root#orjson",
        "//:root#sphinx",
        "//:root#pandas",
        "//:root#pydantic",
        "//:root#python-dateutil",
        "//:root#azure-identity",
        "//:root#sphinx-rtd-theme",
        "//:root#setuptools",
        "//:root#toml",
        "//optimeering_beta:optimeering_beta"
    ],
    script="sphinx-build",
)

adhoc_tool(
    name="gen-tool",
    runnable=":sphinx",
    args=["-M", "html", "source", "generated-site"],
    execution_dependencies=[":source", "//:pyproject"],
    output_directories=[""],
    output_files=["generated-site/**"],
)

run_shell_command(
    name="build-docs",
    execution_dependencies=[":gen-tool"],
    command="""rm -rf docs/site
    mkdir docs/site
    cp -r {chroot}/docs/generated-site/html/. docs/site
    """,
    workdir="",
)
