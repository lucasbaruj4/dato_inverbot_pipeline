"""
Connection Test Runner

This script runs all connection tests for the remote models.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import from src
sys.path.append(str(Path(__file__).parent.parent))

from connection_test.mistral_connection import MistralConnectionTest
from connection_test.embedding_connection import EmbeddingConnectionTest

def run_mistral_test():
    """Run Mistral model connection test."""
    print("🤖 Testing Mistral Model Connection")
    print("=" * 60)
    
    tester = MistralConnectionTest()
    
    # Show configuration
    print("📋 Configuration:")
    info = tester.get_server_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    
    # Test connection
    print("🔍 Testing connection...")
    result = tester.test_connection()
    print(f"  Status: {result['status']}")
    print(f"  Message: {result['message']}")
    
    if result['status'] == 'success':
        print("✅ Connection successful!")
        
        # Test completion
        print("\n🤖 Testing text completion...")
        completion = tester.test_completion("What is the capital of France?")
        print(f"  Status: {completion['status']}")
        if completion['status'] == 'success':
            print(f"  Response: {completion['generated_text']}")
        else:
            print(f"  Error: {completion['message']}")
    else:
        print("❌ Connection failed!")
        print(f"  Error: {result['message']}")
    
    print("\n" + "=" * 60 + "\n")

def run_embedding_test():
    """Run embedding model connection test."""
    print("🧠 Testing Embedding Model Connection")
    print("=" * 60)
    
    tester = EmbeddingConnectionTest()
    
    # Show configuration
    print("📋 Configuration:")
    info = tester.get_server_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    
    # Test connection
    print("🔍 Testing connection...")
    result = tester.test_connection()
    print(f"  Status: {result['status']}")
    print(f"  Message: {result['message']}")
    
    if result['status'] == 'success':
        print("✅ Connection successful!")
        
        # Test embedding
        print("\n🧠 Testing text embedding...")
        embedding = tester.test_embedding("This is a test sentence.")
        print(f"  Status: {embedding['status']}")
        if embedding['status'] == 'success':
            print(f"  Embedding Length: {embedding['embedding_length']}")
            print(f"  Sample: {embedding['embedding_sample']}")
        else:
            print(f"  Error: {embedding['message']}")
    else:
        print("❌ Connection failed!")
        print(f"  Error: {result['message']}")
    
    print("\n" + "=" * 60 + "\n")

def main():
    """Run all connection tests."""
    print("🚀 Starting Connection Tests")
    print("=" * 60)
    print()
    
    # Check if .env.local file exists
    if not os.path.exists('.env.local'):
        print("⚠️  Warning: .env.local file not found!")
        print("   Please copy env.local.example to .env.local and configure your model URLs.")
        print("   You can still run tests, but they will use default/empty values.")
        print()
    
    # Test Mistral model
    run_mistral_test()
    
    # Test embedding model
    run_embedding_test()
    
    print("🎉 All connection tests completed!")
    print("\n📝 Next steps:")
    print("   1. Configure your .env file with actual URLs and API keys")
    print("   2. Deploy your models on Colab with localtunnel")
    print("   3. Run the tests again to verify connections")

if __name__ == "__main__":
    main() 