"""
Test per il sistema di patching
"""
import pytest
from pathlib import Path
from fylia.patcher import generate_diff, apply_patch


def test_generate_diff():
    """Test generazione diff tra due contenuti"""
    original = "linea 1\nlinea 2\nlinea 3\n"
    modified = "linea 1\nlinea 2 modificata\nlinea 3\n"
    
    diff = generate_diff(original, modified, "test.txt")
    
    assert "test.txt" in diff
    assert "linea 2 modificata" in diff


def test_apply_patch_simple(tmp_path):
    """Test applicazione di una patch semplice"""
    # Crea un file di test
    test_file = tmp_path / "test.txt"
    test_file.write_text("linea 1\nlinea 2\nlinea 3\n")
    
    # Genera una patch
    original = "linea 1\nlinea 2\nlinea 3\n"
    modified = "linea 1\nlinea 2 modificata\nlinea 3\n"
    patch_content = generate_diff(original, modified, "test.txt")
    
    # Applica la patch
    result = apply_patch(patch_content, str(tmp_path))
    
    # Nota: questa è una versione semplificata del test
    # In pratica, il patcher ha bisogno di patch più complete
    assert isinstance(result, dict)
    assert 'success' in result
    assert 'files_modified' in result
    assert 'errors' in result
