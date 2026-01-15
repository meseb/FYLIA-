# Guida all'uso di FYLIA

## Introduzione

FYLIA è uno strumento di sviluppo conversazionale progettato per funzionare in Termux su Android (ma funziona anche su sistemi Linux/Unix standard). Ti permette di:

1. **Conversare in italiano** per descrivere cosa vuoi costruire
2. **Vedere la struttura del codice** attraverso mappe concettuali
3. **Applicare modifiche** al codice in modo interattivo

## Comandi Principali

### 1. Interfaccia Conversazionale (`fylia chat`)

Il comando principale di FYLIA. Avvia una sessione interattiva dove puoi:
- Scrivere messaggi per descrivere cosa vuoi costruire
- Usare comandi speciali per esplorare il progetto
- Applicare modifiche proposte al codice

```bash
fylia chat
```

#### Comandi disponibili nella chat:

- **`/map`** - Mostra la mappa completa del progetto
  ```
  Tu: /map
  ```

- **`/stats`** - Mostra statistiche del progetto (numero di file, classi, funzioni, metodi)
  ```
  Tu: /stats
  ```

- **`/refresh`** - Rigenera la mappa del progetto (utile dopo aver fatto modifiche)
  ```
  Tu: /refresh
  ```

- **`/help`** - Mostra l'elenco dei comandi disponibili
  ```
  Tu: /help
  ```

- **`/exit`** o **`/quit`** - Esci da FYLIA
  ```
  Tu: /exit
  ```

#### Esempi di conversazione:

**Esempio 1: Richiesta generica**
```
Tu: Ciao!
FYLIA: Ciao! Sono FYLIA, il tuo assistente di programmazione. Come posso aiutarti oggi?
```

**Esempio 2: Richiedere aiuto**
```
Tu: Aiuto
FYLIA: Posso aiutarti con:
- Scrivere funzioni e classi Python
- Creare strutture di progetto
- Spiegare concetti di programmazione
- Generare e applicare patch al codice

Dimmi cosa vuoi costruire!
```

**Esempio 3: Creare una funzione**
```
Tu: Crea una funzione per calcolare il quadrato di un numero
FYLIA: Ecco un esempio di funzione Python:

```python
def esempio_funzione(parametro):
    '''Questa è una funzione di esempio'''
    risultato = parametro * 2
    return risultato
```

Questa funzione prende un parametro e restituisce il doppio del suo valore.
```

**Esempio 4: Creare una classe**
```
Tu: Voglio una classe per gestire un utente
FYLIA: Ecco un esempio di classe Python:

```python
class EsempioClasse:
    '''Questa è una classe di esempio'''
    
    def __init__(self, valore):
        self.valore = valore
    
    def mostra_valore(self):
        return f"Il valore è: {self.valore}"
```

Questa classe memorizza un valore e fornisce un metodo per visualizzarlo.
```

### 2. Visualizzare la Mappa (`fylia map`)

Visualizza la struttura del progetto senza entrare nella modalità chat.

**Formato albero (default):**
```bash
fylia map
```

Output:
```
📊 Generazione mappa del progetto: .

======================================================================
📁 .
├─ 📁 src
  ├─ 📁 fylia
    ├─ 📄 __init__.py
    ├─ 📄 cli.py
      ├─ ⚙️ cmd_chat (L16)
      ├─ ⚙️ cmd_map (L22)
      └─ ⚙️ main (L74)
    └─ 📄 tui.py
      ├─ 🏛️ SimpleTUI (L12)
      └─ ⚙️ run_tui (L180)
...
```

**Solo statistiche:**
```bash
fylia map -f stats
```

Output:
```
📈 Statistiche:
  📄 File Python:  12
  🏛️  Classi:       5
  ⚙️  Funzioni:     27
  🔧 Metodi:       29
```

**Formato JSON (per elaborazione automatica):**
```bash
fylia map -f json
```

**Specificare un percorso diverso:**
```bash
fylia map -p /percorso/al/progetto
```

### 3. Testare il Provider (`fylia test`)

Testa rapidamente il provider AI con un messaggio, senza entrare nella modalità chat completa.

