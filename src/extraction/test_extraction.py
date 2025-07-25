"""
Test script for the extraction module.

This script tests the extraction functionality including:
- ExtractionLogic class
- ExtractionAgent class
- Data sources configuration
- Connection to remote Mistral model
"""

import sys
import os
import logging

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.extraction import (
    ExtractionLogic, 
    ExtractionAgent, 
    ExtractionTasks,
    TEST_DATA_SOURCES,
    get_data_sources
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_data_sources():
    """Test data sources configuration."""
    print("\n=== Testing Data Sources ===")
    
    # Test getting main data sources
    main_sources = get_data_sources("main")
    print(f"Main data sources: {len(main_sources)}")
    
    # Test getting test data sources
    test_sources = get_data_sources("test")
    print(f"Test data sources: {len(test_sources)}")
    
    # Test filtering by category
    financial_sources = [s for s in main_sources if "Financiero" in s["category"]]
    print(f"Financial sources: {len(financial_sources)}")
    
    # Test filtering by content type
    json_sources = [s for s in main_sources if "JSON" in s["content_type"]]
    print(f"JSON sources: {len(json_sources)}")
    
    print("✅ Data sources test completed")

def test_extraction_logic():
    """Test the ExtractionLogic class."""
    print("\n=== Testing Extraction Logic ===")
    
    try:
        # Create extraction logic with test sources
        extraction_logic = ExtractionLogic(TEST_DATA_SOURCES)
        print("✅ ExtractionLogic created successfully")
        
        # Test extraction (this will actually try to download/scrape)
        print("Running extraction (this may take a moment)...")
        extracted_data = extraction_logic.run_extraction()
        
        print(f"✅ Extraction completed. Extracted {len(extracted_data)} items")
        
        # Print summary of extracted data
        for item in extracted_data:
            print(f"  - {item['source_category']}: {item['content_type']} from {item['source_url']}")
            
    except Exception as e:
        print(f"❌ Extraction logic test failed: {e}")
        logger.error(f"Extraction logic test failed: {e}")

def test_extraction_agent():
    """Test the ExtractionAgent class."""
    print("\n=== Testing Extraction Agent ===")
    
    try:
        # Create extraction agent
        extraction_agent = ExtractionAgent()
        print("✅ ExtractionAgent created successfully")
        
        # Test connection to remote Mistral model
        print("Testing connection to remote Mistral model...")
        connection_result = extraction_agent.test_connection()
        
        if connection_result['status'] == 'success':
            print(f"✅ Connection successful: {connection_result['message']}")
        else:
            print(f"⚠️  Connection failed: {connection_result['message']}")
            print("   This is expected if the remote model is not running")
        
        # Get the CrewAI agent
        agent = extraction_agent.get_agent()
        print("✅ CrewAI agent retrieved successfully")
        
    except Exception as e:
        print(f"❌ Extraction agent test failed: {e}")
        logger.error(f"Extraction agent test failed: {e}")

def test_extraction_tasks():
    """Test the ExtractionTasks class."""
    print("\n=== Testing Extraction Tasks ===")
    
    try:
        # Create a mock agent for testing
        from crewai import Agent
        
        mock_agent = Agent(
            role='Test Agent',
            goal='Test extraction tasks',
            backstory='A test agent for validating extraction tasks',
            verbose=False
        )
        
        # Create extraction tasks
        extraction_tasks = ExtractionTasks(mock_agent)
        print("✅ ExtractionTasks created successfully")
        
        # Test creating tasks
        download_task = extraction_tasks.download_and_scrape_content()
        print("✅ Download and scrape task created")
        
        validation_task = extraction_tasks.validate_extraction_results()
        print("✅ Validation task created")
        
        specific_task = extraction_tasks.extract_specific_content_type("PDF")
        print("✅ Specific content type task created")
        
    except Exception as e:
        print(f"❌ Extraction tasks test failed: {e}")
        logger.error(f"Extraction tasks test failed: {e}")

def main():
    """Run all extraction module tests."""
    print("🚀 Starting Extraction Module Tests")
    print("=" * 50)
    
    try:
        # Test data sources
        test_data_sources()
        
        # Test extraction logic
        test_extraction_logic()
        
        # Test extraction agent
        test_extraction_agent()
        
        # Test extraction tasks
        test_extraction_tasks()
        
        print("\n" + "=" * 50)
        print("🎉 All extraction module tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        logger.error(f"Test suite failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 