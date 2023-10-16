import functools
import os

from pre_commit.git import get_all_files
from pre_commit.yaml import yaml_load
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


def parse_hooks():
    with open(
        os.path.join(os.path.dirname(__file__), ".pre-commit-config.yaml"), "r"
    ) as f:
        data = yaml_load(f.read())
    hooks = {}
    for repo in data["repos"]:
        for hook in repo["hooks"]:
            hooks[hook["id"]] = (repo["repo"], repo["rev"], hook)
    return hooks


def add_and_return_repo(data, repo, rev):
    for r in data["repos"]:
        if r["repo"] == repo:
            return r
    data["repos"].append({"repo": repo, "rev": rev})
    return data["repos"][-1]


def generate_config(hooks):
    hookinfo = parse_hooks()
    data = {}
    data["repos"] = []
    for hook in sorted(hooks):
        repo, rev, hookconfig = hookinfo[hook]
        repoconfig = add_and_return_repo(data, repo, rev)
        repoconfig.setdefault("hooks", [])
        repoconfig["hooks"].append(hookconfig)
    return data
