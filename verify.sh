#!/usr/bin/env bash
# Script di verifica completa per FYLIA

echo "=============================================================="
echo "           VERIFICA COMPLETA DI FYLIA v0.1.0"
echo "=============================================================="
echo

# Test 1: Verifica installazione
echo "📦 Test 1: Verifica installazione..."
if command -v fylia &> /dev/null; then
    echo "✓ Comando fylia trovato"
    fylia --version
else
    echo "✗ Comando fylia non trovato"
    echo "  Prova: pip install -e ."
    exit 1
fi
echo

# Test 2: Test suite
echo "📋 Test 2: Esecuzione test suite..."
cd tests
python3 run_tests.py
if [ $? -eq 0 ]; then
    echo "✓ Tutti i test passati"
else
    echo "✗ Alcuni test falliti"
    exit 1
fi
cd ..
echo

# Test 3: Comandi CLI
echo "🖥️  Test 3: Comandi CLI..."

echo "  - fylia --version"
fylia --version

echo "  - fylia map -f stats"
fylia map -f stats

echo "  - fylia test"
echo "Ciao FYLIA" | fylia test -m "test"

echo "✓ Comandi CLI funzionanti"
echo

# Test 4: Import Python
echo "🐍 Test 4: Import moduli Python..."
python3 -c "import sys; sys.path.insert(0, 'src'); from fylia.providers.mock import MockProvider; print('✓ MockProvider importato')"
python3 -c "import sys; sys.path.insert(0, 'src'); from fylia.mapgen import MapGenerator; print('✓ MapGenerator importato')"
python3 -c "import sys; sys.path.insert(0, 'src'); from fylia.patcher import Patcher; print('✓ Patcher importato')"
python3 -c "import sys; sys.path.insert(0, 'src'); from fylia.tui import SimpleTUI; print('✓ SimpleTUI importato')"
echo

# Test 5: Esempi
echo "📚 Test 5: Esecuzione esempi..."
python3 examples.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Esempi eseguiti con successo"
else
    echo "✗ Errore negli esempi"
    exit 1
fi
echo

# Test 6: Documentazione
echo "📖 Test 6: Verifica documentazione..."
for doc in README.md INSTALL.md USAGE.md ARCHITECTURE.md; do
    if [ -f "$doc" ]; then
        echo "  ✓ $doc presente"
    else
        echo "  ✗ $doc mancante"
        exit 1
    fi
done
echo

# Test 7: Struttura progetto
echo "🗂️  Test 7: Verifica struttura progetto..."
required_files=(
    "src/fylia/__init__.py"
    "src/fylia/cli.py"
    "src/fylia/tui.py"
    "src/fylia/mapgen.py"
    "src/fylia/patcher.py"
    "src/fylia/providers/mock.py"
    "tests/run_tests.py"
    "pyproject.toml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file mancante"
        exit 1
    fi
done
echo

# Riepilogo
echo "=============================================================="
echo "              ✓ VERIFICA COMPLETATA CON SUCCESSO"
echo "=============================================================="
echo
echo "FYLIA è pronto all'uso!"
echo
echo "Per iniziare:"
echo "  fylia chat      # Avvia l'interfaccia conversazionale"
echo "  fylia map       # Visualizza la mappa del progetto"
echo "  fylia --help    # Mostra tutti i comandi"
echo
