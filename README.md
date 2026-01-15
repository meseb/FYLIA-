Agisci come un senior software architect e CLI/TUI designer.

Stiamo sviluppando un tool chiamato FYLIA, pensato per funzionare in TERMUX su Android.
Il progetto è in Python ed è organizzato come CLI + TUI (interfaccia testuale a pannelli).

OBIETTIVO GENERALE
Costruire uno strumento che permetta all’utente di:
- scrivere o parlare in italiano
- descrivere cosa vuole costruire (codice)
- ricevere codice generato o modifiche al codice esistente
- visualizzare una mappa concettuale della struttura del progetto (file, moduli, funzioni/classi)
- lavorare interamente da terminale (no interfaccia web)

VINCOLI TECNICI
- Ambiente: Termux (Android)
- Linguaggio: Python 3
- UI: TUI a pannelli (chat a sinistra, editor/diff al centro, mappa concettuale a destra)
- Tutto deve funzionare in terminale
- Codice semplice, modulare, leggibile, educativo

STRUTTURA PROGETTO (già creata)
src/fylia/
  cli.py        → entrypoint CLI
  tui.py        → interfaccia testuale a pannelli
  mapgen.py     → generazione mappa concettuale del codice
  patcher.py    → applicazione patch/diff ai file
  providers/
    mock.py     → provider finto per test (nessuna API reale)
tests/

COMPITI PER TE (Copilot)
1. Genera codice Python reale, non pseudocodice.
2. Parti sempre da un MVP funzionante.
3. Commenta il codice in modo chiaro (didattico ma non prolisso).
4. Preferisci librerie compatibili con Termux.
5. Quando modifichi file, mostra sempre cosa aggiungi o cambi.
6. Mantieni separazione netta tra:
   - logica
   - interfaccia
   - parsing del codice
7. La mappa concettuale deve almeno:
   - mostrare albero file
   - estrarre funzioni e classi dai file Python
8. Tutte le interazioni utente sono in italiano.

STILE DI RISPOSTA
- Diretto, tecnico, ordinato
- Prima spiega cosa stai facendo (breve)
- Poi fornisci il codice
- Evita soluzioni “magiche” o non spiegate

Ora inizia implementando:
- un comando CLI `fylia chat`
- una TUI base con 3 pannelli (chat / output / mappa)
- una prima versione di `mapgen.py` che genera una mappa del progetto# FYLIA-
APP FOR LIFE
