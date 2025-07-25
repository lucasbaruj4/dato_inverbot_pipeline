"""
Test script for the vectorization module.

This script tests the vectorization functionality including:
- VectorizationLogic class
- VectorizationAgent class
- Pinecone schema definitions and validation
- Connection to remote embedding model
"""

import sys
import os
import logging

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.vectorization import (
    VectorizationLogic, 
    VectorizationAgent, 
    VectorizationTasks,
    PINECONE_SCHEMAS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_pinecone_schemas():
    """Test Pinecone schema definitions and utilities."""
    print("\n=== Testing Pinecone Schemas ===")
    
    # Test available indexes
    print(f"Available Pinecone indexes: {len(PINECONE_SCHEMAS)}")
    for index_name in PINECONE_SCHEMAS.keys():
        print(f"  - {index_name}")
    
    # Test schema info
    financial_index = PINECONE_SCHEMAS.get("documentos-informes-vector", {})
    print(f"Financial index dimension: {financial_index.get('dimension', 'N/A')}")
    print(f"Financial index required fields: {len(financial_index.get('required_metadata', []))}")
    
    # Test utility functions
    from src.vectorization.pinecone_schemas import (
        get_pinecone_schema_info, 
        get_required_metadata, 
        validate_index_exists,
        get_index_dimension
    )
    
    # Test schema info retrieval
    schema_info = get_pinecone_schema_info("documentos-informes-vector")
    print(f"Schema info retrieved: {bool(schema_info)}")
    
    # Test required fields
    required_fields = get_required_metadata("documentos-informes-vector")
    print(f"Required fields: {len(required_fields)}")
    
    # Test index validation
    is_valid = validate_index_exists("documentos-informes-vector")
    print(f"Index validation: {is_valid}")
    
    # Test dimension retrieval
    dimension = get_index_dimension("documentos-informes-vector")
    print(f"Index dimension: {dimension}")
    
    print("✅ Pinecone schemas test completed")

def test_vectorization_logic():
    """Test the VectorizationLogic class."""
    print("\n=== Testing Vectorization Logic ===")
    
    try:
        # Create vectorization logic
        vectorization_logic = VectorizationLogic()
        print("✅ VectorizationLogic created successfully")
        
        # Test text chunking
        sample_text = """
        This is a sample financial report. It contains important information about the company's performance.
        The report includes details about revenue, expenses, and profitability. We can see that the company
        has shown strong growth in the last quarter. The financial statements indicate positive trends.
        """
        
        print("Testing text chunking...")
        chunks = vectorization_logic.chunk_text(sample_text, chunk_size=100, chunk_overlap=20)
        
        if chunks:
            print(f"✅ Text chunking completed. Chunks: {len(chunks)}")
            print(f"   First chunk length: {len(chunks[0])}")
        else:
            print("⚠️  Text chunking returned empty list")
        
        # Test embedding connection
        print("Testing embedding model connection...")
        connection_result = vectorization_logic.test_embedding_connection()
        
        if connection_result['status'] == 'success':
            print(f"✅ Connection successful: {connection_result['message']}")
        else:
            print(f"⚠️  Connection failed: {connection_result['message']}")
            print("   This is expected if the remote model is not running")
        
        # Test content processing (without actual embedding generation)
        print("Testing content processing...")
        source_info = {
            'source_id': 'test-001',
            'titulo_informe': 'Test Financial Report',
            'fecha_publicacion': '2023-12-31',
            'tipo_contenido': 'financial_report'
        }
        
        # This will fail if embedding model is not available, but we can test the structure
        try:
            vectors = vectorization_logic.process_content_for_index(
                sample_text, 
                source_info, 
                "documentos-informes-vector"
            )
            if vectors:
                print(f"✅ Content processing completed. Vectors: {len(vectors)}")
            else:
                print("⚠️  Content processing returned empty list (expected if model not available)")
        except Exception as e:
            print(f"⚠️  Content processing failed (expected if model not available): {e}")
        
        # Test available indexes
        available_indexes = vectorization_logic.get_available_indexes()
        print(f"✅ Available indexes retrieved: {len(available_indexes)}")
        
    except Exception as e:
        print(f"❌ Vectorization logic test failed: {e}")
        logger.error(f"Vectorization logic test failed: {e}")

def test_vectorization_agent():
    """Test the VectorizationAgent class."""
    print("\n=== Testing Vectorization Agent ===")
    
    try:
        # Create vectorization agent
        vectorization_agent = VectorizationAgent()
        print("✅ VectorizationAgent created successfully")
        
        # Test connection to remote embedding model
        print("Testing connection to remote embedding model...")
        connection_result = vectorization_agent.test_connection()
        
        if connection_result['status'] == 'success':
            print(f"✅ Connection successful: {connection_result['message']}")
        else:
            print(f"⚠️  Connection failed: {connection_result['message']}")
            print("   This is expected if the remote model is not running")
        
        # Get the CrewAI agent
        agent = vectorization_agent.get_agent()
        print("✅ CrewAI agent retrieved successfully")
        
        # Test available indexes
        available_indexes = vectorization_agent.get_available_indexes()
        print(f"✅ Available indexes retrieved: {len(available_indexes)}")
        
        # Test index info
        index_info = vectorization_agent.get_index_info("documentos-informes-vector")
        print(f"✅ Index info retrieved: {bool(index_info)}")
        
    except Exception as e:
        print(f"❌ Vectorization agent test failed: {e}")
        logger.error(f"Vectorization agent test failed: {e}")

def test_vectorization_tasks():
    """Test the VectorizationTasks class."""
    print("\n=== Testing Vectorization Tasks ===")
    
    try:
        # Create a mock agent for testing
        from crewai import Agent
        
        mock_agent = Agent(
            role='Test Agent',
            goal='Test vectorization tasks',
            backstory='A test agent for validating vectorization tasks',
            verbose=False
        )
        
        # Create vectorization tasks
        vectorization_tasks = VectorizationTasks(mock_agent)
        print("✅ VectorizationTasks created successfully")
        
        # Test creating tasks
        chunk_task = vectorization_tasks.chunk_and_embed_content()
        print("✅ Chunk and embed task created")
        
        pinecone_task = vectorization_tasks.prepare_pinecone_vectors()
        print("✅ Pinecone vectors task created")
        
        financial_task = vectorization_tasks.process_financial_documents()
        print("✅ Financial documents task created")
        
        macroeconomic_task = vectorization_tasks.process_macroeconomic_data()
        print("✅ Macroeconomic data task created")
        
        contracts_task = vectorization_tasks.process_public_contracts()
        print("✅ Public contracts task created")
        
        news_task = vectorization_tasks.process_news_content()
        print("✅ News content task created")
        
        validation_task = vectorization_tasks.validate_vector_data()
        print("✅ Vector validation task created")
        
    except Exception as e:
        print(f"❌ Vectorization tasks test failed: {e}")
        logger.error(f"Vectorization tasks test failed: {e}")

def test_sample_vectorization():
    """Test sample vectorization with different content types."""
    print("\n=== Testing Sample Vectorization ===")
    
    try:
        vectorization_logic = VectorizationLogic()
        
        # Test financial document processing
        financial_content = """
        Annual Financial Report 2023
        Company: ABC Corporation
        Date: December 31, 2023
        
        Executive Summary:
        ABC Corporation has achieved significant growth in 2023 with total revenue reaching $50 million,
        representing a 15% increase compared to the previous year. Net profit margin improved to 12%,
        driven by operational efficiency improvements and market expansion.
        
        Key Financial Metrics:
        - Total Assets: $75 million
        - Total Liabilities: $30 million
        - Net Equity: $45 million
        - Operating Income: $8 million
        - Net Income: $6 million
        """
        
        financial_source_info = {
            'source_id': 'financial-001',
            'titulo_informe': 'Annual Financial Report 2023',
            'fecha_publicacion': '2023-12-31',
            'tipo_contenido': 'financial_report',
            'id_emisor': 1
        }
        
        print("Testing financial document processing...")
        try:
            vectors = vectorization_logic.process_content_for_index(
                financial_content, 
                financial_source_info, 
                "documentos-informes-vector"
            )
            if vectors:
                print(f"✅ Financial processing completed. Vectors: {len(vectors)}")
            else:
                print("⚠️  Financial processing returned empty list (expected if model not available)")
        except Exception as e:
            print(f"⚠️  Financial processing failed (expected if model not available): {e}")
        
        # Test macroeconomic data processing
        macro_content = """
        Macroeconomic Indicators Report
        Date: December 2023
        Source: Central Bank
        
        Key Indicators:
        - Inflation Rate: 5.2%
        - GDP Growth: 3.1%
        - Unemployment Rate: 7.5%
        - Interest Rate: 4.25%
        - Exchange Rate: 1 USD = 6,800 PYG
        """
        
        macro_source_info = {
            'source_id': 'macro-001',
            'indicador_nombre': 'Monthly Economic Indicators',
            'fecha_dato': '2023-12-31',
            'fuente_dato': 'Central Bank',
            'id_dato': 1
        }
        
        print("Testing macroeconomic data processing...")
        try:
            vectors = vectorization_logic.process_content_for_index(
                macro_content, 
                macro_source_info, 
                "dato-macroeconomico-vector"
            )
            if vectors:
                print(f"✅ Macroeconomic processing completed. Vectors: {len(vectors)}")
            else:
                print("⚠️  Macroeconomic processing returned empty list (expected if model not available)")
        except Exception as e:
            print(f"⚠️  Macroeconomic processing failed (expected if model not available): {e}")
        
    except Exception as e:
        print(f"❌ Sample vectorization test failed: {e}")
        logger.error(f"Sample vectorization test failed: {e}")

def main():
    """Run all vectorization module tests."""
    print("🚀 Starting Vectorization Module Tests")
    print("=" * 50)
    
    try:
        # Test Pinecone schemas
        test_pinecone_schemas()
        
        # Test vectorization logic
        test_vectorization_logic()
        
        # Test vectorization agent
        test_vectorization_agent()
        
        # Test vectorization tasks
        test_vectorization_tasks()
        
        # Test sample vectorization
        test_sample_vectorization()
        
        print("\n" + "=" * 50)
        print("🎉 All vectorization module tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        logger.error(f"Test suite failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 