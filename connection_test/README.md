# Connection Tests

This folder contains utilities to test connections to remote models deployed on Google Colab via localtunnel.

## Files

- `mistral_connection.py` - Test connection to Mistral-7B model
- `embedding_connection.py` - Test connection to sentence-transformers embedding model
- `run_tests.py` - Main script to run all connection tests

## Setup

1. **Copy environment template:**
   ```bash
   cp env.local.example .env
   ```

2. **Configure your .env file:**
   ```bash
   # Edit .env and add your actual values
   MISTRAL_MODEL_URL=https://your-mistral-subdomain.loca.lt
   EMBEDDING_MODEL_URL=https://your-embedding-subdomain.loca.lt
   ```

## Usage

### Run all tests:
```bash
python connection_test/run_tests.py
```

### Run individual tests:
```bash
# Test Mistral model only
python connection_test/mistral_connection.py

# Test embedding model only
python connection_test/embedding_connection.py
```

## Expected Output

When tests are successful, you should see:
- ✅ Connection successful
- 🤖 Text completion working (for Mistral)
- 🧠 Embedding generation working (for sentence-transformers)

## Troubleshooting

### Connection Failed
- Check if your Colab server is running
- Verify the localtunnel URL is correct
- Ensure the server is accessible from your local machine

### Model Not Responding
- Check if the model is loaded in Colab
- Verify the API endpoints match your server setup
- Check server logs in Colab for errors

### Environment Variables
- Make sure `.env` file exists and is properly configured
- Verify all required variables are set
- Check for typos in URLs or API keys 