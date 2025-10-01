"""
Easy Benchmark Runner - Run benchmarks from backend root
"""

import os
import sys
import subprocess

def main():
    """Main function to run benchmarks"""
    print("🚀 AI Agent Performance Benchmark Runner")
    print("=" * 50)
    
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running or not healthy")
            print("Please start the server first:")
            print("   python run_server.py")
            return
    except:
        print("❌ Cannot connect to server")
        print("Please start the server first:")
        print("   python run_server.py")
        return
    
    print("✅ Server is running and healthy")
    
    # Change to benchmark directory
    benchmark_dir = os.path.join(os.path.dirname(__file__), "benchmark")
    
    if not os.path.exists(benchmark_dir):
        print("❌ Benchmark directory not found")
        return
    
    print("\nChoose benchmark type:")
    print("1. Quick Test (Simple comparison)")
    print("2. Quick Benchmark (Turbo mode only)")
    print("3. Full Benchmark (All speed modes)")
    print("4. Custom Benchmark (Selected algorithms)")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🧪 Running Quick Test...")
                subprocess.run([sys.executable, "test_benchmark.py"], cwd=benchmark_dir)
                break
            elif choice == "2":
                print("\n⚡ Running Quick Benchmark...")
                subprocess.run([sys.executable, "run_benchmark.py"], cwd=benchmark_dir, input="1\n")
                break
            elif choice == "3":
                print("\n🚀 Running Full Benchmark...")
                subprocess.run([sys.executable, "run_benchmark.py"], cwd=benchmark_dir, input="2\n")
                break
            elif choice == "4":
                print("\n🎯 Running Custom Benchmark...")
                subprocess.run([sys.executable, "run_benchmark.py"], cwd=benchmark_dir, input="3\n")
                break
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break

if __name__ == "__main__":
    main()

