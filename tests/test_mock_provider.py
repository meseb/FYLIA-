"""
Test per il MockProvider
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fylia.providers.mock import MockProvider


def test_mock_provider_creation():
    """Test creazione provider"""
    provider = MockProvider()
    assert provider is not None
    assert provider.conversation_history == []


def test_mock_provider_chat_hello():
    """Test risposta a saluto"""
    provider = MockProvider()
    response = provider.chat("Ciao")
    assert response is not None
    assert len(response) > 0
    assert "FYLIA" in response or "ciao" in response.lower()


def test_mock_provider_chat_function():
    """Test risposta per richiesta funzione"""
    provider = MockProvider()
    response = provider.chat("Crea una funzione")
    assert response is not None
    assert "def" in response or "funzione" in response.lower()


def test_mock_provider_chat_class():
    """Test risposta per richiesta classe"""
    provider = MockProvider()
    response = provider.chat("Crea una classe")
    assert response is not None
    assert "class" in response or "classe" in response.lower()


def test_mock_provider_history():
    """Test cronologia conversazione"""
    provider = MockProvider()
    provider.chat("Primo messaggio")
    provider.chat("Secondo messaggio")
    
    history = provider.get_history()
    assert len(history) == 4  # 2 user + 2 assistant
    assert history[0]['role'] == 'user'
    assert history[1]['role'] == 'assistant'


def test_mock_provider_clear_history():
    """Test pulizia cronologia"""
    provider = MockProvider()
    provider.chat("Messaggio")
    provider.clear_history()
    
    history = provider.get_history()
    assert len(history) == 0


if __name__ == '__main__':
    # Esegui i test
    test_mock_provider_creation()
    print("✓ test_mock_provider_creation")
    
    test_mock_provider_chat_hello()
    print("✓ test_mock_provider_chat_hello")
    
    test_mock_provider_chat_function()
    print("✓ test_mock_provider_chat_function")
    
    test_mock_provider_chat_class()
    print("✓ test_mock_provider_chat_class")
    
    test_mock_provider_history()
    print("✓ test_mock_provider_history")
    
    test_mock_provider_clear_history()
    print("✓ test_mock_provider_clear_history")
    
    print("\n✓ Tutti i test del MockProvider passati!")
