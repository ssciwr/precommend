from precommend.core import (
    collect_hooks,
    generate_config,
    GenerationContext,
)

import click
import os
import ruamel.yaml


@click.command()
def main():
    """Generate a pre-commit config file

    Run at the root of a git repository to generate a pre-commit config file.
    The generated file is based on the contents of your repository and the
    recommendations of the Scientific Software Center at Heidelberg University.
    """
    ctx = GenerationContext()
    config = generate_config(collect_hooks(ctx))
    path = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
    if os.path.exists(path):
        raise IOError("Pre-commit config already present, no upgrade support yet.")

    yaml = ruamel.yaml.YAML()
    with open(path, "w") as f:
        yaml.dump(config, f)


if __name__ == "__main__":
    main()