**Con messaggio inline:**
```bash
fylia test -m "Crea una funzione"
```

**Leggere da stdin:**
```bash
echo "Voglio una classe per gestire un database" | fylia test
```

O in modalità interattiva:
```bash
fylia test
# (inserisci il tuo messaggio, poi premi Ctrl+D)
```

### 4. Informazioni sulla Versione

```bash
fylia --version
# oppure
fylia version
```

## Workflow Tipico

### Scenario 1: Esplorare un nuovo progetto

```bash
# 1. Vai nella directory del progetto
cd /path/to/project

# 2. Genera la mappa per vedere la struttura
fylia map

# 3. Avvia la chat per esplorare interattivamente
fylia chat

# 4. Nella chat, usa i comandi per navigare
Tu: /stats
Tu: /map
```

### Scenario 2: Sviluppare con FYLIA

```bash
# 1. Avvia la chat
fylia chat

# 2. Descrivi cosa vuoi costruire
Tu: Voglio creare una classe per gestire un sistema di autenticazione

# 3. FYLIA fornirà del codice di esempio

# 4. Se il codice include istruzioni per creare file, FYLIA chiederà conferma

# 5. Visualizza la mappa aggiornata
Tu: /refresh
Tu: /map
```

### Scenario 3: Analisi rapida del progetto

```bash
# Solo statistiche
fylia map -f stats

# Mappa completa salvata in un file
fylia map > mappa_progetto.txt

# Esportare in JSON per elaborazione
fylia map -f json > struttura.json
```

## Caratteristiche Avanzate

### Applicazione Automatica di Patch

FYLIA può riconoscere quando una risposta contiene istruzioni per creare o modificare file. 

Se la risposta contiene:
```
File: src/example.py
```python
def nuova_funzione():
    return "Hello World"
```
```

FYLIA:
1. Rileverà l'istruzione del file
2. Mostrerà un'anteprima delle modifiche (diff colorato)
3. Chiederà conferma prima di applicare
4. Rigenererà automaticamente la mappa dopo l'applicazione

### Interpretazione della Mappa

La mappa usa icone emoji per identificare i diversi elementi:

- 📁 **Directory** - Cartelle del progetto
- 📄 **File Python** - File .py
- 🏛️ **Classe** - Definizione di classe
- ⚙️ **Funzione** - Funzione standalone
- 🔧 **Metodo** - Metodo di una classe
- ⚠️ **Errore** - Errore nell'analisi del file

Il numero dopo `(L##)` indica la riga nel file dove l'elemento è definito.

## Limitazioni della Versione Mock

La versione attuale di FYLIA usa un **MockProvider** che simula le risposte AI senza fare chiamate a servizi esterni. Questo significa:

✅ **Funziona offline**
✅ **Non richiede API key**
✅ **Veloce e leggero**

❌ **Risposte limitate basate su parole chiave**
❌ **Non genera codice veramente personalizzato**
❌ **Non comprende context complesso**

Per usare provider AI reali (OpenAI, Anthropic, etc.), sarà necessario:
1. Implementare un provider specifico
2. Configurare le API key
3. Installare le dipendenze necessarie

## Troubleshooting

### Il comando `fylia` non viene trovato

Aggiungi il percorso dei binari Python al PATH:
```bash
export PATH=$PATH:~/.local/bin
```

In Termux, aggiungi al `.bashrc`:
```bash
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Errori nell'analisi di file Python

FYLIA usa `ast` per analizzare i file Python. Se un file ha errori di sintassi, verrà mostrato un errore ma la mappa continuerà a generarsi per gli altri file.

### La mappa non si aggiorna

Usa il comando `/refresh` nella chat o rigenera manualmente:
```bash
fylia map -p .
```

## Prossimi Passi

1. **Esplora** - Usa `fylia map` per capire la struttura del progetto
2. **Sperimenta** - Prova `fylia chat` e i vari comandi
3. **Costruisci** - Usa FYLIA per creare e modificare codice
4. **Contribuisci** - Migliora FYLIA aggiungendo nuovi provider o funzionalità

Per contribuire al progetto: https://github.com/meseb/FYLIA-
