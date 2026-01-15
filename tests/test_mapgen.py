"""Test per il generatore di mappe"""

import pytest
from pathlib import Path
from fylia.mapgen import CodeMapGenerator


def test_map_generator_creation():
    """Test creazione del generatore"""
    generator = CodeMapGenerator()
    assert generator is not None
    assert hasattr(generator, 'generate_map')


def test_generate_map_current_dir():
    """Test generazione mappa per directory corrente"""
    generator = CodeMapGenerator()
    mappa = generator.generate_map('.')
    
    assert isinstance(mappa, str)
    assert 'MAPPA PROGETTO' in mappa
    assert '📁 Struttura File:' in mappa


def test_generate_map_nonexistent():
    """Test con directory non esistente"""
    generator = CodeMapGenerator()
    mappa = generator.generate_map('/path/che/non/esiste')
    
    assert '❌' in mappa
    assert 'non trovato' in mappa.lower()


def test_file_icon():
    """Test icone per tipi di file"""
    generator = CodeMapGenerator()
    
    assert generator._get_file_icon('test.py') == '🐍'
    assert generator._get_file_icon('README.md') == '📝'
    assert generator._get_file_icon('config.json') == '📋'
