#!/usr/bin/env python3
"""
Script di verifica per FYLIA
Testa tutte le funzionalità principali
"""

import sys
import os

# Aggiungi il percorso src al Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fylia.mapgen import CodeMapGenerator
from fylia.patcher import Patcher
from fylia.providers.mock import MockProvider


def test_map_generator():
    """Test del generatore di mappe"""
    print("🗺️  Testing CodeMapGenerator...")
    generator = CodeMapGenerator()
    mappa = generator.generate_map('.')
    print(mappa)
    print("\n✅ CodeMapGenerator OK\n")


def test_mock_provider():
    """Test del provider mock"""
    print("🤖 Testing MockProvider...")
    provider = MockProvider()
    
    test_inputs = [
        "crea una funzione",
        "scrivi una classe",
        "genera un test",
        "ciao come stai"
    ]
    
    for user_input in test_inputs:
        print(f"\nInput: {user_input}")
        response = provider.generate_response(user_input)
        print(f"Response: {response[:100]}...")
    
    print("\n✅ MockProvider OK\n")


def test_patcher():
    """Test del patcher"""
    print("🔧 Testing Patcher...")
    patcher = Patcher()
    
    # Test diff generation
    old = "def hello():\n    print('Hello')"
    new = "def hello():\n    print('Hello, World!')"
    diff = patcher.generate_diff("test.py", old, new)
    print(f"Diff generato:\n{diff}")
    
    print("\n✅ Patcher OK\n")


def main():
    """Esegue tutti i test"""
    print("="*50)
    print("  FYLIA - Test di verifica")
    print("="*50)
    print()
    
    try:
        test_map_generator()
        test_mock_provider()
        test_patcher()
        
        print("="*50)
        print("  ✅ Tutti i test superati!")
        print("="*50)
        print()
        print("Per testare la TUI, esegui: fylia chat")
        print("Per vedere la mappa, esegui: fylia map .")
        
    except Exception as e:
        print(f"❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
