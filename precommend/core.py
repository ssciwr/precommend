import functools
import os
import ruamel.yaml
import subprocess

from identify.identify import tags_from_path


class NotAGitRepositoryError(Exception):
    """Raised when the current directory is not a Git repository."""


def get_all_files():
    """Yield tracked + untracked-but-unignored files in a Git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip() != "true":
            raise NotAGitRepositoryError(
                f"precommend needs to be run in a Git repository"
            )
    except subprocess.CalledProcessError:
        raise NotAGitRepositoryError(f"precommend needs to be run in a Git repository")

    # Tracked files
    tracked = subprocess.Popen(
        ["git", "ls-files", "--cached"],
        stdout=subprocess.PIPE,
        text=True,
    )
    for line in tracked.stdout:
        yield line.strip()

    tracked.wait()

    # Untracked but unignored files
    untracked = subprocess.Popen(
        ["git", "ls-files", "--others", "--exclude-standard"],
        stdout=subprocess.PIPE,
        text=True,
    )
    for line in untracked.stdout:
        yield line.strip()

    untracked.wait()


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
