"""
Test per il generatore di mappa concettuale
"""
import pytest
from pathlib import Path
from fylia.mapgen import generate_map, parse_python_file, get_file_icon


def test_generate_map_invalid_path():
    """Test che la mappa gestisca percorsi non validi"""
    result = generate_map("/percorso/non/esistente")
    assert "Errore" in result


def test_generate_map_current_directory():
    """Test generazione mappa per directory corrente"""
    result = generate_map(".")
    assert "MAPPA PROGETTO" in result
    assert "Struttura File:" in result


def test_get_file_icon():
    """Test icone per diversi tipi di file"""
    assert get_file_icon('.py') == '🐍'
    assert get_file_icon('.md') == '📝'
    assert get_file_icon('.txt') == '📄'
    assert get_file_icon('.unknown') == '📄'


def test_parse_python_file(tmp_path):
    """Test parsing di un file Python"""
    # Crea un file Python di test
    test_file = tmp_path / "test.py"
    test_file.write_text("""
def test_function():
    pass

class TestClass:
    def method1(self):
        pass
    
    def method2(self):
        pass
""")
    
    result = parse_python_file(test_file)
    
    # Verifica che funzioni e classi siano state trovate
    result_text = "\n".join(result)
    assert "test_function" in result_text
    assert "TestClass" in result_text
    assert "method1" in result_text
    assert "method2" in result_text
