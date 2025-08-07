#!/usr/bin/env python
"""
Simple run script for the Real-Time Chat Application
"""
import os
import sys
import subprocess

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import flask
        import flask_socketio
        import werkzeug
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the application"""
    print("🚀 Starting Real-Time Chat Application...")
    print("=" * 50)
    
    # Check if requirements are installed
    if not check_requirements():
        sys.exit(1)
    
    # Set default environment variables
    os.environ.setdefault('DEBUG', 'True')
    os.environ.setdefault('PORT', '5000')
    
    # Import and run the main application
    try:
        from main import app, socketio
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('DEBUG', 'True').lower() == 'true'
        
        print(f"🌐 Server starting on http://localhost:{port}")
        print("📝 Register the first user to become admin")
        print("⚡ Press Ctrl+C to stop the server")
        print("=" * 50)
        
        socketio.run(app, host='0.0.0.0', port=port, debug=debug)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
