# Connection Tests

This directory contains connection tests for the Inverbot Data Pipeline.

## Overview

These tests verify that all external services and APIs are properly configured and accessible.

## Available Tests

### Google AI API Connection Test
Tests the connection to Google's Gemini and embedding models.

**Usage:**
```bash
python connection_test/run_tests.py
```

## Test Results

Tests will output connection status for:
- ✅ Google Gemini LLM (gemini-2.5-flash-lite)
- ✅ Google Embedding Model (text-embedding-004)
- ✅ Supabase Database Connection
- ✅ Pinecone Vector Database Connection

## Environment Variables Required

Make sure your `.env.local` file contains:
```
GOOGLE_API_KEY=your_google_api_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_key
PINECONE_API_KEY=your_pinecone_key
```

## Testing Strategy

- **Google AI Models**: Free tier for development/testing
- **Cost-Efficient**: Small token limits for prototype validation
- **Database Safety**: Tests connection without data writes

## Troubleshooting

If tests fail:
1. Verify API keys in `.env.local`
2. Check network connectivity
3. Ensure services are not rate-limited
4. Verify Google AI API is enabled in your project

For Google AI setup:
- Go to [Google AI Studio](https://aistudio.google.com/)
- Create API key
- Ensure billing is set up if needed (free tier available) 