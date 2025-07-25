# Pipeline Testing Framework

## 🎯 Testing Strategy

This testing framework validates the Inverbot Data Pipeline using a **safe, incremental approach**:

### 📋 Testing Phases

1. **🛡️ Synthetic Data Testing** - Test with fake data, no database writes
2. **🔍 Agent-by-Agent Testing** - Test each CrewAI agent individually  
3. **🚀 Crew End-to-End Testing** - Test complete crew execution
4. **📊 Output Validation** - Validate data structure before database writes
5. **🌐 Real Data Testing** - Test with real data sources (future phase)
6. **💾 Database Integration** - Test actual database writes (future phase)

## 🚀 Quick Start

```bash
# Navigate to testing directory
cd pipeline_test

# Run complete pipeline testing
python test_output.py

# Validate the results
python validate_test_output.py
```

## 📁 Test Files

- **`test_output.py`** - Main testing script (agent-by-agent + crew end-to-end)
- **`validate_test_output.py`** - Validation script for test outputs
- **`test_outputs/`** - Directory containing test results (auto-created)

## 🔧 Testing Components

### 🤖 Agent-by-Agent Testing

Tests each CrewAI agent individually:

1. **ExtractionAgent** - Tests data extraction from synthetic sources
2. **StructuredProcessingAgent** - Tests structured data processing
3. **VectorizationAgent** - Tests text chunking and embedding
4. **LoadingAgent** - Tests loading simulation (no actual DB writes)

### 🚀 Crew End-to-End Testing

Tests complete crew execution with sequential process:

1. **Extract** → **Process** → **Vectorize** → **Load** (simulation)
2. Validates data flow between agents
3. Tests CrewAI orchestration

### 🛡️ Safety Features

- **Synthetic Data Only** - No real web scraping or API calls
- **No Database Writes** - All loading operations are simulated
- **Output Capture** - All results saved to JSON for inspection
- **Error Handling** - Comprehensive error reporting and logging

## 📊 Test Output Structure

### Agent-by-Agent Results

```json
{
  "test_type": "agent_by_agent",
  "timestamp": "2024-12-19T16:30:00",
  "agents": {
    "extraction": {
      "status": "success",
      "agent": "ExtractionAgent",
      "input": [...],
      "output": [...],
      "timestamp": "2024-12-19T16:30:01"
    },
    "processing": { ... },
    "vectorization": { ... },
    "loading": { ... }
  },
  "summary": {
    "total_agents": 4,
    "successful": 4,
    "failed": 0,
    "success_rate": "100.0%"
  }
}
```

### Crew End-to-End Results

```json
{
  "status": "success",
  "test_type": "crew_end_to_end",
  "input": [...],
  "output": [...],
  "timestamp": "2024-12-19T16:30:05"
}
```

### Complete Pipeline Results

```json
{
  "test_session": {
    "timestamp": "2024-12-19T16:30:00",
    "test_type": "full_pipeline",
    "output_files": {
      "agent_by_agent": "test_outputs/test_agent_by_agent_20241219_163000.json",
      "crew_end_to_end": "test_outputs/test_crew_end_to_end_20241219_163005.json"
    }
  },
  "agent_by_agent": { ... },
  "crew_end_to_end": { ... },
  "summary": {
    "agent_success_rate": "100.0%",
    "crew_success": true,
    "overall_status": "success"
  }
}
```

## 🔍 Validation

The validation script checks:

- **Required Fields** - All expected fields are present
- **Data Types** - Fields have correct data types
- **Status Values** - Status fields contain valid values
- **Timestamp Format** - ISO format timestamps
- **Agent Names** - Valid agent names
- **Summary Consistency** - Counts add up correctly

## 🎯 Expected Test Flow

### Phase 1: Synthetic Data Testing ✅

```bash
# Run tests with synthetic data
python test_output.py

# Expected output:
# 🤖 Agent-by-Agent Testing:
#    ✅ Successful: 4/4
#    ❌ Failed: 0
#    📈 Success Rate: 100.0%
#
# 🚀 Crew End-to-End Testing:
#    ✅ Success
#
# 🎯 Overall Pipeline Status:
#    ✅ FULL SUCCESS
```

### Phase 2: Real Data Testing (Future)

```bash
# TODO: Test with real data sources
# - Small, controlled real data
# - Validate output structure
# - Ensure no database pollution
```

### Phase 3: Database Integration (Future)

```bash
# TODO: Test actual database writes
# - Small test datasets
# - Database cleanup utilities
# - Transaction rollback testing
```

## 🛠️ Troubleshooting

### Common Issues

1. **LLM Connection Errors**
   - Check `.env.local` configuration
   - Verify Mistral model URL is accessible
   - Ensure localtunnel is running

2. **Agent Initialization Failures**
   - Check import paths
   - Verify environment variables
   - Review agent configuration

3. **Crew Execution Errors**
   - Check task dependencies
   - Verify agent tool assignments
   - Review CrewAI configuration

### Debug Mode

```bash
# Run with verbose logging
python test_output.py 2>&1 | tee test_debug.log

# Check specific agent
python -c "
from src.extraction.extraction_agent import ExtractionAgent
agent = ExtractionAgent()
print('Agent created successfully')
"
```

## 📈 Success Criteria

### ✅ Agent-by-Agent Testing
- All 4 agents initialize successfully
- Each agent processes synthetic data correctly
- No exceptions or errors during execution
- Output data structure matches expectations

### ✅ Crew End-to-End Testing
- Crew executes without errors
- Data flows correctly between agents
- Final output is properly structured
- No database writes occur (simulation only)

### ✅ Overall Pipeline
- 100% agent success rate
- Crew execution successful
- All output files generated
- Validation passes without errors

## 🔄 Next Steps

After successful synthetic data testing:

1. **Real Data Testing** - Test with small, controlled real data sources
2. **Database Integration** - Test actual database writes with cleanup
3. **Performance Testing** - Measure execution times and resource usage
4. **Error Recovery** - Test error handling and recovery mechanisms
5. **CI/CD Integration** - Automate testing in deployment pipeline

## 📝 Notes

- **No Database Writes**: All testing is done without writing to actual databases
- **Synthetic Data**: Uses fake data to avoid external dependencies
- **Safe Testing**: Designed to be run repeatedly without side effects
- **Comprehensive Logging**: Detailed logs for debugging and analysis
- **Modular Design**: Each test component can be run independently 