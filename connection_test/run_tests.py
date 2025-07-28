"""
Connection Test Runner for Inverbot Data Pipeline

This script tests connections to all external services:
- Google AI (Gemini LLM + Embeddings)
- Supabase (PostgreSQL)
- Pinecone (Vector Database)
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_config, validate_config
from utils.logging import get_logger
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import supabase
import pinecone

logger = get_logger(__name__)


def test_google_ai_connection():
    """Test Google AI (Gemini LLM + Embeddings) connection."""
    print("\n🧠 Testing Google AI Connection...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Test Gemini LLM
        print("  📝 Testing Gemini LLM...")
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=0.3,
            max_tokens=50
        )
        
        # Test with a simple message
        response = llm.invoke("Hello, this is a connection test.")
        if response and response.content:
            print(f"  ✅ Gemini LLM ({model_config['llm_model']}) - Connected")
            print(f"      Response: {response.content[:100]}...")
        else:
            print(f"  ❌ Gemini LLM - No response received")
            return False
        
        # Test Embeddings
        print("  🔢 Testing Google Embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model=model_config["embedding_model"],
            google_api_key=model_config["api_key"]
        )
        
        # Test embedding generation
        test_embedding = embeddings.embed_query("Test embedding generation")
        if test_embedding and len(test_embedding) > 0:
            print(f"  ✅ Google Embeddings ({model_config['embedding_model']}) - Connected")
            print(f"      Embedding dimension: {len(test_embedding)}")
        else:
            print(f"  ❌ Google Embeddings - Failed to generate embedding")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Google AI Connection Failed: {str(e)}")
        return False


def test_supabase_connection():
    """Test Supabase database connection."""
    print("\n🗄️ Testing Supabase Connection...")
    
    try:
        config = get_config()
        
        # Create Supabase client
        client = supabase.create_client(
            config.supabase_url,
            config.supabase_key
        )
        
        # Test connection with a simple query
        response = client.table("pg_catalog.pg_tables").select("tablename").limit(1).execute()
        
        if response.data is not None:
            print("  ✅ Supabase Database - Connected")
            print(f"      URL: {config.supabase_url}")
            return True
        else:
            print("  ❌ Supabase Database - Connection failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Supabase Connection Failed: {str(e)}")
        return False


def test_pinecone_connection():
    """Test Pinecone vector database connection."""
    print("\n🌲 Testing Pinecone Connection...")
    
    try:
        config = get_config()
        
        # Initialize Pinecone
        pc = pinecone.Pinecone(api_key=config.pinecone_api_key)
        
        # List indexes to test connection
        indexes = pc.list_indexes()
        
        print("  ✅ Pinecone Vector Database - Connected")
        print(f"      Environment: {config.pinecone_environment}")
        print(f"      Available indexes: {len(indexes)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pinecone Connection Failed: {str(e)}")
        return False


def test_configuration():
    """Test configuration validation."""
    print("\n⚙️ Testing Configuration...")
    
    try:
        if validate_config():
            print("  ✅ Configuration - Valid")
            return True
        else:
            print("  ❌ Configuration - Invalid")
            return False
            
    except Exception as e:
        print(f"  ❌ Configuration Test Failed: {str(e)}")
        return False


def main():
    """Run all connection tests."""
    print("🚀 Starting Inverbot Data Pipeline Connection Tests")
    print("=" * 60)
    
    # Test results
    results = {}
    
    # Run tests
    results['config'] = test_configuration()
    results['google_ai'] = test_google_ai_connection()
    results['supabase'] = test_supabase_connection()
    results['pinecone'] = test_pinecone_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Connection Test Results:")
    print("-" * 30)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for service, status in results.items():
        status_icon = "✅" if status else "❌"
        service_name = service.replace('_', ' ').title()
        print(f"  {status_icon} {service_name}")
    
    print("-" * 30)
    print(f"  📈 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All connections successful! Ready to run the pipeline.")
        return 0
    else:
        print(f"\n⚠️ {total_tests - passed_tests} connection(s) failed. Please check configuration.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 