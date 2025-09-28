"""
Quick server runner with API key setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_and_run():
    """Setup API key and run server"""
    
    print("🚀 AI Python Interpreter Server Setup")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found!")
        print()
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print()
        api_key = input("Enter your Gemini API key: ").strip()
        
        if api_key:
            os.environ['GEMINI_API_KEY'] = api_key
            print("✅ API key set!")
        else:
            print("❌ No API key provided. Exiting.")
            return
    
    print("🤖 Starting AI server...")
    print("📡 Server: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Import and run server
    try:
        import uvicorn
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    setup_and_run()
