"""
Test per il Mock Provider
"""
import pytest
from fylia.providers.mock import MockProvider


def test_mock_provider_initialization():
    """Test inizializzazione del provider"""
    provider = MockProvider()
    assert provider is not None
    assert len(provider.conversation_history) == 0


def test_mock_provider_greeting():
    """Test risposta a saluto"""
    provider = MockProvider()
    response = provider.get_response("Ciao")
    
    assert "Ciao" in response or "FYLIA" in response
    assert len(provider.conversation_history) == 2  # user + assistant


def test_mock_provider_help():
    """Test richiesta aiuto"""
    provider = MockProvider()
    response = provider.get_response("aiuto")
    
    assert "aiuto" in response.lower() or "posso" in response.lower()


def test_mock_provider_generate_code():
    """Test generazione codice"""
    provider = MockProvider()
    
    # Test funzione
    code = provider.generate_code("crea una funzione")
    assert "def" in code
    assert "```python" in code
    
    # Test classe
    code = provider.generate_code("crea una classe")
    assert "class" in code
    assert "```python" in code


def test_mock_provider_conversation_history():
    """Test che la cronologia conversazione sia mantenuta"""
    provider = MockProvider()
    
    provider.get_response("Primo messaggio")
    provider.get_response("Secondo messaggio")
    
    assert len(provider.conversation_history) == 4  # 2 user + 2 assistant
    assert provider.conversation_history[0][0] == 'user'
    assert provider.conversation_history[1][0] == 'assistant'
