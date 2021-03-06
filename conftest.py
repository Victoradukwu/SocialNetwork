from glob import glob

pytest_plugins = [
    fixture_file.replace("/", ".").replace(".py", "")
    for fixture_file in glob(
        "src/**/tests/fixtures/[!__]*.py",
        recursive=True
    )
]
