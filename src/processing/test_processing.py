"""
Test script for the processing module.

This script tests the structured processing functionality including:
- StructuredProcessingLogic class
- StructuredProcessingAgent class
- Schema definitions and validation
- Connection to remote Mistral model
"""

import sys
import os
import logging

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.processing import (
    StructuredProcessingLogic, 
    StructuredProcessingAgent, 
    StructuredProcessingTasks,
    SUPABASE_SCHEMAS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_schemas():
    """Test schema definitions and utilities."""
    print("\n=== Testing Schemas ===")
    
    # Test available schemas
    print(f"Available schemas: {len(SUPABASE_SCHEMAS)}")
    for schema_name in SUPABASE_SCHEMAS.keys():
        print(f"  - {schema_name}")
    
    # Test schema info
    financial_schema = SUPABASE_SCHEMAS.get("Resumen_Informe_Financiero", {})
    print(f"Financial schema fields: {len(financial_schema.get('fields', {}))}")
    print(f"Financial schema required fields: {len(financial_schema.get('required_fields', []))}")
    
    print("✅ Schemas test completed")

def test_processing_logic():
    """Test the StructuredProcessingLogic class."""
    print("\n=== Testing Processing Logic ===")
    
    try:
        # Create processing logic
        processing_logic = StructuredProcessingLogic()
        print("✅ StructuredProcessingLogic created successfully")
        
        # Test with sample content
        sample_content = """
        Financial Report Summary:
        Date: 2023-12-31
        Total Assets: 1,250,000.00
        Total Liabilities: 750,000.00
        Net Equity: 500,000.00
        Currency: USD
        Risk Rating: A
        """
        
        # Test financial report processing
        print("Testing financial report processing...")
        result = processing_logic.process_financial_reports(sample_content)
        
        if result:
            print(f"✅ Financial processing completed. Result type: {type(result)}")
            print(f"   Extracted fields: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
        else:
            print("⚠️  Financial processing returned None (expected if model not available)")
        
        # Test schema validation
        print("Testing schema validation...")
        test_data = {
            "fecha_corte_informe": "2023-12-31",
            "activos_totales": 1250000.00,
            "pasivos_totales": 750000.00,
            "patrimonio_neto": 500000.00
        }
        
        validation_result = processing_logic.validate_extracted_data(test_data, "Resumen_Informe_Financiero")
        print(f"✅ Validation completed. Valid: {validation_result['is_valid']}")
        
    except Exception as e:
        print(f"❌ Processing logic test failed: {e}")
        logger.error(f"Processing logic test failed: {e}")

def test_processing_agent():
    """Test the StructuredProcessingAgent class."""
    print("\n=== Testing Processing Agent ===")
    
    try:
        # Create processing agent
        processing_agent = StructuredProcessingAgent()
        print("✅ StructuredProcessingAgent created successfully")
        
        # Test connection to remote Mistral model
        print("Testing connection to remote Mistral model...")
        connection_result = processing_agent.test_connection()
        
        if connection_result['status'] == 'success':
            print(f"✅ Connection successful: {connection_result['message']}")
        else:
            print(f"⚠️  Connection failed: {connection_result['message']}")
            print("   This is expected if the remote model is not running")
        
        # Get the CrewAI agent
        agent = processing_agent.get_agent()
        print("✅ CrewAI agent retrieved successfully")
        
        # Test available schemas
        available_schemas = processing_agent.get_available_schemas()
        print(f"✅ Available schemas retrieved: {len(available_schemas)}")
        
    except Exception as e:
        print(f"❌ Processing agent test failed: {e}")
        logger.error(f"Processing agent test failed: {e}")

def test_processing_tasks():
    """Test the StructuredProcessingTasks class."""
    print("\n=== Testing Processing Tasks ===")
    
    try:
        # Create a mock agent for testing
        from crewai import Agent
        
        mock_agent = Agent(
            role='Test Agent',
            goal='Test processing tasks',
            backstory='A test agent for validating processing tasks',
            verbose=False
        )
        
        # Create processing tasks
        processing_tasks = StructuredProcessingTasks(mock_agent)
        print("✅ StructuredProcessingTasks created successfully")
        
        # Test creating tasks
        financial_task = processing_tasks.process_financial_reports()
        print("✅ Financial reports task created")
        
        movements_task = processing_tasks.process_daily_movements_json()
        print("✅ Daily movements task created")
        
        macroeconomic_task = processing_tasks.process_macroeconomic_data()
        print("✅ Macroeconomic data task created")
        
        contracts_task = processing_tasks.process_public_contracts()
        print("✅ Public contracts task created")
        
        validation_task = processing_tasks.validate_structured_data()
        print("✅ Data validation task created")
        
    except Exception as e:
        print(f"❌ Processing tasks test failed: {e}")
        logger.error(f"Processing tasks test failed: {e}")

def test_sample_extraction():
    """Test sample data extraction with different content types."""
    print("\n=== Testing Sample Extraction ===")
    
    try:
        processing_logic = StructuredProcessingLogic()
        
        # Test JSON content
        sample_json = {
            "fecha_operacion": "2023-12-15",
            "cantidad_operacion": 1000,
            "precio_operacion": 25.50,
            "monto_total": 25500.00,
            "tipo_operacion": "COMPRA"
        }
        
        print("Testing JSON content processing...")
        result = processing_logic.process_daily_movements_json(sample_json)
        
        if result:
            print(f"✅ JSON processing completed. Records: {len(result) if isinstance(result, list) else 1}")
        else:
            print("⚠️  JSON processing returned None (expected if model not available)")
        
        # Test text content
        sample_text = """
        Macroeconomic Indicators Report:
        Inflation Rate: 5.2%
        GDP Growth: 3.1%
        Unemployment Rate: 7.5%
        Date: 2023-12-31
        Source: Central Bank
        """
        
        print("Testing text content processing...")
        result = processing_logic.process_macroeconomic_data(sample_text)
        
        if result:
            print(f"✅ Text processing completed. Result type: {type(result)}")
        else:
            print("⚠️  Text processing returned None (expected if model not available)")
        
    except Exception as e:
        print(f"❌ Sample extraction test failed: {e}")
        logger.error(f"Sample extraction test failed: {e}")

def main():
    """Run all processing module tests."""
    print("🚀 Starting Processing Module Tests")
    print("=" * 50)
    
    try:
        # Test schemas
        test_schemas()
        
        # Test processing logic
        test_processing_logic()
        
        # Test processing agent
        test_processing_agent()
        
        # Test processing tasks
        test_processing_tasks()
        
        # Test sample extraction
        test_sample_extraction()
        
        print("\n" + "=" * 50)
        print("🎉 All processing module tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        logger.error(f"Test suite failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 