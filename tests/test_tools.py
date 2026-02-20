"""Tests for life4a4 tool functions."""

import os
import tempfile

import pytest

from life4a4.tools import list_files, read_file, run_command, write_file


# ---------------------------------------------------------------------------
# read_file / write_file
# ---------------------------------------------------------------------------


def test_write_and_read_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "hello.txt")
        result = write_file(path, "hello world")
        assert "Successfully" in result
        assert read_file(path) == "hello world"


def test_write_creates_parent_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "sub", "dir", "file.txt")
        result = write_file(path, "nested")
        assert "Successfully" in result
        assert read_file(path) == "nested"


def test_read_nonexistent_file():
    result = read_file("/tmp/life4a4_nonexistent_file_xyz.txt")
    assert result.startswith("Error")


# ---------------------------------------------------------------------------
# run_command
# ---------------------------------------------------------------------------


def test_run_command_stdout():
    result = run_command("echo hello")
    assert "hello" in result


def test_run_command_nonzero_exit():
    result = run_command("exit 1", timeout=5)
    assert "Exit code" in result or "1" in result


def test_run_command_stderr():
    result = run_command("echo err >&2", timeout=5)
    assert "err" in result


def test_run_command_timeout():
    result = run_command("sleep 60", timeout=1)
    assert "timed out" in result


# ---------------------------------------------------------------------------
# list_files
# ---------------------------------------------------------------------------


def test_list_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        write_file(os.path.join(tmpdir, "a.txt"), "")
        write_file(os.path.join(tmpdir, "b.txt"), "")
        result = list_files(tmpdir)
        assert "a.txt" in result
        assert "b.txt" in result


def test_list_files_shows_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "mydir"))
        result = list_files(tmpdir)
        assert "mydir/" in result


def test_list_files_nonexistent():
    result = list_files("/tmp/life4a4_nonexistent_dir_xyz")
    assert result.startswith("Error")


def test_list_files_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = list_files(tmpdir)
        assert result == "(empty directory)"
