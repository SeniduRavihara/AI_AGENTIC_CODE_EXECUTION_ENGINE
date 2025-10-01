"""
Test the benchmark system with a simple algorithm
"""

import asyncio
import requests
import time
import subprocess
import sys
import tempfile
import os


def test_normal_execution():
    """Test normal Python execution"""
    code = """
def simple_test(n):
    result = 0
    for i in range(n):
        result += i * 2
    return result

result = simple_test(1000)
print(f"Result: {result}")
"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Execute with Python
        start_time = time.time()
        result = subprocess.run([sys.executable, temp_file], 
                              capture_output=True, text=True, timeout=30)
        end_time = time.time()
        
        print(f"✅ Normal Python Execution:")
        print(f"   Time: {end_time - start_time:.3f}s")
        print(f"   Output: {result.stdout.strip()}")
        print(f"   Success: {result.returncode == 0}")
        
        return {
            "success": result.returncode == 0,
            "execution_time": end_time - start_time,
            "output": result.stdout.strip()
        }
        
    except Exception as e:
        print(f"❌ Normal execution failed: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_ai_execution():
    """Test AI agent execution"""
    code = """
def simple_test(n):
    result = 0
    for i in range(n):
        result += i * 2
    return result

result = simple_test(1000)
print(f"Result: {result}")
"""
    
    payload = {
        "code": code,
        "language": "python",
        "problem_type": "general",
        "speed_mode": "turbo"
    }
    
    try:
        start_time = time.time()
        response = requests.post("http://localhost:8000/execute-speed", json=payload, timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI Agent Execution:")
            print(f"   Time: {end_time - start_time:.3f}s")
            print(f"   Success: {result.get('success', False)}")
            print(f"   Console Output: {result.get('console_output', [])}")
            print(f"   Performance Grade: {result.get('speed_coordinator', {}).get('performance_grade', 'Unknown')}")
            
            return {
                "success": result.get('success', False),
                "execution_time": end_time - start_time,
                "output": result.get('console_output', []),
                "performance_grade": result.get('speed_coordinator', {}).get('performance_grade', 'Unknown')
            }
        else:
            print(f"❌ AI execution failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"❌ AI execution failed: {str(e)}")
        return {"success": False, "error": str(e)}


async def main():
    """Run simple benchmark test"""
    print("🧪 Simple Benchmark Test")
    print("=" * 40)
    
    # Test normal execution
    print("\n1. Testing Normal Python Execution...")
    normal_result = test_normal_execution()
    
    # Test AI execution
    print("\n2. Testing AI Agent Execution...")
    ai_result = await test_ai_execution()
    
    # Compare results
    print("\n📊 COMPARISON RESULTS")
    print("=" * 40)
    
    if normal_result['success'] and ai_result['success']:
        normal_time = normal_result['execution_time']
        ai_time = ai_result['execution_time']
        
        if ai_time > 0:
            speedup = normal_time / ai_time
            improvement = ((normal_time - ai_time) / normal_time) * 100
            
            print(f"Normal Python: {normal_time:.3f}s")
            print(f"AI Agent:      {ai_time:.3f}s")
            print(f"Speedup:       {speedup:.1f}x")
            print(f"Improvement:   {improvement:.1f}%")
            
            if speedup > 1:
                print("🎉 AI Agent is FASTER!")
            elif speedup < 1:
                print("⚠️ Normal Python is faster")
            else:
                print("🤝 Similar performance")
        else:
            print("❌ Cannot calculate speedup (AI time = 0)")
    else:
        print("❌ One or both executions failed")
        if not normal_result['success']:
            print(f"   Normal execution error: {normal_result.get('error', 'Unknown')}")
        if not ai_result['success']:
            print(f"   AI execution error: {ai_result.get('error', 'Unknown')}")
    
    print("\n✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(main())
