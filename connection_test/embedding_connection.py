"""
Embedding Model Connection Test

This module provides utilities to test the connection to the embedding model
deployed on Google Colab via localtunnel.
"""

import os
import requests
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env.local for model connections
load_dotenv('.env.local')

class EmbeddingConnectionTest:
    """Test connection to embedding model server."""
    
    def __init__(self):
        self.base_url = os.getenv('EMBEDDING_MODEL_URL')
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.headers = {
            'bypass-tunnel-reminder': 'true',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test basic connection to the embedding server."""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'Connection successful',
                    'response': response.json() if response.content else None
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Server responded with status {response.status_code}',
                    'response': response.text
                }
                
        except requests.exceptions.ConnectionError:
            return {
                'status': 'error',
                'message': 'Connection failed - server might be down or URL incorrect'
            }
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'message': 'Connection timeout - server might be overloaded'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }
    
    def test_embedding(self, text: str = "Hello world") -> Dict[str, Any]:
        """Test text embedding with the model."""
        try:
            payload = {
                "text": text
            }
            
            response = requests.post(
                f"{self.base_url}/embed",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                embeddings = result.get('embeddings', [])
                embedding = embeddings[0] if embeddings else []
                return {
                    'status': 'success',
                    'message': 'Embedding successful',
                    'embedding_length': len(embedding),
                    'embedding_sample': embedding[:5] if embedding else []
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Embedding failed with status {response.status_code}',
                    'response': response.text
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Embedding error: {str(e)}'
            }
    
    def test_batch_embedding(self, texts: List[str]) -> Dict[str, Any]:
        """Test batch embedding with multiple texts."""
        try:
            payload = {
                "texts": texts
            }
            
            response = requests.post(
                f"{self.base_url}/embed",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                embeddings = result.get('embeddings', [])
                return {
                    'status': 'success',
                    'message': f'Batch embedding successful for {len(texts)} texts',
                    'embeddings_count': len(embeddings),
                    'embedding_dimension': len(embeddings[0]) if embeddings else 0
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Batch embedding failed with status {response.status_code}',
                    'response': response.text
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Batch embedding error: {str(e)}'
            }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the server configuration."""
        return {
            'embedding_url': self.base_url,
            'supabase_url': self.supabase_url,
            'has_supabase_key': bool(self.supabase_key),
            'has_pinecone_key': bool(self.pinecone_api_key),
            'headers': self.headers
        }

def main():
    """Main function to run connection tests."""
    print("🔗 Testing Embedding Model Connection...")
    print("=" * 50)
    
    # Initialize connection test
    tester = EmbeddingConnectionTest()
    
    # Show server info
    print("📋 Server Configuration:")
    info = tester.get_server_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    
    # Test basic connection
    print("🔍 Testing basic connection...")
    connection_result = tester.test_connection()
    print(f"  Status: {connection_result['status']}")
    print(f"  Message: {connection_result['message']}")
    if 'response' in connection_result and connection_result['response']:
        print(f"  Response: {connection_result['response']}")
    print()
    
    # Test embedding if connection successful
    if connection_result['status'] == 'success':
        print("🧠 Testing text embedding...")
        embedding_result = tester.test_embedding("This is a test sentence for embedding.")
        print(f"  Status: {embedding_result['status']}")
        print(f"  Message: {embedding_result['message']}")
        if embedding_result['status'] == 'success':
            print(f"  Embedding Length: {embedding_result['embedding_length']}")
            print(f"  Embedding Sample: {embedding_result['embedding_sample']}")
        print()
        
        # Test batch embedding
        print("📦 Testing batch embedding...")
        batch_result = tester.test_batch_embedding([
            "First sentence for testing.",
            "Second sentence for testing.",
            "Third sentence for testing."
        ])
        print(f"  Status: {batch_result['status']}")
        print(f"  Message: {batch_result['message']}")
        if batch_result['status'] == 'success':
            print(f"  Embeddings Count: {batch_result['embeddings_count']}")
            print(f"  Embedding Dimension: {batch_result['embedding_dimension']}")
        print()
    
    print("✅ Connection test completed!")

if __name__ == "__main__":
    main() 