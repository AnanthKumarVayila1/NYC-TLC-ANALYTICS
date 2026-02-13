import os
from typing import Optional

# Check if we're in development mode
DEV_MODE = os.getenv('DEV_MODE', '').lower() in ['true', '1', 'yes']

# Try to import pyodbc, but fall back to mock if not available
try:
    import pyodbc
    from contextlib import contextmanager
    from app.config import settings
    pyodbc_available = True
except ImportError:
    print("⚠️  WARNING: pyodbc not available (SQL Server ODBC driver missing). Using mock database.")
    pyodbc_available = False
    DEV_MODE = True

if DEV_MODE or not pyodbc_available:
    # Use mock database for development
    from app.database_dev import Database
else:
    # Use real database connection
    from contextlib import contextmanager
    from app.config import settings
    
    class Database:
        def __init__(self):
            self.connection_string = settings.database_url
        
        @contextmanager
        def get_connection(self):
            """Context manager for database connections"""
            conn = None
            try:
                conn = pyodbc.connect(self.connection_string)
                yield conn
            except Exception as e:
                if conn:
                    conn.rollback()
                raise e
            finally:
                if conn:
                    conn.close()
        
        def execute_query(self, query: str, params: Optional[tuple] = None):
            """Execute SELECT query and return results"""
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                return results
        
        def execute_scalar(self, query: str, params: Optional[tuple] = None):
            """Execute query and return single value"""
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                result = cursor.fetchone()
                return result[0] if result else None

db = Database()