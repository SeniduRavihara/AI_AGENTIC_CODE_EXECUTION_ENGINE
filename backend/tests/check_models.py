"""
Check what Gemini models are available
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def list_available_models():
    """List all available Gemini models"""
    
    print("🔍 Checking Available Gemini Models")
    print("=" * 50)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key found!")
        return
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # List all models
        print("📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"   ✅ {model.name}")
            else:
                print(f"   ❌ {model.name} (no generateContent)")
        
        print("\n🎯 Trying the first available model...")
        
        # Try the first available model
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name
                print(f"Testing with: {model_name}")
                
                try:
                    model_obj = genai.GenerativeModel(model_name)
                    response = model_obj.generate_content("Say 'Hello, AI is working!'")
                    print(f"✅ SUCCESS! Response: {response.text}")
                    return model_name
                except Exception as e:
                    print(f"❌ Failed: {e}")
        
        print("❌ No working models found!")
        return None
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return None

if __name__ == "__main__":
    working_model = list_available_models()
    
    if working_model:
        print(f"\n🎉 Working model found: {working_model}")
        print("Update your code to use this model name!")
    else:
        print("\n❌ No working models found. Check your API key and billing!")
