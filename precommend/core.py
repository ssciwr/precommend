import copy
import functools
import os
import ruamel.yaml

from pre_commit.git import get_all_files
from identify.identify import tags_from_path


class GenerationContext:
    def __init__(self):
        self._path = os.path.realpath(".")
        # We use get_all_files from pre-commit as it respects .gitignore, but
        # we need to filter out files that do not exist in the working copy.
        self._files = [f for f in get_all_files() if os.path.exists(f)]
        self._tags = functools.reduce(
            lambda a, b: a.union(b), map(tags_from_path, self._files), set()
        )

    def tag_exists(self, tag):
        return tag in self._tags

    def filename_exists(self, filename):
        return filename in self._files

    def directory_exists(self, directory):
        for filename in self._files:
            if filename.startswith(directory):
                return True
        return False


def collect_hooks(ctx):
    from precommend.rules import _rules

    hooks = []
    for rule in _rules:
        hook = rule(ctx)
        if hook is not None:
            hooks.append(hook)
    return hooks


def generate_config(hooks):
    # Load all available hooks
    yaml = ruamel.yaml.YAML()
    with open(
        os.path.join(os.path.dirname(__file__), ".pre-commit-config.yaml"), "r"
    ) as f:
        data = yaml.load(f)

    # Ruamel types to use in constructing the output
    CS = ruamel.yaml.comments.CommentedSeq
    CM = ruamel.yaml.comments.CommentedMap

    # The output data structure
    final = CM(repos=CS())
    for repo in data["repos"]:
        # If no hook of this repo matches, it is never added to the output
        if set(h["id"] for h in repo["hooks"]).intersection(hooks):
            repo_hooks = repo.pop("hooks")
            hook_list = CS()
            for hook in repo_hooks:
                if hook["id"] in hooks:
                    hook_list.append(hook)

            repo_map = CM(**repo)
            repo_map["hooks"] = hook_list
            final["repos"].append(repo_map)

    return final
