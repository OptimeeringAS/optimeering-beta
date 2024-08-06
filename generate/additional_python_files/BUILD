python_sources()

files(name="all-files", sources=["**", "!BUILD"])

relocated_files(
    name="additional-python-files",
    files_targets=[":all-files"],
    src="generate/additional_python_files",
    dest="generate/optimeering_beta",
)
