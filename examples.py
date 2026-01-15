#!/usr/bin/env python3
"""
Esempi di utilizzo programmatico di FYLIA
"""

import sys
sys.path.insert(0, 'src')

from fylia.providers.mock import MockProvider
from fylia.mapgen import MapGenerator
from fylia.patcher import Patcher


def esempio_1_provider():
    """Esempio 1: Usare il provider direttamente"""
    print("=" * 70)
    print("ESEMPIO 1: Uso del MockProvider")
    print("=" * 70)
    
    provider = MockProvider()
    
    # Invia alcuni messaggi
    messaggi = [
        "Ciao",
        "Crea una funzione",
        "Voglio una classe",
        "Come posso aiutare?"
    ]
    
    for msg in messaggi:
        print(f"\n📤 Utente: {msg}")
        risposta = provider.chat(msg)
        print(f"📥 FYLIA: {risposta[:100]}...")  # Primi 100 caratteri
    
    # Mostra la cronologia
    print(f"\n📊 Messaggi nella cronologia: {len(provider.get_history())}")


def esempio_2_mapgen():
    """Esempio 2: Generare mappe del codice"""
    print("\n" + "=" * 70)
    print("ESEMPIO 2: Generazione Mappa del Progetto")
    print("=" * 70)
    
    # Genera mappa del progetto corrente
    mapgen = MapGenerator('.')
    mappa = mapgen.generate_map()
    
    # Mostra statistiche
    stats = mapgen.get_summary(mappa)
    print(f"\n📊 Statistiche del progetto:")
    print(f"  📄 File Python:  {stats['files']}")
    print(f"  🏛️  Classi:       {stats['classes']}")
    print(f"  ⚙️  Funzioni:     {stats['functions']}")
    print(f"  🔧 Metodi:       {stats['methods']}")
    
    # Mostra parte dell'albero
    tree = mapgen.format_tree(mappa)
    lines = tree.split('\n')
    print(f"\n🌳 Primi 20 elementi dell'albero:")
    for line in lines[:20]:
        print(line)


def esempio_3_patcher():
    """Esempio 3: Creare e visualizzare diff"""
    print("\n" + "=" * 70)
    print("ESEMPIO 3: Creazione e Gestione Diff")
    print("=" * 70)
    
    patcher = Patcher()
    
    # Esempio di contenuti
    vecchio = """def saluta(nome):
    print(f"Ciao {nome}")
    return True
"""
    
    nuovo = """def saluta(nome):
    '''Funzione che saluta una persona'''
    messaggio = f"Ciao {nome}!"
    print(messaggio)
    return messaggio
"""
    
    # Crea un diff
    diff = patcher.create_diff("esempio.py", vecchio, nuovo)
    print("\n📝 Diff generato:")
    print(patcher.format_diff_for_display(diff))
    
    # Esempio di estrazione codice da markdown
    testo = """
Ecco un esempio di codice:

```python
def test():
    return 42
```

E altro codice:

```javascript
console.log('Hello');
```
"""
    
    blocchi = patcher.extract_code_blocks(testo)
    print(f"\n📦 Blocchi di codice estratti: {len(blocchi)}")
    for lang, code in blocchi:
        print(f"  - Linguaggio: {lang}")
        print(f"    Linee: {len(code.splitlines())}")


def esempio_4_integrazione():
    """Esempio 4: Integrazione di tutti i componenti"""
    print("\n" + "=" * 70)
    print("ESEMPIO 4: Integrazione Completa")
    print("=" * 70)
    
    # Crea un provider e un mapgen
    provider = MockProvider()
    mapgen = MapGenerator('.')
    
    # Simula una conversazione
    domanda = "Mostrami come creare una funzione"
    print(f"\n💬 Domanda: {domanda}")
    
    risposta = provider.chat(domanda)
    print(f"\n🤖 Risposta ricevuta ({len(risposta)} caratteri)")
    
    # Genera mappa
    print("\n🗺️  Generazione mappa del progetto...")
    mappa = mapgen.generate_map()
    stats = mapgen.get_summary(mappa)
    print(f"✓ Mappa generata: {stats['files']} file analizzati")
    
    # Verifica se la risposta contiene codice
    patcher = Patcher()
    blocchi = patcher.extract_code_blocks(risposta)
    if blocchi:
        print(f"\n💻 Trovati {len(blocchi)} blocchi di codice nella risposta")
        for i, (lang, code) in enumerate(blocchi, 1):
            print(f"  Blocco {i}: {lang} ({len(code.splitlines())} linee)")


def main():
    """Esegue tutti gli esempi"""
    print("\n")
    print("*" * 70)
    print(" " * 20 + "FYLIA - ESEMPI D'USO")
    print("*" * 70)
    
    try:
        esempio_1_provider()
        esempio_2_mapgen()
        esempio_3_patcher()
        esempio_4_integrazione()
        
        print("\n" + "=" * 70)
        print("✓ Tutti gli esempi completati con successo!")
        print("=" * 70)
        print("\nPer usare FYLIA interattivamente, esegui: fylia chat")
        print()
        
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione degli esempi: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
