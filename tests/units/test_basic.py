"""Basic unit tests for ansible-creator."""

from pathlib import Path

import pytest

from ansible_creator.cli import Cli
from ansible_creator.config import Config
from ansible_creator.output import Output
from ansible_creator.utils import TermFeatures, expand_path


def test_expand_path() -> None:
    """Test expand_path utils."""
    assert (
        expand_path("~/$DEV_WORKSPACE/namespace/collection")
        == "/home/ansible/collections/ansible_collections/namespace/collection"
    )


@pytest.mark.parametrize(
    argnames=["sysargs", "expected"],
    argvalues=[
        [
            ["ansible-creator", "init", "testorg.testcol"],
            {
                "subcommand": "init",
                "no_ansi": False,
                "log_file": str(Path.cwd() / "ansible-creator.log"),
                "log_level": "notset",
                "log_append": "true",
                "json": False,
                "verbose": 0,
                "collection": "testorg.testcol",
                "init_path": "./",
                "force": False,
                "project": "collection",  # default value
                "scm_org": None,
                "scm_project": None,
            },
        ],
        [
            [
                "ansible-creator",
                "init",
                "--project=ansible-project",
                "--init-path=/home/ansible/my-ansible-project",
            ],
            {
                "subcommand": "init",
                "no_ansi": False,
                "log_file": str(Path.cwd() / "ansible-creator.log"),
                "log_level": "notset",
                "log_append": "true",
                "json": False,
                "verbose": 0,
                "collection": None,
                "init_path": "/home/ansible/my-ansible-project",
                "force": False,
                "project": "ansible-project",
                "scm_org": None,
                "scm_project": None,
            },
        ],
        [
            [
                "ansible-creator",
                "init",
                "testorg.testcol",
                "--init-path=/home/ansible",
                "-vvv",
                "--json",
                "--no-ansi",
                "--la=false",
                "--lf=test.log",
                "--ll=debug",
                "--force",
            ],
            {
                "subcommand": "init",
                "no_ansi": True,
                "log_file": "test.log",
                "log_level": "debug",
                "log_append": "false",
                "json": True,
                "verbose": 3,
                "collection": "testorg.testcol",
                "init_path": "/home/ansible",
                "force": True,
                "project": "collection",  # default value
                "scm_org": None,
                "scm_project": None,
            },
        ],
        [
            [
                "ansible-creator",
                "init",
                "--project=ansible-project",
                "--scm-org=weather",
                "--scm-project=demo",
                "--init-path=/home/ansible/my-ansible-project",
                "-vvv",
                "--json",
                "--no-ansi",
                "--la=false",
                "--lf=test.log",
                "--ll=debug",
                "--force",
            ],
            {
                "subcommand": "init",
                "no_ansi": True,
                "log_file": "test.log",
                "log_level": "debug",
                "log_append": "false",
                "json": True,
                "verbose": 3,
                "collection": None,
                "init_path": "/home/ansible/my-ansible-project",
                "force": True,
                "project": "ansible-project",
                "scm_org": "weather",
                "scm_project": "demo",
            },
        ],
    ],
)
def test_cli_parser(monkeypatch, sysargs, expected) -> None:
    """Test CLI args parsing."""
    monkeypatch.setattr("sys.argv", sysargs)
    assert vars(Cli().parse_args()) == expected


def test_configuration_class(output: Output) -> None:
    """Test Config() dataclass post_init."""
    cli_args: dict = {
        "creator_version": "0.0.1",
        "json": True,
        "log_append": True,
        "log_file": "./ansible-creator.log",
        "log_level": "debug",
        "no_ansi": False,
        "output": output,
        "subcommand": "init",
        "verbose": 2,
        "collection": "testorg.testcol",
        "init_path": "$HOME",
    }
    app_config = Config(**cli_args)
    assert app_config.namespace == "testorg"
    assert app_config.collection_name == "testcol"
    assert app_config.init_path == "/home/ansible"
