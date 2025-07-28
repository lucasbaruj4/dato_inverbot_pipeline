#!/usr/bin/env python3
"""
Context-Efficient Google AI Migration Test

This test verifies the Google AI migration works correctly with:
- Minimal token usage (small inputs/outputs)
- Synthetic data only
- No database writes
- Core component testing
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_config
from utils.logging import get_logger
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


def create_synthetic_data() -> Dict[str, Any]:
    """Create minimal synthetic data for testing."""
    return {
        "url": "https://example.com/test",
        "content": "This is a test document about AI and machine learning. It contains basic information for testing purposes.",
        "metadata": {
            "title": "Test Document",
            "source": "synthetic",
            "type": "test"
        }
    }


def test_google_llm():
    """Test Google LLM directly."""
    print("\n🧠 Testing Google LLM...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        # Test with minimal prompt
        test_prompt = "Say 'test' if you can read this."
        response = llm.invoke(test_prompt)
        
        if "test" in response.content.lower():
            print("  ✅ Google LLM working")
            print(f"      Model: {model_config['llm_model']}")
            print(f"      Response: {response.content[:50]}...")
        else:
            print("  ❌ Google LLM failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Google LLM Failed: {str(e)}")
        return False


def test_google_embeddings():
    """Test Google embeddings directly."""
    print("\n🔢 Testing Google Embeddings...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create embedding model
        embedding_model = GoogleGenerativeAIEmbeddings(
            model=model_config["embedding_model"],
            google_api_key=model_config["api_key"]
        )
        
        # Test with minimal text
        test_text = "test"
        embeddings = embedding_model.embed_documents([test_text])
        
        if embeddings and len(embeddings[0]) > 0:
            print("  ✅ Google Embeddings working")
            print(f"      Model: {model_config['embedding_model']}")
            print(f"      Embedding dimension: {len(embeddings[0])}")
        else:
            print("  ❌ Google Embeddings failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Google Embeddings Failed: {str(e)}")
        return False


def test_configuration():
    """Test configuration loading."""
    print("\n⚙️ Testing Configuration...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        print("  ✅ Configuration loaded successfully")
        print(f"      LLM Model: {model_config['llm_model']}")
        print(f"      Embedding Model: {model_config['embedding_model']}")
        print(f"      Max Input Tokens: {model_config['max_input_tokens']}")
        print(f"      Max Output Tokens: {model_config['max_output_tokens']}")
        print(f"      Temperature: {model_config['temperature']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration Failed: {str(e)}")
        return False


def test_synthetic_data_processing():
    """Test processing synthetic data with Google AI."""
    print("\n📊 Testing Synthetic Data Processing...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        # Create embedding model
        embedding_model = GoogleGenerativeAIEmbeddings(
            model=model_config["embedding_model"],
            google_api_key=model_config["api_key"]
        )
        
        # Test with synthetic data
        synthetic_data = create_synthetic_data()
        
        # Test LLM processing
        prompt = f"Summarize this content in 10 words: {synthetic_data['content']}"
        response = llm.invoke(prompt)
        
        print("  ✅ LLM Processing working")
        print(f"      Summary: {response.content}")
        
        # Test embedding generation
        embeddings = embedding_model.embed_documents([synthetic_data['content']])
        
        print("  ✅ Embedding Generation working")
        print(f"      Embedding count: {len(embeddings)}")
        print(f"      Embedding dimension: {len(embeddings[0])}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Synthetic Data Processing Failed: {str(e)}")
        return False


def main():
    """Run context-efficient Google AI migration tests."""
    print("🚀 Starting Context-Efficient Google AI Migration Tests")
    print("=" * 60)
    print("📊 Testing with minimal tokens and synthetic data only")
    print("🔒 No database writes - Core component testing only")
    print("=" * 60)
    
    # Test each component
    results = []
    
    results.append(test_configuration())
    results.append(test_google_llm())
    results.append(test_google_embeddings())
    results.append(test_synthetic_data_processing())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    test_names = [
        "Configuration",
        "Google LLM", 
        "Google Embeddings",
        "Synthetic Data Processing"
    ]
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 SUCCESS: Google AI migration is working perfectly!")
        print("   Core components are ready for integration.")
        print("   Next: Test CrewAI agents and full pipeline.")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check configuration.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 