#!/usr/bin/env python3
"""
Test Azure SQL Database Connection
"""
import sys

def test_azure_sql_connection():
    """Test connection to Azure SQL Database"""
    
    # Connection details from environment
    server = "nyc-sqldb-server.database.windows.net"
    database = "nyc-sqldatabase"
    username = "serveradmin"
    password = "Ram@221207"
    
    print("=" * 70)
    print("  🔌 Testing Azure SQL Database Connection")
    print("=" * 70)
    print()
    print(f"Server:   {server}")
    print(f"Database: {database}")
    print(f"User:     {username}")
    print()
    
    try:
        import pyodbc
        
        print("✓ pyodbc module found")
        print()
        
        # Create connection string
        connection_string = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server=tcp:{server},1433;"
            f"Database={database};"
            f"Uid={username};"
            f"Pwd={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        
        print("Connecting to Azure SQL Database...")
        conn = pyodbc.connect(connection_string)
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as connection_test")
        result = cursor.fetchone()
        
        print()
        print("=" * 70)
        print(f"✅ SUCCESS! Connected to Azure SQL Database")
        print("=" * 70)
        print()
        print(f"Test query result: {result[0]}")
        print()
        
        # Get database info
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES")
        table_count = cursor.fetchone()[0]
        print(f"Tables in database: {table_count}")
        print()
        
        conn.close()
        return True
        
    except ImportError:
        print("❌ ERROR: pyodbc not installed")
        print()
        print("To fix:")
        print("  pip install pyodbc")
        print()
        return False
        
    except Exception as e:
        error_msg = str(e)
        
        if "ODBC Driver 18 for SQL Server" in error_msg:
            print("❌ ERROR: ODBC Driver 18 for SQL Server not installed")
            print()
            print("This is a system-level dependency that needs to be installed.")
            print()
            print("Installation instructions:")
            print()
            print("macOS (using Homebrew):")
            print("  1. Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            print("  2. Add Homebrew to PATH:  eval \"$(/opt/homebrew/bin/brew shellenv)\"")
            print("  3. Install ODBC driver:  brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release")
            print("  4. brew install mssql-tools18")
            print()
            return False
            
        elif "Login failed" in error_msg or "18456" in error_msg:
            print("❌ ERROR: Invalid credentials")
            print()
            print("Please check:")
            print(f"  • Server: {server}")
            print(f"  • Database: {database}")
            print(f"  • Username: {username}")
            print(f"  • Password: {password}")
            print()
            return False
            
        elif "Network" in error_msg or "timeout" in error_msg.lower():
            print("❌ ERROR: Network/Connection timeout")
            print()
            print("Please check:")
            print("  • Server name is correct")
            print("  • Firewall allows your IP address")
            print("  • Azure SQL firewall rules are configured")
            print()
            print(f"Full error: {error_msg}")
            print()
            return False
            
        else:
            print(f"❌ ERROR: {error_msg}")
            print()
            return False

if __name__ == "__main__":
    success = test_azure_sql_connection()
    sys.exit(0 if success else 1)
