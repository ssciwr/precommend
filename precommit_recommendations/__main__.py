from pre_commit.yaml import yaml_dump
from precommit_recommendations.core import (
    collect_hooks,
    generate_config,
    GenerationContext,
)

import os


def main():
    ctx = GenerationContext()
    config = generate_config(collect_hooks(ctx))
    path = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
    if os.path.exists(path):
        raise IOError("Pre-commit config already present, no upgrade support yet.")

    with open(path, "w") as f:
        f.write(yaml_dump(config))


if __name__ == "__main__":
    main()
