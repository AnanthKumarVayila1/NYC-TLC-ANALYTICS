#!/usr/bin/env python3
"""
Start Backend API Server
Runs the FastAPI server with uvicorn
"""
import uvicorn
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def main():
    """Start the server"""
    print("="*70)
    print("  🚀 STARTING NYC TLC ANALYTICS BACKEND API SERVER")
    print("="*70)
    print()
    print("Server will start on: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
    print()
    print("Default credentials:")
    print("  Username: admin")
    print("  Password: secret")
    print()
    print("Press CTRL+C to stop the server")
    print("="*70)
    print()
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("  Server stopped by user")
        print("="*70)
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        print("\nPlease check:")
        print("1. Port 8000 is not already in use")
        print("2. All required packages are installed")
        print("3. .env file is properly configured")


if __name__ == "__main__":
    main()
