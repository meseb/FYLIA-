"""
Provider Base

Interfaccia base per i provider AI.
"""
from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Classe base astratta per i provider AI"""
    
    @abstractmethod
    def get_response(self, user_input: str) -> str:
        """
        Ottiene una risposta dal provider AI
        
        Args:
            user_input: Input dell'utente
            
        Returns:
            Risposta generata
        """
        pass
    
    @abstractmethod
    def generate_code(self, description: str) -> str:
        """
        Genera codice basato su una descrizione
        
        Args:
            description: Descrizione di cosa generare
            
        Returns:
            Codice generato
        """
        pass
