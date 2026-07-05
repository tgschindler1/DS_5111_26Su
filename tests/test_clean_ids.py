#!/usr/bin/env python3
"""Tests for lib.clean_ids: validating and filtering YouTube video IDs from stdin."""

import sys
import io
import platform
import pytest
from lib.clean_ids import main


def test_script_execution(monkeypatch, capsys):
    """A valid ID followed by an invalid one should only emit the valid one."""
    fake_input = io.StringIO("kcFsuxaJ1es\nasd123\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ1es\n"


def test_good_bad_good(monkeypatch, capsys):
    """Valid, invalid, valid sequence should emit only the two valid IDs."""
    fake_input = io.StringIO("kcFsuxaJ1es\nabcd123\nCctJNYYCPo0\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ1es\nCctJNYYCPo0\n"


def test_all_bad(monkeypatch, capsys):
    """All invalid IDs should produce no output."""
    fake_input = io.StringIO("1111\nwoiufads;lkjv;asldkfj\n!!QWERTYUI!!\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_10_char_id(monkeypatch, capsys):
    """A 10-character ID is too short and should be rejected."""
    fake_input = io.StringIO("CctJNYYCPo\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_12_char_id(monkeypatch, capsys):
    """A 12-character ID is too long and should be rejected."""
    fake_input = io.StringIO("CctJNYYCPo00\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


@pytest.mark.skipif(
    platform.system() != "Linux",
    reason="Test assumes Linux-style path separators used in pipeline scripts"
)
def test_running_on_ubuntu():
    """Pipeline scripts assume a Linux runtime environment."""
    assert platform.system() == "Linux"


def test_python_version():
    """Pipeline requires Python 3.8 or newer."""
    assert sys.version_info >= (3, 8)


@pytest.mark.xfail(reason="Decorators are invalid but not yet handled")
def test_decorator_xfail(monkeypatch, capsys):
    """IDs containing spaces are not yet rejected by the validator (known gap)."""
    fake_input = io.StringIO("CctJNY YCPo0\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == "CctJNY YCPo0\n"


@pytest.mark.skip(reason="Empty invalid but not yet handled")
def test_empty_stdin(monkeypatch, capsys):
    """Empty stdin input is not yet handled by the validator (known gap)."""
    fake_input = io.StringIO("")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


@pytest.mark.parametrize("youtube_id, expected", [
    ("CctJNYYCPo0", "CctJNYYCPo0\n"),   # valid
    ("dQw4w9WgXcQ", "dQw4w9WgXcQ\n"),   # valid
    ("aBC123", ""),                     # too short
    ("CctJNYYCPo000", ""),              # too long
    ("kcFsuxaJ!es", ""),                # invalid character
    ("___________", "___________\n"),  # valid: underscores allowed
    ("-----------", "-----------\n"),  # valid: hyphens allowed
])
def test_parametrized_ids(monkeypatch, capsys, youtube_id, expected):
    """Validate a range of ID formats against expected pass/fail behavior."""
    fake_input = io.StringIO(f"{youtube_id}\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == expected
