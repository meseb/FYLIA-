"""
Provider finto per test senza API reali
Simula risposte di un assistente AI
"""


class MockProvider:
    """Provider mock per simulare risposte AI durante lo sviluppo"""
    
    def __init__(self):
        self.responses = {
            'funzione': self._generate_function_response,
            'classe': self._generate_class_response,
            'file': self._generate_file_response,
            'test': self._generate_test_response,
        }
    
    def generate_response(self, user_input: str) -> str:
        """
        Genera una risposta mock basata sull'input dell'utente
        
        Args:
            user_input: testo inserito dall'utente
            
        Returns:
            Risposta simulata
        """
        user_input_lower = user_input.lower()
        
        # Cerca keyword nell'input
        for keyword, response_func in self.responses.items():
            if keyword in user_input_lower:
                return response_func(user_input)
        
        # Risposta di default
        return self._generate_default_response(user_input)
    
    def _generate_function_response(self, user_input: str) -> str:
        """Genera esempio di funzione Python"""
        return """Ecco una funzione Python di esempio:

```python
def calcola_somma(a: int, b: int) -> int:
    \"\"\"
    Calcola la somma di due numeri
    
    Args:
        a: primo numero
        b: secondo numero
        
    Returns:
        La somma di a e b
    \"\"\"
    return a + b

# Esempio di utilizzo
risultato = calcola_somma(5, 3)
print(f"Il risultato è: {risultato}")
```

Questa funzione è semplice ed educativa, 
con type hints e docstring completa."""
    
    def _generate_class_response(self, user_input: str) -> str:
        """Genera esempio di classe Python"""
        return """Ecco una classe Python di esempio:

```python
class Persona:
    \"\"\"Rappresenta una persona con nome ed età\"\"\"
    
    def __init__(self, nome: str, eta: int):
        self.nome = nome
        self.eta = eta
    
    def saluta(self) -> str:
        \"\"\"Restituisce un messaggio di saluto\"\"\"
        return f"Ciao, mi chiamo {self.nome} e ho {self.eta} anni"
    
    def compleanno(self):
        \"\"\"Incrementa l'età di 1\"\"\"
        self.eta += 1

# Esempio di utilizzo
persona = Persona("Mario", 30)
print(persona.saluta())
persona.compleanno()
print(f"Dopo il compleanno: {persona.eta} anni")
```

Classe base con costruttore, attributi e metodi."""
    
    def _generate_file_response(self, user_input: str) -> str:
        """Genera esempio di creazione file"""
        return """Per creare un nuovo file Python:

```python
# nuovo_modulo.py

def funzione_principale():
    \"\"\"Funzione principale del modulo\"\"\"
    print("Modulo caricato correttamente!")

if __name__ == "__main__":
    funzione_principale()
```

Puoi salvare questo codice in un file .py
e importarlo in altri moduli."""
    
    def _generate_test_response(self, user_input: str) -> str:
        """Genera esempio di test"""
        return """Ecco un esempio di test con pytest:

```python
import pytest

def test_somma():
    \"\"\"Test per la funzione di somma\"\"\"
    assert calcola_somma(2, 3) == 5
    assert calcola_somma(0, 0) == 0
    assert calcola_somma(-1, 1) == 0

def test_somma_negativi():
    \"\"\"Test con numeri negativi\"\"\"
    assert calcola_somma(-5, -3) == -8
```

Usa `pytest` per eseguire i test."""
    
    def _generate_default_response(self, user_input: str) -> str:
        """Risposta di default quando nessuna keyword è trovata"""
        return f"""Ho ricevuto la tua richiesta: "{user_input}"

Sono un provider mock, quindi posso solo generare 
esempi predefiniti per:

- 'funzione': genera esempio di funzione Python
- 'classe': genera esempio di classe Python  
- 'file': genera esempio di nuovo file
- 'test': genera esempio di test

Prova a includere una di queste parole chiave 
nella tua prossima richiesta!

In una versione completa di FYLIA, qui ci sarebbe 
l'integrazione con un vero modello AI che genererebbe
codice personalizzato basato sulla tua richiesta."""
