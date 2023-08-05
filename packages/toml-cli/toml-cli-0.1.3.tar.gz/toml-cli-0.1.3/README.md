# tom-cli

Command line interface for toml files.

This can be usefull for getting or setting parts of a toml file without an editor.
Which can be convinient when values have to be read by a script for example in
continuous development steps.


## Install

`pip install toml-cli`

## Get a value

`toml get --toml-path pyproject.toml tool.poetry.name`

## Set a value

`toml set --toml-path pyproject.toml tool.poetry.version 0.2.0`

## Add a section

`toml add_section --toml-path pyproject.toml tool.poetry.new_section`

## Unset a value

`toml unset --toml-path pyproject.toml tool.poetry.version`
