#!/usr/bin/env python3
"""
Test Output Script - Agent-by-Agent and Crew End-to-End Testing

This script tests the pipeline using CrewAI agents and crews without committing to databases.
It uses synthetic test data to validate the complete pipeline flow.

Testing Strategy:
1. Agent-by-Agent Testing: Test each agent individually
2. Crew End-to-End Testing: Test complete crew execution
3. Synthetic Data Only: No real database writes
4. Output Capture: Save all outputs to JSON for inspection
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.extraction.extraction_agent import ExtractionAgent
from src.processing.processing_agent import StructuredProcessingAgent
from src.vectorization.vectorization_agent import VectorizationAgent
from src.loading.loading_agent import LoadingAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)

class TestOutputCapture:
    """Captures and saves test outputs to JSON files for inspection."""
    
    def __init__(self):
        self.output_dir = Path("test_outputs")
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def save_output(self, stage: str, data: Any, test_type: str = "agent"):
        """Save test output to JSON file."""
        filename = f"{test_type}_{stage}_{self.timestamp}.json"
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Saved {test_type} test output to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving test output: {e}")
            return None

def get_synthetic_test_data() -> List[Dict[str, Any]]:
    """Generate synthetic test data for safe testing."""
    return [
        {
            "category": "Synthetic Financial Report",
            "url": "https://example.com/synthetic-financial.pdf",
            "content_type": ["TEXT"],
            "description": "Synthetic financial data for testing"
        },
        {
            "category": "Synthetic Daily Movements", 
            "url": "https://example.com/synthetic-movements.json",
            "content_type": ["JSON"],
            "description": "Synthetic daily movements data for testing"
        },
        {
            "category": "Synthetic Macroeconomic Data",
            "url": "https://example.com/synthetic-macro.txt", 
            "content_type": ["TEXT"],
            "description": "Synthetic macroeconomic data for testing"
        }
    ]

def get_synthetic_content_for_testing() -> Dict[str, Any]:
    """Generate synthetic content that agents can process."""
    return {
        "financial_report": {
            "content": """
            Financial Report - Synthetic Test Data
            Company: TestCorp Inc.
            Date: 2024-12-19
            Total Assets: $1,000,000
            Total Liabilities: $400,000
            Net Income: $150,000
            Currency: USD
            """,
            "schema": "Resumen_Informe_Financiero"
        },
        "daily_movements": {
            "content": {
                "fecha_operacion": "2024-12-19",
                "cantidad_operacion": 1000,
                "precio_operacion": 25.50,
                "id_instrumento": "TEST001",
                "id_emisor": "TESTCORP"
            },
            "schema": "Movimiento_Diario_Bolsa"
        },
        "macroeconomic_data": {
            "content": """
            Macroeconomic Indicators - Synthetic Data
            GDP Growth Rate: 3.2%
            Inflation Rate: 2.1%
            Unemployment Rate: 4.5%
            Date: 2024-12-19
            Source: Test Central Bank
            """,
            "schema": "Dato_Macroeconomico"
        }
    }

def test_extraction_agent() -> Dict[str, Any]:
    """Test the ExtractionAgent individually."""
    logger.info("Testing ExtractionAgent...")
    
    try:
        # Initialize agent
        extraction_agent = ExtractionAgent()
        agent = extraction_agent.get_agent()
        
        # Test data
        test_sources = get_synthetic_test_data()
        
        # Test agent execution
        result = agent.invoke({
            "sources_list": test_sources
        })
        
        logger.info("✅ ExtractionAgent test completed successfully")
        return {
            "status": "success",
            "agent": "ExtractionAgent",
            "input": test_sources,
            "output": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ ExtractionAgent test failed: {e}")
        return {
            "status": "error",
            "agent": "ExtractionAgent", 
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def test_processing_agent() -> Dict[str, Any]:
    """Test the StructuredProcessingAgent individually."""
    logger.info("Testing StructuredProcessingAgent...")
    
    try:
        # Initialize agent
        processing_agent = StructuredProcessingAgent()
        agent = processing_agent.get_agent()
        
        # Test data
        synthetic_content = get_synthetic_content_for_testing()
        
        results = {}
        for content_type, data in synthetic_content.items():
            try:
                result = agent.invoke({
                    "content": data["content"],
                    "schema_name": data["schema"]
                })
                results[content_type] = {
                    "status": "success",
                    "output": result
                }
            except Exception as e:
                results[content_type] = {
                    "status": "error", 
                    "error": str(e)
                }
        
        logger.info("✅ StructuredProcessingAgent test completed")
        return {
            "status": "success",
            "agent": "StructuredProcessingAgent",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ StructuredProcessingAgent test failed: {e}")
        return {
            "status": "error",
            "agent": "StructuredProcessingAgent",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def test_vectorization_agent() -> Dict[str, Any]:
    """Test the VectorizationAgent individually."""
    logger.info("Testing VectorizationAgent...")
    
    try:
        # Initialize agent
        vectorization_agent = VectorizationAgent()
        agent = vectorization_agent.get_agent()
        
        # Test data
        test_content = "This is synthetic test content for vectorization. It contains multiple sentences that should be chunked and embedded for testing purposes."
        
        # Test agent execution
        result = agent.invoke({
            "content": test_content
        })
        
        logger.info("✅ VectorizationAgent test completed successfully")
        return {
            "status": "success",
            "agent": "VectorizationAgent",
            "input": test_content,
            "output": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ VectorizationAgent test failed: {e}")
        return {
            "status": "error",
            "agent": "VectorizationAgent",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def test_loading_agent() -> Dict[str, Any]:
    """Test the LoadingAgent individually (without database writes)."""
    logger.info("Testing LoadingAgent (simulation mode)...")
    
    try:
        # Initialize agent
        loading_agent = LoadingAgent()
        agent = loading_agent.get_agent()
        
        # Test data (simulated structured data)
        test_structured_data = {
            "table_name": "Resumen_Informe_Financiero",
            "data": {
                "fecha_corte_informe": "2024-12-19",
                "activos_totales": 1000000.00,
                "moneda_informe": 1
            }
        }
        
        # Test agent execution (should simulate loading without actual DB writes)
        result = agent.invoke({
            "data": test_structured_data["data"],
            "table_name": test_structured_data["table_name"],
            "simulation_mode": True  # Flag to prevent actual DB writes
        })
        
        logger.info("✅ LoadingAgent test completed successfully (simulation)")
        return {
            "status": "success",
            "agent": "LoadingAgent",
            "input": test_structured_data,
            "output": result,
            "simulation_mode": True,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ LoadingAgent test failed: {e}")
        return {
            "status": "error",
            "agent": "LoadingAgent",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def test_crew_end_to_end() -> Dict[str, Any]:
    """Test complete crew execution end-to-end."""
    logger.info("Testing Crew End-to-End Execution...")
    
    try:
        from src.crew_orchestrator import create_pipeline_crew
        
        # Create crew orchestrator in simulation mode
        orchestrator = create_pipeline_crew(simulation_mode=True)
        
        # Test crew setup first
        setup_test = orchestrator.test_crew_setup()
        if setup_test['status'] != 'success':
            logger.error(f"Crew setup test failed: {setup_test}")
            return {
                "status": "error",
                "test_type": "crew_end_to_end",
                "error": f"Crew setup failed: {setup_test}",
                "timestamp": datetime.now().isoformat()
            }
        
        # Test data
        test_sources = get_synthetic_test_data()
        
        # Execute pipeline
        result = orchestrator.execute_pipeline(test_sources)
        
        logger.info("✅ Crew End-to-End test completed successfully")
        return {
            "status": "success",
            "test_type": "crew_end_to_end",
            "input": test_sources,
            "output": result,
            "crew_info": orchestrator.get_crew_info(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Crew End-to-End test failed: {e}")
        return {
            "status": "error",
            "test_type": "crew_end_to_end",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def test_agent_by_agent() -> Dict[str, Any]:
    """Run all agent-by-agent tests."""
    logger.info("Starting Agent-by-Agent Testing...")
    
    results = {
        "test_type": "agent_by_agent",
        "timestamp": datetime.now().isoformat(),
        "agents": {}
    }
    
    # Test each agent individually
    agents_to_test = [
        ("extraction", test_extraction_agent),
        ("processing", test_processing_agent),
        ("vectorization", test_vectorization_agent),
        ("loading", test_loading_agent)
    ]
    
    for agent_name, test_function in agents_to_test:
        logger.info(f"Testing {agent_name} agent...")
        results["agents"][agent_name] = test_function()
    
    # Count successes and failures
    successes = sum(1 for result in results["agents"].values() if result.get("status") == "success")
    failures = len(results["agents"]) - successes
    
    results["summary"] = {
        "total_agents": len(results["agents"]),
        "successful": successes,
        "failed": failures,
        "success_rate": f"{(successes/len(results['agents'])*100):.1f}%"
    }
    
    logger.info(f"Agent-by-Agent Testing Complete: {successes}/{len(results['agents'])} agents successful")
    return results

def test_full_pipeline() -> Dict[str, Any]:
    """Run complete pipeline testing (agent-by-agent + crew end-to-end)."""
    logger.info("Starting Full Pipeline Testing...")
    
    output_capture = TestOutputCapture()
    
    # Run agent-by-agent tests
    agent_results = test_agent_by_agent()
    agent_output_path = output_capture.save_output("agent_by_agent", agent_results, "test")
    
    # Run crew end-to-end test
    crew_results = test_crew_end_to_end()
    crew_output_path = output_capture.save_output("crew_end_to_end", crew_results, "test")
    
    # Compile final results
    final_results = {
        "test_session": {
            "timestamp": datetime.now().isoformat(),
            "test_type": "full_pipeline",
            "output_files": {
                "agent_by_agent": agent_output_path,
                "crew_end_to_end": crew_output_path
            }
        },
        "agent_by_agent": agent_results,
        "crew_end_to_end": crew_results,
        "summary": {
            "agent_success_rate": agent_results.get("summary", {}).get("success_rate", "0%"),
            "crew_success": crew_results.get("status") == "success",
            "overall_status": "success" if (
                agent_results.get("summary", {}).get("successful", 0) == 4 and 
                crew_results.get("status") == "success"
            ) else "partial_success"
        }
    }
    
    # Save complete results
    complete_output_path = output_capture.save_output("complete_pipeline", final_results, "test")
    
    logger.info(f"Full Pipeline Testing Complete. Results saved to: {complete_output_path}")
    return final_results

def main():
    """Main test execution function."""
    logger.info("🚀 Starting Pipeline Testing with Synthetic Data")
    logger.info("📋 Testing Strategy: Agent-by-Agent + Crew End-to-End")
    logger.info("🛡️ Safety: No database writes, synthetic data only")
    
    try:
        # Run full pipeline testing
        results = test_full_pipeline()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 PIPELINE TESTING RESULTS")
        print("="*60)
        
        # Agent-by-Agent Results
        agent_summary = results["agent_by_agent"]["summary"]
        print(f"\n🤖 Agent-by-Agent Testing:")
        print(f"   ✅ Successful: {agent_summary['successful']}/{agent_summary['total_agents']}")
        print(f"   ❌ Failed: {agent_summary['failed']}")
        print(f"   📈 Success Rate: {agent_summary['success_rate']}")
        
        # Crew End-to-End Results
        crew_success = results["crew_end_to_end"]["status"] == "success"
        print(f"\n🚀 Crew End-to-End Testing:")
        print(f"   {'✅ Success' if crew_success else '❌ Failed'}")
        
        # Overall Status
        overall_status = results["summary"]["overall_status"]
        print(f"\n🎯 Overall Pipeline Status:")
        print(f"   {'✅ FULL SUCCESS' if overall_status == 'success' else '⚠️ PARTIAL SUCCESS' if overall_status == 'partial_success' else '❌ FAILED'}")
        
        # Output Files
        print(f"\n📁 Test Output Files:")
        for test_type, filepath in results["test_session"]["output_files"].items():
            if filepath:
                print(f"   {test_type}: {filepath}")
        
        print("\n" + "="*60)
        
        if overall_status == "success":
            logger.info("🎉 All tests passed! Pipeline is ready for real data testing.")
        else:
            logger.warning("⚠️ Some tests failed. Check output files for details.")
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        print(f"\n❌ Test execution failed: {e}")

if __name__ == "__main__":
    main() 