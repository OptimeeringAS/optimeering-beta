python_sources()

#### CREATE OPENAPI SCHEMA ####
python_source(
    name="fix-openapi-extensions",
    source="fix_openapi_extensions.py"
)

# curl -L https://beta.optimeering.com/api/docs/openapi_public.json | tee >(wc -c) >(shasum -a 256) >/dev/null
resource(
    name="openapi-schema",
    source=http_source(
        url="https://beta.optimeering.com/api/docs/openapi_public.json",
        sha256="b8d479c9cb6ab6fa966d99f2cc452689f64101f535e9335b5bb949394a746efe",
        len=34822
    )
)

adhoc_tool(
    name="run-fix-openapi-extensions",
    runnable=":fix-openapi-extensions",
    args=[
        "-s",
        "openapi_public.json"
    ],
    execution_dependencies=[
        ":openapi-schema",
    ],
    stdout="generate/openapi.json",
    root_output_directory=".",
)

#### CREATE GENERATOR CONFIG ####
python_source(
    name="create-config",
    source="create_config.py",
    dependencies=[
        "//:pyproject"
    ]
)

adhoc_tool(
    name="run-create-config",
    runnable=":create-config",
    stdout="generate/config.json",
    root_output_directory=".",
)

#### GENERATE CLIENT ####
files(
    name="generator-files",
    sources=["python_templates/**", "generation_config.json"]
)

# Specify JAR dependencies
jvm_artifact(
    name="openapi-generator",
    group="org.openapitools",
    artifact="openapi-generator-cli",
    version="7.7.0",
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
    execution_dependencies=[":generator"]
)
