"""
Mock Provider - Provider finto per test

Fornisce risposte predefinite senza chiamare API reali.
Utile per sviluppo e testing.
"""
from fylia.providers import BaseProvider


class MockProvider(BaseProvider):
    """Provider di test che restituisce risposte simulate"""
    
    def __init__(self):
        self.conversation_history = []
        self.response_templates = {
            'ciao': "Ciao! Sono FYLIA, il tuo assistente per la programmazione. Come posso aiutarti oggi?",
            'aiuto': "Posso aiutarti a:\n- Generare codice\n- Spiegare concetti\n- Refactoring\n- Debug\nCosa vuoi fare?",
            'funzione': self._generate_function_example,
            'classe': self._generate_class_example,
        }
    
    def get_response(self, user_input: str) -> str:
        """
        Genera una risposta basata sull'input dell'utente
        
        Args:
            user_input: Messaggio dell'utente
            
        Returns:
            Risposta simulata
        """
        self.conversation_history.append(('user', user_input))
        
        # Converti a minuscolo per il matching
        input_lower = user_input.lower()
        
        # Cerca parole chiave
        for keyword, response in self.response_templates.items():
            if keyword in input_lower:
                if callable(response):
                    result = response(user_input)
                else:
                    result = response
                self.conversation_history.append(('assistant', result))
                return result
        
        # Risposta generica
        generic_response = self._generate_generic_response(user_input)
        self.conversation_history.append(('assistant', generic_response))
        return generic_response
    
    def generate_code(self, description: str) -> str:
        """
        Genera codice di esempio basato sulla descrizione
        
        Args:
            description: Descrizione del codice da generare
            
        Returns:
            Codice di esempio
        """
        if 'funzione' in description.lower():
            return self._generate_function_example(description)
        elif 'classe' in description.lower():
            return self._generate_class_example(description)
        else:
            return "# Esempio di codice\ndef esempio():\n    print('Ciao da FYLIA!')\n"
    
    def _generate_generic_response(self, user_input: str) -> str:
        """Genera una risposta generica"""
        responses = [
            f"Ho capito che vuoi: '{user_input}'. Posso aiutarti con del codice di esempio.",
            f"Interessante! Per '{user_input}', ti suggerisco di iniziare con...",
            f"Per realizzare '{user_input}', potremmo procedere così:",
        ]
        
        # Scegli in base alla lunghezza dell'input
        index = len(user_input) % len(responses)
        return responses[index]
    
    def _generate_function_example(self, description: str) -> str:
        """Genera un esempio di funzione"""
        return """Ecco un esempio di funzione:

```python
def calcola_somma(a, b):
    \"\"\"
    Calcola la somma di due numeri
    
    Args:
        a: Primo numero
        b: Secondo numero
        
    Returns:
        La somma di a e b
    \"\"\"
    return a + b
```

Questa funzione è semplice ma dimostra buone pratiche: docstring, parametri tipizzati, return chiaro."""
    
    def _generate_class_example(self, description: str) -> str:
        """Genera un esempio di classe"""
        return """Ecco un esempio di classe:

```python
class Calcolatrice:
    \"\"\"Classe per operazioni matematiche di base\"\"\"
    
    def __init__(self):
        self.memoria = 0
    
    def somma(self, a, b):
        \"\"\"Calcola la somma\"\"\"
        risultato = a + b
        self.memoria = risultato
        return risultato
    
    def sottrai(self, a, b):
        \"\"\"Calcola la sottrazione\"\"\"
        risultato = a - b
        self.memoria = risultato
        return risultato
    
    def get_memoria(self):
        \"\"\"Restituisce il valore in memoria\"\"\"
        return self.memoria
```

Questa classe dimostra:
- Inizializzazione con __init__
- Attributi di istanza (self.memoria)
- Metodi pubblici
- Documentazione chiara"""
