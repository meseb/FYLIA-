"""Test per il patcher"""

import pytest
from pathlib import Path
import tempfile
import os
from fylia.patcher import Patcher


def test_patcher_creation():
    """Test creazione del patcher"""
    patcher = Patcher()
    assert patcher is not None


def test_create_file():
    """Test creazione file"""
    patcher = Patcher()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        content = "Hello, world!"
        
        result = patcher.create_file(str(test_file), content)
        
        assert result is True
        assert test_file.exists()
        assert test_file.read_text() == content


def test_modify_file():
    """Test modifica file"""
    patcher = Patcher()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("Hello, world!")
        
        result = patcher.modify_file(
            str(test_file), 
            "world", 
            "Python"
        )
        
        assert result is True
        assert test_file.read_text() == "Hello, Python!"


def test_delete_file():
    """Test eliminazione file"""
    patcher = Patcher()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("Test content")
        
        assert test_file.exists()
        
        result = patcher.delete_file(str(test_file))
        
        assert result is True
        assert not test_file.exists()


def test_generate_diff():
    """Test generazione diff"""
    patcher = Patcher()
    
    old = "line 1\nline 2\nline 3"
    new = "line 1\nmodified line 2\nline 3"
    
    diff = patcher.generate_diff("test.txt", old, new)
    
    assert isinstance(diff, str)
    assert "test.txt" in diff
    assert "-" in diff
    assert "+" in diff
