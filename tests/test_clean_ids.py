#!/usr/bin/env python3 

import sys
import io
import pytest
from lab2.clean_ids import main
import platform

def test_script_execution(monkeypatch, capsys):
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("kcFsuxaJ1es\nasd123\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()

    # 3. Capture the printed output
    captured = capsys.readouterr()
    
    # 4. Assert that the data was modified correctly
    assert captured.out == "kcFsuxaJ1es\n"

def test_good_bad_good(monkeypatch, capsys):
    """Valid id, bad line, valid id — both valid ids should print."""
    fake_input = io.StringIO("kcFsuxaJ1es\nasd123\ndQw4w9WgXcQ\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ1es\ndQw4w9WgXcQ\n"


def test_all_bad_lines(monkeypatch, capsys):
    """All invalid ids — nothing should print."""
    fake_input = io.StringIO("tooshort\nwaytoolongtobevalid\n!!invalid!!\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_10_char_id_invalid(monkeypatch, capsys):
    """10 character id should be rejected (too short)."""
    fake_input = io.StringIO("kcFsuxaJ1e\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_12_char_id_invalid(monkeypatch, capsys):
    """12 character id should be rejected (too long)."""
    fake_input = io.StringIO("kcFsuxaJ1esX\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_running_on_ubuntu():
    """Check that the code is running on Ubuntu."""
    assert platform.system() == "Linux"
    assert "ubuntu" in platform.version().lower()


def test_python_version():
    """Check that Python 3.8 or higher is being used."""
    assert sys.version_info >= (3, 8)


@pytest.mark.xfail(reason="Special characters should be invalid but not yet handled")
def test_special_characters_xfail(monkeypatch, capsys):
    """Expected to fail: special chars like spaces are not yet explicitly handled."""
    fake_input = io.StringIO("kcFsuxaJ 1e\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ 1e\n"


@pytest.mark.skip(reason="Empty stdin handling not yet implemented")
def test_empty_stdin(monkeypatch, capsys):
    """Skipped: behaviour for completely empty stdin not yet defined."""
    fake_input = io.StringIO("")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


@pytest.mark.parametrize("youtube_id, expected", [
    ("kcFsuxaJ1es", "kcFsuxaJ1es\n"),   # valid
    ("dQw4w9WgXcQ", "dQw4w9WgXcQ\n"),   # valid
    ("asd123", ""),                       # too short
    ("kcFsuxaJ1esX", ""),                # too long
    ("kcFsuxaJ!es", ""),                 # invalid character
    ("___________", "___________\n"),    # valid: underscores allowed
    ("-----------", "-----------\n"),    # valid: hyphens allowed
])
def test_parametrized_ids(monkeypatch, capsys, youtube_id, expected):
    """Parametrized test covering a range of valid and invalid ids."""
    fake_input = io.StringIO(f"{youtube_id}\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == expected
