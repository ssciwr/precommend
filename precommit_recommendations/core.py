import copy
import functools
import os
import strictyaml

from pre_commit.git import get_all_files
from identify.identify import tags_from_path


class GenerationContext:
    def __init__(self):
        self._path = os.path.realpath(".")
        self._files = get_all_files()
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
    from precommit_recommendations.rules import _rules

    hooks = []
    for rule in _rules:
        hook = rule(ctx)
        if hook is not None:
            hooks.append(hook)
    return hooks


def generate_config(hooks):
    with open(
        os.path.join(os.path.dirname(__file__), ".pre-commit-config.yaml"), "r"
    ) as f:
        data = strictyaml.load(f.read())

    # NB: The deepcopy's here might seem unnecessary, but they are required
    # because modification of strictyaml objects is a difficult process.
    output = copy.deepcopy(data)

    def _remove_hook(hook_id):
        for i, orepo in enumerate(output["repos"]):
            for j, ohook in enumerate(orepo["hooks"]):
                if ohook.value["id"] == hook_id:
                    del output["repos"][i]["hooks"][j]
                    return

    # Iterate the original data and remove hooks
    for repo in data["repos"]:
        for hook in repo["hooks"]:
            if hook.value["id"] not in hooks:
                _remove_hook(hook.value["id"])

    output2 = copy.deepcopy(output)

    def _remove_repo(repo_url):
        for i, repo in enumerate(output2["repos"]):
            if repo.value["repo"] == repo_url:
                del output2["repos"][i]
                return

    for repo in output["repos"]:
        if len(repo["hooks"].value) == 0:
            _remove_repo(repo.value["repo"])

    return output2
