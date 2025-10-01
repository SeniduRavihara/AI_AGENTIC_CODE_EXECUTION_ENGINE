"""
Setup script for benchmark system
"""

import subprocess
import sys
import os

def install_requirements():
    """Install benchmark requirements"""
    print("📦 Installing benchmark requirements...")
    
    requirements_file = os.path.join(os.path.dirname(__file__), "benchmark_requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("❌ benchmark_requirements.txt not found")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_server():
    """Check if server is running"""
    print("🔍 Checking if server is running...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print("❌ Server is not healthy")
            return False
    except ImportError:
        print("❌ requests module not available")
        return False
    except:
        print("❌ Server is not running")
        print("Please start the server first:")
        print("   cd .. && python run_server.py")
        return False

def main():
    """Main setup function"""
    print("🚀 Benchmark System Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return
    
    print("\n" + "=" * 40)
    
    # Check server
    if not check_server():
        print("❌ Setup failed at server check")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\nYou can now run benchmarks:")
    print("  python test_benchmark.py      # Quick test")
    print("  python run_benchmark.py       # Full benchmark system")
    print("  python benchmark_system.py    # Direct benchmark")

if __name__ == "__main__":
    main()

