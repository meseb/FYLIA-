# Installazione e Uso di FYLIA

## Installazione

### In Termux (Android)

```bash
# Installa Python se non già presente
pkg install python

# Clona il repository
git clone https://github.com/meseb/FYLIA-.git
cd FYLIA-

# Installa FYLIA in modalità sviluppo
pip install -e .
```

### In ambiente normale

```bash
# Clona il repository
git clone https://github.com/meseb/FYLIA-.git
cd FYLIA-

# Installa FYLIA
pip install -e .
```

## Uso

### Avvia l'interfaccia conversazionale

```bash
fylia chat
```

Questo avvia la TUI (Text User Interface) che permette di:
- Conversare con FYLIA in italiano
- Vedere la mappa del progetto
- Applicare modifiche al codice

### Comandi disponibili nella TUI

- `/map` - Mostra la mappa del progetto
- `/stats` - Mostra statistiche del progetto
- `/refresh` - Rigenera la mappa del progetto
- `/help` - Mostra l'aiuto
- `/exit` - Esci da FYLIA

### Genera la mappa del progetto

```bash
# Formato albero (default)
fylia map

# Solo statistiche
fylia map -f stats

# Formato JSON
fylia map -f json

# Specifica un percorso diverso
fylia map -p /path/to/project
```

### Testa il provider

```bash
# Con messaggio inline
fylia test -m "Crea una funzione"

# Legge da stdin
echo "Crea una classe" | fylia test
```

### Mostra la versione

```bash
fylia version
# oppure
fylia --version
```

## Esecuzione test

```bash
# Esegui tutti i test
cd tests
python3 run_tests.py

# Oppure esegui test singoli
python3 test_mock_provider.py
python3 test_mapgen.py
python3 test_patcher.py
```

## Esempi di conversazione

### Esempio 1: Crea una funzione

```
Tu: Crea una funzione che calcola il fattoriale
FYLIA: [fornisce esempio di codice]
```

### Esempio 2: Visualizza la mappa

```
Tu: /map
FYLIA: [mostra la struttura del progetto]
```

### Esempio 3: Visualizza statistiche

```
Tu: /stats
FYLIA: 
  📄 File Python:  5
  🏛️  Classi:       3
  ⚙️  Funzioni:     8
  🔧 Metodi:       12
```

## Struttura del progetto

```
FYLIA-/
├── src/
│   └── fylia/
│       ├── __init__.py      # Package principale
│       ├── cli.py           # CLI entry point
│       ├── tui.py           # Interfaccia testuale
│       ├── mapgen.py        # Generatore mappe
│       ├── patcher.py       # Gestione patch
│       └── providers/
│           ├── __init__.py
│           └── mock.py      # Provider di test
├── tests/
│   ├── __init__.py
│   ├── run_tests.py         # Test runner
│   ├── test_mock_provider.py
│   ├── test_mapgen.py
│   └── test_patcher.py
├── pyproject.toml           # Configurazione package
├── requirements.txt         # Dipendenze
├── README.md               # Documentazione principale
└── INSTALL.md              # Questo file
```

## Risoluzione problemi

### Comando `fylia` non trovato

Assicurati che il percorso di installazione dei binari Python sia nel PATH:

```bash
# In Termux
export PATH=$PATH:~/.local/bin

# Aggiungi al .bashrc per renderlo permanente
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
```

### Errori di importazione

Assicurati di essere nella directory corretta e che il package sia installato:

```bash
pip install -e .
```

### Problemi con i permessi

In Termux, assicurati di avere i permessi di storage:

```bash
termux-setup-storage
```
