# Architettura di FYLIA

## Panoramica

FYLIA è organizzata in moduli separati per garantire chiarezza, manutenibilità ed estensibilità.

```
FYLIA
├── CLI Layer         (cli.py)
├── TUI Layer         (tui.py)
└── Core Components
    ├── Providers     (providers/)
    ├── MapGen        (mapgen.py)
    └── Patcher       (patcher.py)
```

## Componenti Principali

### 1. CLI (`cli.py`)

**Responsabilità:** Entry point del programma, gestione argomenti della riga di comando

**Comandi:**
- `fylia chat` → Avvia la TUI
- `fylia map` → Genera mappa del progetto
- `fylia test` → Testa il provider
- `fylia version` → Mostra versione

**Funzioni principali:**
- `main()` - Entry point, parsing argomenti
- `cmd_chat()` - Gestisce comando chat
- `cmd_map()` - Gestisce comando map
- `cmd_test()` - Gestisce comando test

**Design Pattern:** Command Pattern

### 2. TUI (`tui.py`)

**Responsabilità:** Interfaccia utente testuale, gestione interazione utente

**Caratteristiche:**
- Loop principale di interazione
- Gestione comandi speciali (`/map`, `/stats`, etc.)
- Integrazione con Provider, MapGen e Patcher
- Applicazione interattiva di patch

**Classi:**
- `SimpleTUI` - Interfaccia testuale semplificata

**Metodi chiave:**
- `start()` - Avvia l'interfaccia
- `_main_loop()` - Loop principale
- `_handle_command()` - Gestisce comandi speciali
- `_handle_message()` - Gestisce messaggi utente

**Design Pattern:** MVC (Model-View-Controller)

### 3. Providers (`providers/`)

**Responsabilità:** Astrarre l'interazione con modelli AI

**Struttura:**
```
providers/
├── __init__.py
└── mock.py      # MockProvider - per test senza API
```

**Provider Interface (implicito):**
```python
class Provider:
    def chat(message: str) -> str
    def get_history() -> list
    def clear_history() -> None
```

**MockProvider:**
- Simula risposte AI basate su keyword
- Nessuna dipendenza esterna
- Ideale per sviluppo e test

**Estensioni future:**
- `openai.py` - Integrazione OpenAI
- `anthropic.py` - Integrazione Anthropic
- `local.py` - Modelli locali (ollama, etc.)

**Design Pattern:** Strategy Pattern

### 4. MapGen (`mapgen.py`)

**Responsabilità:** Analisi codice Python e generazione mappe concettuali

**Classi:**
- `CodeNode` - Nodo dell'albero di codice
- `MapGenerator` - Generatore di mappe

**Funzionalità:**
- Scansione ricorsiva directory
- Parsing AST di file Python
- Estrazione classi, funzioni, metodi
- Formattazione output (tree, stats, json)

**CodeNode:**
```python
class CodeNode:
    - name: str           # Nome dell'elemento
    - node_type: str      # 'file', 'class', 'function', etc.
    - line_number: int    # Riga nel file
    - children: list      # Nodi figli
```

**MapGenerator metodi:**
- `generate_map()` - Genera mappa completa
- `_scan_directory()` - Scansiona directory
- `_analyze_python_file()` - Analizza file Python
- `format_tree()` - Formatta come albero
- `get_summary()` - Statistiche

**Tecnologie:**
- `ast` module - Parsing Python
- `pathlib` - Gestione percorsi

**Design Pattern:** Composite Pattern (per CodeNode tree)

### 5. Patcher (`patcher.py`)

**Responsabilità:** Gestione modifiche al codice, diff, patch

**Classe:**
- `Patcher` - Gestione patch e diff

**Funzionalità:**
- Creazione diff unificati
- Applicazione patch con backup
- Estrazione blocchi codice da markdown
- Parsing istruzioni file
- Formattazione diff con colori ANSI

**Metodi chiave:**
- `create_diff()` - Crea diff tra due versioni
- `apply_patch()` - Applica modifiche a file
- `preview_changes()` - Anteprima modifiche
- `extract_code_blocks()` - Estrae codice da markdown
- `parse_file_instruction()` - Trova istruzioni file
- `format_diff_for_display()` - Formatta per visualizzazione

**Tecnologie:**
- `difflib` - Generazione diff

**Design Pattern:** Facade Pattern

## Flusso di Dati

### Scenario: Chat Interattiva

```
1. Utente esegue: fylia chat
   └→ CLI.main() → cmd_chat() → TUI.run_tui()

2. TUI si avvia
   └→ SimpleTUI.__init__()
   └→ Crea: MockProvider, MapGenerator, Patcher
   └→ Genera mappa iniziale

3. Loop principale
   ┌─→ Utente inserisce messaggio
   │   └→ TUI._handle_message()
   │       └→ Provider.chat(message)
   │       └→ Patcher.parse_file_instruction()
   │       └→ Se trovato: Patcher.preview_changes()
   │       └→ Conferma utente
   │       └→ Patcher.apply_patch()
   │       └→ MapGen.generate_map() [refresh]
   └─── Ritorna al loop
```

