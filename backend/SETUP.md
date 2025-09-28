# 🚀 Setup Instructions

## 1. Create Environment File

Copy the template and add your API key:

```bash
# Copy the template
copy env_template.txt .env

# Edit .env file and add your actual Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

## 2. Get Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key
4. Paste it in your `.env` file

## 3. Run the Server

```bash
# Activate virtual environment
venv\Scripts\activate

# Run server
python run_server.py
```

## 4. Test the API

```bash
# Test with client
python test_client.py

# Or visit: http://localhost:8000/docs
```

## 🔒 Security Note

- **Never commit your `.env` file to GitHub**
- The `.gitignore` file is already set up to ignore `.env`
- Only commit the `env_template.txt` file

## 📡 API Endpoints

- `POST /execute` - Execute Python code
- `POST /execute-simple` - Simple execution
- `GET /health` - Health check
- `GET /docs` - API documentation

## 🎯 Example Usage

```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = 2\ny = x + 3\nif y > 4:\n    z = y * 2",
    "language": "python"
  }'
```
