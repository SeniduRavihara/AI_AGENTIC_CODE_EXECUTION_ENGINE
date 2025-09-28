# 🤖 AI Python Interpreter Server

**FastAPI server with real AI agents using Google Gemini for Python code execution simulation**

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Gemini API Key
```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run Server
```bash
python main.py
```

Server runs at: `http://localhost:8000`

## 🔥 API Endpoints

### POST `/execute`
Execute Python code with AI:

```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = 2\ny = x + 3\nif y > 4:\n    z = y * 2\nelse:\n    z = 0",
    "language": "python"
  }'
```

### POST `/execute-simple`
Simple endpoint:

```bash
curl -X POST "http://localhost:8000/execute-simple" \
  -H "Content-Type: application/json" \
  -d '"x = 5; y = x * 2"'
```

### GET `/health`
Health check:

```bash
curl http://localhost:8000/health
```

## 🧠 AI Response

```json
{
  "success": true,
  "final_variables": {
    "x": 2,
    "y": 5,
    "z": 10
  },
  "execution_steps": [
    "Step 1: AI parsed x = 2",
    "Step 2: AI stored x = 2",
    "Step 3: AI evaluated y = x + 3 = 5"
  ],
  "ai_reasoning": "AI analyzed the code and determined...",
  "confidence": 0.95,
  "execution_time": 2.3,
  "timestamp": "2024-01-15T10:30:00",
  "coordinator": {
    "agent_used": "GeminiAgent",
    "execution_method": "AI reasoning with Google Gemini"
  }
}
```

## 🧪 Testing

```bash
# Test the server
python tests/test_client.py

# Run simple API test
python tests/simple_test.py

# Check available models
python tests/check_models.py
```

## 🎯 What This Does

- ✅ **Real AI**: Uses Google Gemini for intelligent code execution
- ✅ **FastAPI**: Clean REST API
- ✅ **Async**: Fast, non-blocking execution
- ✅ **JSON API**: Easy integration

## 🔧 Example Usage

### Python
```python
import requests

response = requests.post("http://localhost:8000/execute", json={
    "code": "x = 2\ny = x + 3\nif y > 4:\n    z = y * 2",
    "language": "python"
})

result = response.json()
print(f"Variables: {result['final_variables']}")
print(f"AI reasoning: {result['ai_reasoning']}")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'x = 2\ny = x + 3\nif y > 4:\n    z = y * 2',
    language: 'python'
  })
});

const result = await response.json();
console.log('Result:', result.final_variables);
```

## 🎉 That's It!

**Clean, simple, real AI agents with FastAPI server!**

Get Gemini API key: https://makersuite.google.com/app/apikey
