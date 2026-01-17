"""Test per il provider mock"""

import pytest
from fylia.providers.mock import MockProvider


def test_mock_provider_creation():
    """Test creazione del provider"""
    provider = MockProvider()
    assert provider is not None


def test_function_keyword():
    """Test risposta con keyword 'funzione'"""
    provider = MockProvider()
    response = provider.generate_response("crea una funzione")
    
    assert isinstance(response, str)
    assert 'funzione' in response.lower() or 'def' in response


def test_class_keyword():
    """Test risposta con keyword 'classe'"""
    provider = MockProvider()
    response = provider.generate_response("crea una classe")
    
    assert isinstance(response, str)
    assert 'class' in response or 'classe' in response.lower()


def test_file_keyword():
    """Test risposta con keyword 'file'"""
    provider = MockProvider()
    response = provider.generate_response("crea un file")
    
    assert isinstance(response, str)
    assert 'file' in response.lower()


def test_test_keyword():
    """Test risposta con keyword 'test'"""
    provider = MockProvider()
    response = provider.generate_response("scrivi un test")
    
    assert isinstance(response, str)
    assert 'test' in response.lower() or 'pytest' in response


def test_default_response():
    """Test risposta di default senza keyword"""
    provider = MockProvider()
    response = provider.generate_response("qualcosa di casuale")
    
    assert isinstance(response, str)
    assert 'mock' in response.lower() or 'provider' in response.lower()
