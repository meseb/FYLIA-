# Guida all'Installazione e Uso di FYLIA

## Requisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)
- Termux su Android (consigliato) o qualsiasi terminale Unix/Linux

## Installazione

### 1. Clona il repository

```bash
git clone https://github.com/meseb/FYLIA-.git
cd FYLIA-
```

### 2. Crea un ambiente virtuale (opzionale ma consigliato)

```bash
python -m venv venv
source venv/bin/activate  # Su Unix/Linux/Termux
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Installa FYLIA in modalità development

```bash
pip install -e .
```

## Utilizzo

### Avviare l'interfaccia conversazionale

```bash
fylia chat
```

Questo avvia l'interfaccia TUI a 3 pannelli:
- **Sinistra**: Chat conversazionale
- **Centro**: Editor/Output del codice
- **Destra**: Mappa concettuale del progetto

### Comandi disponibili

#### Interfaccia TUI

Una volta avviata l'interfaccia con `fylia chat`:

- **Scrivi nella chat**: Digita il tuo messaggio nella casella in basso e premi Enter
- **q**: Esci dall'applicazione
- **r**: Aggiorna la mappa del progetto

#### Generare la mappa del progetto

```bash
fylia map              # Mappa della directory corrente
fylia map /percorso    # Mappa di una directory specifica
```

### Esempi di conversazione

Nella chat puoi scrivere cose come:

- "Ciao" - Per iniziare
- "aiuto" - Per vedere cosa puoi fare
- "crea una funzione per calcolare la somma" - Per generare codice
- "crea una classe Calcolatrice" - Per generare una classe

## Test

Per eseguire i test:

```bash
pytest tests/
```

Per eseguire i test con coverage:

```bash
pytest tests/ --cov=fylia
```

## Struttura del Progetto

```
FYLIA-/
├── src/fylia/           # Codice sorgente
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Entry point CLI
│   ├── tui.py           # Interfaccia TUI
│   ├── mapgen.py        # Generatore mappa concettuale
│   ├── patcher.py       # Sistema patch/diff
│   └── providers/       # Provider AI
│       ├── __init__.py
│       └── mock.py      # Provider mock per test
├── tests/               # Test suite
├── requirements.txt     # Dipendenze
├── pyproject.toml       # Configurazione progetto
└── README.md           # Documentazione principale
```

## Sviluppo

### Aggiungere un nuovo provider AI

1. Crea un nuovo file in `src/fylia/providers/`
2. Eredita da `BaseProvider`
3. Implementa i metodi richiesti: `get_response()` e `generate_code()`

Esempio:

```python
from fylia.providers import BaseProvider

class MyProvider(BaseProvider):
    def get_response(self, user_input: str) -> str:
        # La tua implementazione
        pass
    
    def generate_code(self, description: str) -> str:
        # La tua implementazione
        pass
```

## Troubleshooting

### ImportError o ModuleNotFoundError

Assicurati di aver installato tutte le dipendenze:

```bash
pip install -r requirements.txt
```

### L'interfaccia TUI non si avvia

Verifica che Textual sia installato correttamente:

```bash
pip install --upgrade textual
```

### Problemi su Termux

Su Termux, potrebbe essere necessario installare alcuni pacchetti aggiuntivi:

```bash
pkg install python
pkg install clang
```

## Contribuire

Il progetto è in fase iniziale e accoglie contributi! Sentiti libero di:

- Aprire issue per bug o suggerimenti
- Proporre pull request
- Migliorare la documentazione

## Licenza

[Specificare licenza]
