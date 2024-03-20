from precommend.core import (
    collect_hooks,
    generate_config,
    GenerationContext,
)

import os
import ruamel.yaml


def main():
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
