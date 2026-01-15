# FYLIA - Guida d'uso

## Installazione

### Requisiti
- Python 3.8 o superiore
- pip

### Installazione da repository

```bash
# Clone il repository
git clone https://github.com/meseb/FYLIA-.git
cd FYLIA-

# Installa il pacchetto
pip install -e .

# Oppure installa solo le dipendenze
pip install -r requirements.txt
```

### Per Termux (Android)

```bash
# Installa Python su Termux
pkg install python

# Clone e installa FYLIA
git clone https://github.com/meseb/FYLIA-.git
cd FYLIA-
pip install -e .
```

## Utilizzo

FYLIA offre due comandi principali:

### 1. Visualizzare la mappa del progetto

```bash
fylia map [percorso]
```

Mostra una mappa della struttura del progetto con:
- Albero dei file
- Classi e funzioni Python estratte automaticamente

**Esempio:**
```bash
# Mappa della directory corrente
fylia map .

# Mappa di un progetto specifico
fylia map /path/to/project
```

### 2. Avviare l'interfaccia TUI

```bash
fylia chat
```

Avvia l'interfaccia TUI a 3 pannelli:
- **Pannello sinistro**: Chat per inserire le tue richieste
- **Pannello centrale**: Output con codice generato
- **Pannello destro**: Mappa concettuale del progetto

**Controlli:**
- Scrivi nella chat e premi `Enter` per inviare
- `Ctrl+R`: Aggiorna la mappa del progetto
- `Ctrl+C`: Esci dall'applicazione

## Esempi di utilizzo della chat

Il provider mock attuale risponde a keyword specifiche:

- **"funzione"**: Genera esempio di funzione Python
- **"classe"**: Genera esempio di classe Python
- **"file"**: Genera esempio di nuovo file
- **"test"**: Genera esempio di test con pytest

**Esempi:**
```
Tu: crea una funzione per calcolare la somma
FYLIA: [genera esempio di funzione Python]

Tu: scrivi una classe per gestire utenti
FYLIA: [genera esempio di classe Python]
```

## Architettura

FYLIA è organizzato in moduli chiari:

```
src/fylia/
├── cli.py          # Entry point CLI
├── tui.py          # Interfaccia TUI a pannelli
├── mapgen.py       # Generatore mappa concettuale
├── patcher.py      # Applicazione patch/diff
└── providers/
    └── mock.py     # Provider mock per test
```

## Provider Mock

Il provider attuale è un mock che simula risposte AI per scopi di sviluppo e testing. In futuro può essere sostituito con provider reali (OpenAI, Anthropic, ecc.) implementando l'interfaccia comune.

## Testing

```bash
# Esegui tutti i test
pytest tests/

# Con coverage
pytest tests/ --cov=src/fylia

# Test specifico
pytest tests/test_mapgen.py -v
```

## Sviluppo

FYLIA è pensato per essere:
- **Modulare**: ogni componente ha responsabilità chiare
- **Educativo**: codice commentato e leggibile
- **Estensibile**: facile aggiungere nuovi provider o comandi

## Prossimi passi

- [ ] Integrazione con provider AI reali
- [ ] Supporto per più linguaggi di programmazione nella mappa
- [ ] Salvataggio conversazioni chat
- [ ] Export della mappa in formati diversi
- [ ] Riconoscimento vocale per input (Android)

## Supporto

Per problemi o domande, apri una issue su GitHub.
