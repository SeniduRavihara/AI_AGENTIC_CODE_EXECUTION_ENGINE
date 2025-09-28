"""
Test client for AI Python Interpreter Server
"""

import requests
import json
import time

SERVER_URL = "http://localhost:8000"

def test_server():
    """Test the AI server"""
    
    print("🧪 Testing AI Python Interpreter Server")
    print("=" * 50)
    
    # Test health check
    print("1. Health check...")
    try:
        response = requests.get(f"{SERVER_URL}/health")
        if response.status_code == 200:
            print("✅ Server healthy")
            print(f"   {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect: {e}")
        print("Start server: python main.py")
        return
    
    print()
    
    # Test code execution
    test_cases = [
        {
            "name": "Basic Math",
            "code": "x = 2\ny = x + 3\nz = y * 2"
        },
        {
            "name": "If Statement", 
            "code": "x = 5\nif x > 3:\n    y = x * 2\nelse:\n    y = 0"
        },
        {
            "name": "Complex",
            "code": "a = 2\nb = 3\nc = a + b * 2\nd = (a + b) * 2"
        }
    ]
    
    for i, test in enumerate(test_cases, 2):
        print(f"{i}. Testing {test['name']}...")
        print(f"   Code: {test['code']}")
        
        try:
            start = time.time()
            
            response = requests.post(f"{SERVER_URL}/execute", json={
                "code": test['code'],
                "language": "python"
            })
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success")
                print(f"   Variables: {result['final_variables']}")
                print(f"   Confidence: {result['confidence']:.2f}")
                print(f"   Time: {elapsed:.2f}s")
                print(f"   AI: {result['ai_reasoning'][:80]}...")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    print("🎉 Testing complete!")


def test_simple():
    """Test simple endpoint"""
    
    print("🧪 Testing Simple Endpoint")
    print("=" * 30)
    
    code = "x = 10; y = x * 2; z = y + 5"
    print(f"Code: {code}")
    
    try:
        response = requests.post(f"{SERVER_URL}/execute-simple", 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(code))
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success")
            print(f"   Result: {result}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Choose test:")
    print("1. Full test")
    print("2. Simple test")
    
    choice = input("Choice (1 or 2): ").strip()
    
    if choice == "2":
        test_simple()
    else:
        test_server()
