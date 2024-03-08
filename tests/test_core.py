from precommend.core import *


def test_collect_hooks_python(monkeypatch, python_data):
    monkeypatch.chdir(python_data)
    ctx = GenerationContext()
    print(ctx._files)
    hooks = collect_hooks(ctx)

    assert "black" in hooks
    assert "validate-pyproject" in hooks


def test_collect_hooks_cpp(monkeypatch, cpp_data):
    monkeypatch.chdir(cpp_data)
    ctx = GenerationContext()
    hooks = collect_hooks(ctx)

    assert "clang-format" in hooks
    assert "cmake-format" in hooks


def test_generate_config_python(monkeypatch, tmp_path, python_data):
    monkeypatch.chdir(python_data)
    ctx = GenerationContext()
    hooks = collect_hooks(ctx)

    monkeypatch.chdir(str(tmp_path))
    output = generate_config(hooks).as_yaml()

    assert "black" in output
    assert "validate-pyproject" in output


def test_generate_config_python(monkeypatch, tmp_path, cpp_data):
    monkeypatch.chdir(cpp_data)
    ctx = GenerationContext()
    hooks = collect_hooks(ctx)

    monkeypatch.chdir(str(tmp_path))
    output = generate_config(hooks).as_yaml()

    assert "clang-format" in output
    assert "cmake-format" in output
