"""Pytest fixtures and configuration for tests"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from peli_palvelu import PeliPalvelu, PeliTehdas
from web_app import app


@pytest.fixture
def tuomari():
    """Create a fresh Tuomari instance for each test"""
    return Tuomari()


@pytest.fixture
def tekoaly():
    """Create a fresh Tekoaly instance for each test"""
    return Tekoaly()


@pytest.fixture
def tekoaly_parannettu():
    """Create a fresh TekoalyParannettu instance for each test"""
    return TekoalyParannettu(10)


@pytest.fixture
def peli_palvelu():
    """Create a fresh PeliPalvelu instance for each test"""
    return PeliPalvelu(PeliTehdas())


@pytest.fixture
def flask_app():
    """Create a Flask app for testing"""
    app.config['TESTING'] = True
    return app


@pytest.fixture
def flask_client(flask_app):
    """Create a test client for Flask"""
    return flask_app.test_client()


@pytest.fixture
def flask_runner(flask_app):
    """Create a CLI runner for Flask"""
    return flask_app.test_cli_runner()
