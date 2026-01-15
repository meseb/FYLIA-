#!/usr/bin/env python3
"""
Script helper per avviare FYLIA senza installazione
Utile per test e sviluppo
"""

import sys
import os

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fylia.cli import main

if __name__ == '__main__':
    main()
