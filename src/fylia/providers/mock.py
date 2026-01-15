"""
Provider finto per test - nessuna API reale
Simula risposte di un modello AI senza fare chiamate esterne
"""

class MockProvider:
    """Provider di test che simula risposte AI"""
    
    def __init__(self):
        self.conversation_history = []
    
    def chat(self, message: str) -> str:
        """
        Simula una risposta a un messaggio dell'utente
        
        Args:
            message: Il messaggio dell'utente in italiano
            
        Returns:
            Una risposta simulata
        """
        self.conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        # Risposte simulate basate su parole chiave
        message_lower = message.lower()
        
        if 'funzione' in message_lower or 'function' in message_lower:
            response = """Ecco un esempio di funzione Python:

```python
def esempio_funzione(parametro):
    '''Questa è una funzione di esempio'''
    risultato = parametro * 2
    return risultato
```

Questa funzione prende un parametro e restituisce il doppio del suo valore."""
            
        elif 'classe' in message_lower or 'class' in message_lower:
            response = """Ecco un esempio di classe Python:

```python
class EsempioClasse:
    '''Questa è una classe di esempio'''
    
    def __init__(self, valore):
        self.valore = valore
    
    def mostra_valore(self):
        return f"Il valore è: {self.valore}"
```

Questa classe memorizza un valore e fornisce un metodo per visualizzarlo."""
            
        elif 'ciao' in message_lower or 'hello' in message_lower:
            response = "Ciao! Sono FYLIA, il tuo assistente di programmazione. Come posso aiutarti oggi?"
            
        elif 'aiuto' in message_lower or 'help' in message_lower:
            response = """Posso aiutarti con:
- Scrivere funzioni e classi Python
- Creare strutture di progetto
- Spiegare concetti di programmazione
- Generare e applicare patch al codice

Dimmi cosa vuoi costruire!"""
            
        else:
            response = f"Ho ricevuto il tuo messaggio: '{message}'. In modalità mock, posso solo fornire risposte simulate. Descrivi cosa vuoi costruire e ti aiuterò!"
        
        self.conversation_history.append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def get_history(self):
        """Restituisce la cronologia della conversazione"""
        return self.conversation_history
    
    def clear_history(self):
        """Pulisce la cronologia della conversazione"""
        self.conversation_history = []
