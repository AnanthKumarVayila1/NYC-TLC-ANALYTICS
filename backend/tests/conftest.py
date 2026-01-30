"""
Pytest configuration and fixtures
"""
import pytest
import os
from unittest.mock import patch, MagicMock

# Mock environment variables
os.environ.setdefault('DB_SERVER', 'mock-server')
os.environ.setdefault('DB_NAME', 'mock-db')
os.environ.setdefault('DB_USER', 'mock-user')
os.environ.setdefault('DB_PASSWORD', 'mock-password')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')


@pytest.fixture
def mock_db_connection():
    """Mock database connection"""
    with patch('app.database.get_db_connection') as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def mock_pyodbc():
    """Mock pyodbc connection"""
    with patch('pyodbc.connect') as mock:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock.return_value = mock_connection
        yield mock
