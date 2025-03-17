python_sources()

#### CREATE OPENAPI SCHEMA ####
python_source(name="fix-openapi-extensions", source="fix_openapi_extensions.py")

# To get the SHA and the length, use the following command
# curl -L https://beta.optimeering.com/api/docs/openapi.json | tee >(wc -c) >(shasum -a 256) >/dev/null
resource(
    name="openapi-schema",
    source=http_source(
        url="https://beta.optimeering.com/api/docs/openapi.json",
        sha256="78e82a41335ceb84842ed9d7778f05811a4d1e47126080166374b2fa26d827a6",
        len=109337,
    ),
)
# resource(name="openapi-schema", source="openapi.json")

adhoc_tool(
    name="run-fix-openapi-extensions",
    runnable=":fix-openapi-extensions",
    args=["-s", "openapi.json"],
    execution_dependencies=[
        ":openapi-schema",
    ],
    stdout="generate/openapi.json",
    root_output_directory=".",
)

#### CREATE GENERATOR CONFIG ####
python_source(name="create-config", source="create_config.py", dependencies=["//:pyproject"])

adhoc_tool(
    name="run-create-config",
    runnable=":create-config",
    stdout="generate/config.json",
    root_output_directory=".",
)

#### GENERATE CLIENT ####
files(name="generator-files", sources=["python_templates/**"])

# Specify JAR dependencies
jvm_artifact(
    name="openapi-generator",
    group="org.openapitools",
    artifact="openapi-generator-cli",
    version="7.10.0",
)

adhoc_tool(
    name="generator",
    runnable=":openapi-generator",
    args=[
        "generate",
        "-i",
        "openapi.json",
        "--template-dir",
        "python_templates",
        "--config",
        "config.json",
        "--skip-validate-spec",
        "-g",
        "python",
        "-o",
        "./",
    ],
    execution_dependencies=[
        ":run-fix-openapi-extensions",
        ":run-create-config",
        ":generator-files",
        "//generate/additional_python_files:additional-python-files",
    ],
    output_directories=[
        "./optimeering_beta",
    ],
    workdir=".",
    root_output_directory=".",
)

shell_command(
    name="run-generator",
    command="echo Generated client",
    execution_dependencies=[":generator"],
    output_directories=[
        "./optimeering_beta",
    ],
)

run_shell_command(
    name="generate-client",
    command="""rm -rf ../optimeering_beta
        mkdir ../optimeering_beta
        cp -r {chroot}/optimeering_beta ../
        rm -rf ../optimeering_beta/docs ../optimeering_beta/test
    """,
    execution_dependencies=[":generator"],
)
