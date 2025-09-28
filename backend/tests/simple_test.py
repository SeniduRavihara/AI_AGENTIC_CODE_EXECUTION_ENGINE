"""
Simple test to check if Gemini AI is working
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_directly():
    """Test Gemini API directly"""
    
    print("🧪 Testing Gemini API Directly")
    print("=" * 40)
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key found!")
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with simple model
        print("🤖 Testing with gemini-pro...")
        model = genai.GenerativeModel('gemini-pro')
        
        # Simple test
        response = model.generate_content("Say 'Hello, AI is working!' if you can read this.")
        
        print("✅ AI Response:")
        print(f"   {response.text}")
        print()
        print("🎉 Gemini AI is working perfectly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Try alternative models
        print("\n🔄 Trying alternative models...")
        
        models_to_try = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'models/gemini-pro',
            'gemini-pro-vision'
        ]
        
        for model_name in models_to_try:
            try:
                print(f"   Trying {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello")
                print(f"   ✅ {model_name} works!")
                print(f"   Response: {response.text[:50]}...")
                return True
            except Exception as model_error:
                print(f"   ❌ {model_name} failed: {model_error}")
        
        return False

def test_python_execution():
    """Test Python code execution with AI"""
    
    print("\n🐍 Testing Python Code Execution")
    print("=" * 40)
    
    try:
        from agents import GeminiAgent
        
        agent = GeminiAgent()
        
        # Simple test
        code = "x = 2\ny = x + 3"
        print(f"Code: {code}")
        
        import asyncio
        result = asyncio.run(agent.execute_python_code(code))
        
        print("✅ AI Execution Result:")
        print(f"   Success: {result.get('success')}")
        print(f"   Variables: {result.get('final_variables')}")
        print(f"   Reasoning: {result.get('ai_reasoning', '')[:100]}...")
        print(f"   Confidence: {result.get('confidence')}")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ Python execution test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Gemini AI Test")
    print("=" * 50)
    
    # Test 1: Direct API test
    api_works = test_gemini_directly()
    
    if api_works:
        # Test 2: Python execution test
        execution_works = test_python_execution()
        
        if execution_works:
            print("\n🎉 ALL TESTS PASSED!")
            print("Your AI Python interpreter is working!")
        else:
            print("\n⚠️ API works but Python execution has issues")
    else:
        print("\n❌ API test failed - check your API key and billing")
    
    print("\n" + "=" * 50)
