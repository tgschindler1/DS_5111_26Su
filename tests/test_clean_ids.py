#!/usr/bin/env python3 

import sys
import io
import pytest
from lib.clean_ids import main
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
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("kcFsuxaJ1es\nabcd123\nCctJNYYCPo0\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()

    # 3. Capture the printed output
    captured = capsys.readouterr()

    # 4. Assert that the data was modified correctly
    assert captured.out == "kcFsuxaJ1es\nCctJNYYCPo0\n"


def test_all_bad(monkeypatch, capsys):
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("1111\nwoiufads;lkjv;asldkfj\n!!QWERTYUI!!\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()
    captured = capsys.readouterr()

    # 4. Assert that the data was modified correctly
    assert captured.out == ""


def test_10_char_id(monkeypatch, capsys):
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("CctJNYYCPo\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()
    captured = capsys.readouterr()

    # 4. Assert that the data was modified correctly
    assert captured.out == ""


def test_12_char_id(monkeypatch, capsys):
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("CctJNYYCPo00\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()
    captured = capsys.readouterr()

    # 4. Assert that the data was modified correctly
    assert captured.out == ""


@pytest.mark.skipif(
    platform.system() != "Linux",
    reason="Test assumes Linux-style path separators used in pipeline scripts"
)
def test_running_on_ubuntu():
    assert platform.system() == "Linux"


def test_python_version():
    assert sys.version_info >= (3, 8)


@pytest.mark.xfail(reason="Decorators are invalid but not yet handled")
def test_decorator_xfail(monkeypatch, capsys):
    fake_input = io.StringIO("CctJNY YCPo0\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == "CctJNY YCPo0\n"


@pytest.mark.skip(reason="Empty invalid but not yet handled")
def test_empty_stdin(monkeypatch, capsys):
    fake_input = io.StringIO("")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == ""


@pytest.mark.parametrize("youtube_id, expected", [
    ("CctJNYYCPo0", "CctJNYYCPo0\n"),   # valid
    ("dQw4w9WgXcQ", "dQw4w9WgXcQ\n"),   # valid
    ("aBC123", ""),                       # too short
    ("CctJNYYCPo000", ""),                # too long
    ("kcFsuxaJ!es", ""),                 # invalid character
    ("___________", "___________\n"),    # valid: underscores allowed
    ("-----------", "-----------\n"),    # valid: hyphens allowed
])
def test_parametrized_ids(monkeypatch, capsys, youtube_id, expected):
    fake_input = io.StringIO(f"{youtube_id}\n")
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == expected
