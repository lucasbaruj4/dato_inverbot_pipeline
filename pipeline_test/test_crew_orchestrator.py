#!/usr/bin/env python3
"""
Test Crew Orchestrator Script

Simple test to verify that the crew orchestrator can be imported and initialized.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_crew_orchestrator_import():
    """Test that the crew orchestrator can be imported."""
    try:
        from src.crew_orchestrator import CrewOrchestrator, create_pipeline_crew
        print("✅ Crew orchestrator imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import crew orchestrator: {e}")
        return False

def test_crew_orchestrator_creation():
    """Test that a crew orchestrator can be created."""
    try:
        from src.crew_orchestrator import create_pipeline_crew
        
        # Create orchestrator in simulation mode
        orchestrator = create_pipeline_crew(simulation_mode=True)
        print("✅ Crew orchestrator created successfully")
        
        # Test crew setup
        setup_result = orchestrator.test_crew_setup()
        print(f"✅ Crew setup test result: {setup_result['status']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create crew orchestrator: {e}")
        return False

def test_crew_info():
    """Test that crew information can be retrieved."""
    try:
        from src.crew_orchestrator import create_pipeline_crew
        
        orchestrator = create_pipeline_crew(simulation_mode=True)
        crew_info = orchestrator.get_crew_info()
        
        print("✅ Crew info retrieved successfully")
        print(f"   Agents: {list(crew_info['agents'].keys())}")
        print(f"   Tasks: {len(crew_info['tasks'])}")
        print(f"   Process type: {crew_info['process_type']}")
        print(f"   Simulation mode: {crew_info['simulation_mode']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to get crew info: {e}")
        return False

def main():
    """Run all crew orchestrator tests."""
    print("🧪 Testing Crew Orchestrator")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_crew_orchestrator_import),
        ("Creation Test", test_crew_orchestrator_creation),
        ("Info Test", test_crew_info)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All crew orchestrator tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main() 