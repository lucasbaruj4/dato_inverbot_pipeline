"""
Mistral Model Connection Test

This module provides utilities to test the connection to the Mistral model
deployed on Google Colab via localtunnel.
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env.local for model connections
load_dotenv('.env.local')

class MistralConnectionTest:
    """Test connection to Mistral model server."""
    
    def __init__(self):
        self.base_url = os.getenv('MISTRAL_MODEL_URL')
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.headers = {
            'bypass-tunnel-reminder': 'true',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test basic connection to the Mistral server."""
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
    
    def test_completion(self, prompt: str = "Hello, how are you?") -> Dict[str, Any]:
        """Test text completion with the Mistral model."""
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": 50,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract the generated text from the response
                full_response = result.get('response', '')
                # Remove the original prompt from the response to get just the generated part
                original_prompt = result.get('prompt', '')
                generated_text = full_response.replace(original_prompt, '').strip()
                
                return {
                    'status': 'success',
                    'message': 'Completion successful',
                    'response': result,
                    'generated_text': generated_text
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Completion failed with status {response.status_code}',
                    'response': response.text
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Completion error: {str(e)}'
            }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the server configuration."""
        return {
            'mistral_url': self.base_url,
            'supabase_url': self.supabase_url,
            'has_supabase_key': bool(self.supabase_key),
            'has_pinecone_key': bool(self.pinecone_api_key),
            'headers': self.headers
        }

def main():
    """Main function to run connection tests."""
    print("🔗 Testing Mistral Model Connection...")
    print("=" * 50)
    
    # Initialize connection test
    tester = MistralConnectionTest()
    
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
    
    # Test completion if connection successful
    if connection_result['status'] == 'success':
        print("🤖 Testing text completion...")
        test_prompt = "What is artificial intelligence? Please explain in one sentence."
        completion_result = tester.test_completion(test_prompt)
        print(f"  Status: {completion_result['status']}")
        print(f"  Message: {completion_result['message']}")
        if completion_result['status'] == 'success':
            print(f"  Prompt: {test_prompt}")
            print(f"  Generated Text: {completion_result['generated_text']}")
            print(f"  Full Response: {completion_result['response']}")
        else:
            print(f"  Error: {completion_result['message']}")
        print()
    
    print("✅ Connection test completed!")

if __name__ == "__main__":
    main() 