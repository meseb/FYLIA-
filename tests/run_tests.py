#!/usr/bin/env python3
"""
Script per eseguire tutti i test di FYLIA
"""

import sys
import os

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    """Esegue tutti i test"""
    print("=" * 70)
    print(" " * 20 + "FYLIA - Test Suite")
    print("=" * 70)
    print()
    
    test_modules = [
        'test_mock_provider',
        'test_mapgen',
        'test_patcher'
    ]
    
    all_passed = True
    
    for module_name in test_modules:
        print(f"\n📦 Esecuzione test: {module_name}")
        print("-" * 70)
        
        try:
            module = __import__(module_name)
            
            # Esegui tutte le funzioni di test
            test_functions = [
                name for name in dir(module)
                if name.startswith('test_') and callable(getattr(module, name))
            ]
            
            for test_name in test_functions:
                try:
                    test_func = getattr(module, test_name)
                    test_func()
                    print(f"  ✓ {test_name}")
                except Exception as e:
                    print(f"  ✗ {test_name}: {e}")
                    all_passed = False
            
        except Exception as e:
            print(f"  ✗ Errore nel modulo: {e}")
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ TUTTI I TEST SONO PASSATI!")
    else:
        print("✗ Alcuni test sono falliti")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
