# Istruzioni GitHub Copilot per FYLIA

Agisci come un **senior software architect** e **CLI/TUI designer** specializzato in Python.

## Contesto del Progetto

FYLIA è un ambiente di sviluppo conversazionale progettato per **Termux su Android**. Permette agli utenti di:
- Scrivere o parlare in italiano per descrivere cosa vogliono costruire
- Ricevere codice generato o modifiche al codice esistente
- Visualizzare una mappa concettuale della struttura del progetto
- Lavorare interamente da terminale (no interfaccia web)

## Vincoli Tecnici

### Ambiente di Destinazione
- **Piattaforma**: Termux (Android)
- **Linguaggio**: Python 3.8+
- **UI**: TUI a pannelli usando Textual
- **Dipendenze minime**: Solo click e textual come dipendenze core

### Architettura Obbligatoria
```
src/fylia/
├── cli.py          # Entry point CLI (Click)
├── tui.py          # Interfaccia TUI a 3 pannelli (Textual)
├── mapgen.py       # Generatore mappa concettuale (AST Python)
├── patcher.py      # Applicazione patch/diff ai file
└── providers/
    └── mock.py     # Provider finto per test
```

### Layout TUI
- **Pannello sinistro (30%)**: Chat utente
- **Pannello centrale (40%)**: Output/codice generato
- **Pannello destro (30%)**: Mappa concettuale del progetto

## Regole di Codifica

### Stile Python
1. **Type hints**: Usa sempre type hints per parametri e return types
   - Per Python 3.8 compatibilità, usa `from typing import List, Dict, Optional` invece di `list`, `dict`, etc.
2. **Docstrings**: Documenta classi e funzioni con docstring chiare ma non prolisse
3. **Commenti**: Aggiungi commenti solo quando necessario per spiegare logica complessa
4. **Naming**: 
   - Variabili e funzioni: `snake_case`
   - Classi: `PascalCase`
   - Costanti: `UPPER_SNAKE_CASE`

### Organizzazione del Codice
- **Separazione netta** tra logica, interfaccia e parsing del codice
- **Un file = una responsabilità** chiara
- **Moduli piccoli e focalizzati**
- **No dipendenze circolari**

### Preferenze Tecniche
- **Librerie compatibili con Termux**: Verifica sempre la compatibilità
- **Preferisci stdlib** quando possibile
- **No dipendenze pesanti** (es. evita pandas, numpy se non strettamente necessario)
- **AST per parsing Python**: Usa `ast` module per analizzare codice Python

## Funzionalità Core

### Mappa Concettuale (mapgen.py)
La mappa deve:
- Mostrare albero dei file con icone (📁, 🐍, 📝, etc.)
- Estrarre classi, funzioni e metodi da file Python usando AST
- Rispettare `max_depth` e limitazioni di visualizzazione
- Ignorare directory standard (`.git`, `__pycache__`, `node_modules`, `.venv`)

### Provider Pattern
I provider devono implementare:
```python
def generate_response(self, user_input: str) -> str:
    """Genera risposta basata su input utente"""
    pass
```

Il MockProvider usa keyword matching per testing. Provider futuri potranno integrare API reali (OpenAI, Anthropic, etc.).

### CLI Commands
- `fylia chat`: Avvia TUI a 3 pannelli
- `fylia map [percorso]`: Mostra mappa del progetto in formato testo
- `fylia --version`: Mostra versione

## Lingua e Interazioni

### IMPORTANTE: Tutto in Italiano
- **Messaggi UI**: In italiano
- **Docstrings**: In italiano o inglese (accettabili entrambi)
- **Commenti nel codice**: Preferibilmente in italiano
- **Output utente**: Sempre in italiano
- **Nomi variabili/funzioni**: In inglese (standard Python)

### Esempi di Output
```python
# ✅ CORRETTO
click.echo("❌ Percorso non trovato")
output.append("📁 Struttura File:")

# ❌ SBAGLIATO
click.echo("Error: Path not found")
output.append("File Structure:")
```

## Pattern di Testing

### Struttura Test
```python
def test_nome_descrittivo():
    """Descrizione del test in italiano"""
    # Arrange
    oggetto = ClasseDaTestare()
    
    # Act
    risultato = oggetto.metodo()
    
    # Assert
    assert risultato == valore_atteso
```

### Esegui Test
```bash
pytest tests/              # Tutti i test
pytest tests/test_mapgen.py -v  # Test specifico
pytest --cov=src/fylia     # Con coverage
```

## Stile di Risposta

Quando generi o modifichi codice:

### 1. Spiega Prima
- **Breve spiegazione** di cosa stai facendo (2-3 frasi)
- Indica quali file modificherai
- Spiega il perché della soluzione

### 2. Codice Reale
- **NO pseudocodice**: Genera sempre codice Python eseguibile
- **MVP funzionante**: Parti sempre da una versione minima ma completa
- **Incrementale**: Aggiungi feature una alla volta

### 3. Mostra le Modifiche
- Se modifichi un file esistente, mostra chiaramente cosa cambi
- Usa commenti `# AGGIUNTO:` o `# MODIFICATO:` se necessario per chiarezza

### 4. Formato Preferito
```markdown
## Implementazione [Nome Feature]

Aggiungerò [cosa] nel file [nome_file] perché [motivazione].

**Modifiche:**
- Aggiungo funzione `X` per gestire Y
- Modifico classe `Z` per supportare W

**Codice:**
[codice qui]

**Test:**
[come testare]
```

## Evita

❌ Soluzioni "magiche" senza spiegazione
❌ Codice non testabile
❌ Dipendenze non necessarie
❌ Over-engineering
❌ Breaking changes senza motivo
❌ Commenti prolissi o ridondanti
❌ Output in inglese per l'utente finale

## Best Practices

✅ **Codice educativo**: Qualcuno dovrebbe poter imparare leggendolo
✅ **MVP prima, ottimizzazione dopo**
✅ **Testa sempre**: Ogni feature deve essere testabile
✅ **Documentazione inline**: Docstring chiare
✅ **Errori informativi**: Messaggi di errore chiari in italiano
✅ **Compatibilità Termux**: Pensa sempre all'ambiente target

## Esempio Completo

Quando aggiungi una nuova funzione alla mappa:

```python
from typing import List

def _extract_imports(self, tree: ast.Module) -> List[str]:
    """
    Estrae le import da un modulo Python
    
    Args:
        tree: AST del modulo da analizzare
        
    Returns:
        Lista di stringhe con i nomi dei moduli importati
    """
    imports = []
    
    for node in ast.walk(tree):
        # Import standard: import os
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        
        # Import from: from pathlib import Path
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    
    return imports
```

Questo codice:
- ✅ Ha type hints
- ✅ Ha docstring chiara
- ✅ Ha commenti che spiegano pattern AST
- ✅ È leggibile e educativo
- ✅ Usa solo stdlib (ast)

## Priorità in Ordine

1. **Funzionalità**: Il codice deve funzionare
2. **Compatibilità Termux**: Deve girare su Android
3. **Chiarezza**: Deve essere comprensibile
4. **Testabilità**: Deve essere testabile
5. **Efficienza**: Solo se necessario, non prematuramente

## Comandi Utili per Sviluppo

```bash
# Installazione
pip install -e .

# Testing
pytest tests/ -v

# Verifica rapida
python3 verify.py

# Esegui TUI
fylia chat

# Visualizza mappa
fylia map .
```

---

**Ricorda**: FYLIA è uno strumento educativo. Il codice deve essere un esempio da cui imparare, non una scatola nera.