### Scenario: Generazione Mappa

```
1. Utente esegue: fylia map
   └→ CLI.main() → cmd_map()

2. MapGenerator.generate_map()
   └→ Crea CodeNode radice
   └→ _scan_directory(root)
       ├→ Per ogni item:
       │  ├─ Directory → ricorsione
       │  └─ File .py → _analyze_python_file()
       │      └→ ast.parse()
       │      └→ Estrae classi e funzioni
       │      └→ Crea CodeNode per ognuno

3. Formattazione output
   └→ format_tree() / get_summary() / to_dict()
```

## Principi di Design

### 1. Separazione delle Responsabilità
Ogni modulo ha un compito chiaro e definito.

### 2. Dependency Injection
I componenti ricevono le dipendenze nel costruttore:
```python
class SimpleTUI:
    def __init__(self, root_path: str = '.'):
        self.provider = MockProvider()
        self.mapgen = MapGenerator(root_path)
        self.patcher = Patcher(root_path)
```

### 3. Interfacce Implicite
Python usa duck typing, ma manteniamo contratti chiari:
```python
# Tutti i provider devono implementare:
def chat(message: str) -> str
```

### 4. Modularità
Ogni componente può essere usato indipendentemente:
```python
# Usa solo MapGen
from fylia.mapgen import MapGenerator
mapgen = MapGenerator('.')
mappa = mapgen.generate_map()
```

### 5. Estensibilità
Facile aggiungere nuovi provider:
```python
# providers/openai.py
class OpenAIProvider:
    def chat(self, message: str) -> str:
        # Implementazione OpenAI
        pass
```

## Struttura File

```
FYLIA-/
├── src/fylia/              # Package principale
│   ├── __init__.py         # Info package
│   ├── cli.py              # CLI entry point
│   ├── tui.py              # TUI interface
│   ├── mapgen.py           # Map generator
│   ├── patcher.py          # Patch manager
│   └── providers/          # AI providers
│       ├── __init__.py
│       └── mock.py         # Mock provider
│
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── run_tests.py        # Test runner
│   ├── test_mock_provider.py
│   ├── test_mapgen.py
│   └── test_patcher.py
│
├── pyproject.toml          # Package config
├── requirements.txt        # Dependencies
├── fylia.py                # Dev launcher
├── examples.py             # Usage examples
│
├── README.md               # Main documentation
├── INSTALL.md              # Installation guide
├── USAGE.md                # Usage guide
└── ARCHITECTURE.md         # This file
```

## Tecnologie e Dipendenze

### Standard Library Only
FYLIA usa **solo** la libreria standard Python:
- `argparse` - Parsing CLI arguments
- `ast` - Parsing Python code
- `difflib` - Diff generation
- `pathlib` - Path manipulation
- `sys`, `os` - System operations

### Nessuna Dipendenza Esterna (v0.1.0)
- ✅ Funziona ovunque ci sia Python 3.7+
- ✅ Nessun `pip install` di librerie esterne
- ✅ Ideale per Termux con connessione limitata

### Dipendenze Opzionali Future
- `rich` - TUI avanzata con colori e layout
- `textual` - Framework TUI moderno
- `openai` - Integrazione OpenAI
- `anthropic` - Integrazione Anthropic

## Testing

### Strategia di Test
- **Unit tests** per ogni modulo
- **Integration tests** per flussi completi
- **Manual testing** per TUI

### Esecuzione Test
```bash
cd tests
python3 run_tests.py
```

### Coverage
- MockProvider: 100%
- MapGen: 90%+
- Patcher: 90%+

## Estensioni Future

### 1. Provider Reali
```python
# providers/openai.py
class OpenAIProvider:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
```

### 2. TUI Avanzata
```python
# tui_rich.py - con Rich/Textual
class AdvancedTUI:
    # Pannelli side-by-side
    # Syntax highlighting
    # Mouse support
```

### 3. Git Integration
```python
# git_manager.py
class GitManager:
    def auto_commit()
    def create_branch()
    def show_diff()
```

### 4. Plugin System
```python
# plugins/
class PluginInterface:
    def on_message()
    def on_file_change()
```

## Contribuire

Per contribuire all'architettura:
1. Mantieni la separazione dei moduli
2. Usa solo standard library per core
3. Estendi via plugin/provider pattern
4. Documenta le modifiche

## Contatti

- Repository: https://github.com/meseb/FYLIA-
- Issues: https://github.com/meseb/FYLIA-/issues
