# The storage for all our rules
_rules = []


def rule(func):
    """A decorator for rules"""
    _rules.append(func)


@rule
def actionlint(ctx):
    if ctx.directory_exists(".github/workflows"):
        return "actionlint"


@rule
def beautysh(ctx):
    if ctx.tag_exists("bash"):
        return "beautysh"


@rule
def black(ctx):
    if ctx.tag_exists("jupyter"):
        return "black-jupyter"
    if ctx.tag_exists("python"):
        return "black"


@rule
def check_json(ctx):
    if ctx.tag_exists("json"):
        return "check-json"


@rule
def check_dependabot(ctx):
    if ctx.filename_exists(".github/dependabot.yml"):
        return "check-dependabot"


@rule
def check_readthedocs(ctx):
    if ctx.filename_exists(".readthedocs.yml"):
        return "check-readthedocs"


@rule
def check_toml(ctx):
    if ctx.tag_exists("toml"):
        return "check-toml"


@rule
def check_yaml(ctx):
    if ctx.tag_exists("yaml"):
        return "check-yaml"


@rule
def clang_format(ctx):
    if (
        ctx.tag_exists("c++")
        or ctx.tag_exists("c")
        or ctx.tag_exists("c#")
        or ctx.tag_exists("objective-c")
        or ctx.tag_exists("cuda")
    ):
        return "clang-format"


@rule
def cmake_format(ctx):
    if ctx.tag_exists("cmake"):
        return "cmake-format"


@rule
def cmake_lint(ctx):
    if ctx.tag_exists("cmake"):
        return "cmake-lint"


@rule
def end_of_file_fixer(ctx):
    return "end-of-file-fixer"


@rule
def large_files(ctx):
    return "check-added-large-files"


@rule
def mixed_line_ending(ctx):
    return "mixed-line-ending"


@rule
def nbstripout(ctx):
    if ctx.tag_exists("jupyter"):
        return "nbstripout"


@rule
def pretty_format_json(ctx):
    if ctx.tag_exists("json"):
        return "pretty-format-json"


@rule
def requirements_txt_fixer(ctx):
    if ctx.filename_exists("requirements.txt"):
        return "requirements-txt-fixer"


@rule
def setup_cfg_fmt(ctx):
    if ctx.filename_exists("setup.cfg"):
        return "setup-cfg-fmt"


@rule
def trailing_whitespace(ctx):
    return "trailing-whitespace"


@rule
def validate_cff(ctx):
    if ctx.filename_exists("CITATION.cff"):
        return "validate-cff"


@rule
def validate_pyproject(ctx):
    if ctx.filename_exists("pyproject.toml"):
        return "validate-pyproject"
