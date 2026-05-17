"""Automation tasks for MOOD."""

import shutil
from pathlib import Path

DOIT_CONFIG = {"default_tasks": ["html"]}


def clean_targets(targets):
    """Remove generated files."""
    for target in targets:
        path = Path(target)
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def task_i18n_pot():
    """Extract translation template."""
    return {
        "actions": [
            "pybabel extract -F babel.cfg -o mood/server/po/mood_server.pot .",
        ],
        "file_dep": [
            "babel.cfg",
            *[str(path) for path in Path("mood/server").glob("**/*.py")],
        ],
        "targets": [
            "mood/server/po/mood_server.pot",
        ],
        "clean": True,
    }


def task_i18n_po():
    """Update Russian translation."""
    po_file = "mood/server/po/ru_RU/LC_MESSAGES/mood_server.po"

    return {
        "actions": [
            f"pybabel update -i mood/server/po/mood_server.pot "
            f"-d mood/server/po -D mood_server -l ru_RU",
        ],
        "file_dep": [
            "mood/server/po/mood_server.pot",
        ],
        "targets": [
            po_file,
        ],
    }


def task_i18n_mo():
    """Compile Russian translation."""
    mo_file = "mood/server/po/ru_RU/LC_MESSAGES/mood_server.mo"

    return {
        "actions": [
            "pybabel compile -d mood/server/po -D mood_server",
        ],
        "file_dep": [
            "mood/server/po/ru_RU/LC_MESSAGES/mood_server.po",
        ],
        "targets": [
            mo_file,
        ],
        "clean": True,
    }


def task_i18n():
    """Generate all translation files."""
    return {
        "actions": None,
        "task_dep": [
            "i18n_pot",
            "i18n_po",
            "i18n_mo",
        ],
    }


def task_html():
    """Build HTML documentation."""
    html_dir = "doc/_build/html"

    return {
        "actions": [
            "sphinx-build -M html doc doc/_build",
            "rm -rf mood/documentation",
            "mkdir -p mood/documentation",
            "cp -r doc/_build/html/* mood/documentation/",
        ],
        "file_dep": [
            *[str(path) for path in Path("doc").glob("**/*.rst")],
            *[str(path) for path in Path("mood").glob("**/*.py")],
        ],
        "targets": [
            "mood/documentation/index.html",
        ],
        "clean": True,
    }


def task_test():
    """Run client-server tests."""
    return {
        "actions": [
            "python -m unittest tests/test_server.py",
        ],
        "task_dep": [
            "i18n",
        ],
        "file_dep": [
            *[str(path) for path in Path("mood").glob("**/*.py")],
            *[str(path) for path in Path("tests").glob("**/*.py")],
        ],
    }


def task_wheel():
    """Build wheel package."""
    return {
        "actions": [
            "python -m build --wheel",
        ],
        "task_dep": [
            "i18n",
            "html",
        ],
        "targets": [
            "dist/mood-0.1.0-py3-none-any.whl",
        ],
        "clean": True,
    }


def task_sdist():
    """Build source distribution."""
    return {
        "actions": [
            "python -m build --sdist",
        ],
        "task_dep": [
            "i18n",
            "html",
        ],
        "targets": [
            "dist/mood-0.1.0.tar.gz",
        ],
        "clean": True,
    }

