import pytest
from pathlib import Path
from utils.file_ops import ensure_dirs, read_file, write_file, append_file

def test_ensure_dirs(tmp_path):
    dirs = ensure_dirs(tmp_path)
    assert (tmp_path / "raw").exists()
    assert (tmp_path / "wiki").exists()
    assert (tmp_path / "raw" / "assets").exists()

def test_read_write_file(tmp_path):
    file_path = tmp_path / "test.txt"
    write_file(file_path, "content")
    assert read_file(file_path) == "content"

def test_append_file(tmp_path):
    file_path = tmp_path / "test.txt"
    write_file(file_path, "line1\n")
    append_file(file_path, "line2\n")
    assert read_file(file_path) == "line1\nline2\n"
