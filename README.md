# Inverbot Data Pipeline

A comprehensive data pipeline for extracting, processing, vectorizing, and loading financial and economic data from various Paraguayan institutions using **Google AI models** and **CrewAI** multi-agent orchestration.

## 🎯 Overview

This pipeline automates the collection and processing of data from multiple sources including BVA (Bolsa de Valores y Productos de Asunción), government institutions, and financial reports. The system uses **Google's Gemini models** for intelligent data processing and **Google embeddings** for semantic search capabilities.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EXTRACTION    │───▶│   PROCESSING    │───▶│ VECTORIZATION   │───▶│    LOADING      │
│                 │    │                 │    │                 │    │                 │
│ • Web Scraping  │    │ • Data Cleaning │    │ • Text Chunking │    │ • Supabase      │
│ • API Calls     │    │ • Validation    │    │ • Google Embeds │    │ • Pinecone      │
│ • File Downloads│    │ • Schema Mapping│    │ • Metadata Prep │    │ • Batch Loading │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                        ▲                        ▲                        ▲
         │                        │                        │                        │
    ┌────▼────┐              ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
    │Extraction│              │Processing│              │Vector   │              │Loading  │
    │  Agent   │              │  Agent   │              │ Agent   │              │ Agent   │
    └─────────┘              └─────────┘              └─────────┘              └─────────┘
                                    │
                           ┌────────▼────────┐
                           │ CrewAI Crew     │
                           │ Orchestrator    │
                           │ (Google Gemini) │
                           └─────────────────┘
```

### Module Structure
```
src/
├── crew_orchestrator.py     # CrewAI Crew Management
├── extraction/              # Data extraction from web sources
├── processing/              # Structured data processing
├── vectorization/           # Text chunking & Google embeddings
├── loading/                 # Database operations (Supabase + Pinecone)
└── utils/                   # Configuration & logging
```

## 🚀 Features

- **🤖 AI-Powered**: Google Gemini 2.5 Flash-Lite for cost-efficient processing
- **🔍 Semantic Search**: Google embeddings for vector similarity search
- **⚡ Multi-Agent**: CrewAI orchestration with specialized agents
- **💰 Cost-Optimized**: Context-efficient processing with minimal token usage
- **🛡️ Safe Testing**: Simulation mode for database-free validation
- **📊 Comprehensive**: Handles JSON, HTML, PDF, Excel data sources
- **✅ Production Ready**: 100% test success rate, clean architecture

## 🛠️ Setup

### 1. Prerequisites
- Python 3.8+
- Google AI API access
- Supabase account
- Pinecone account

### 2. Installation
```bash
git clone <repository-url>
cd Inverbot_Data_Pipeline
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env.local` file:
```env
# Google AI
GOOGLE_API_KEY=your_google_api_key_here

# Databases
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-east-1
```

### 4. Test Configuration
```bash
# Test all connections
python connection_test/run_tests.py

# Test with synthetic data (safe mode)
cd pipeline_test
python test_output.py
```

### 5. Run Pipeline
```bash
# Run complete pipeline with simulation mode
python run_pipeline.py --simulation

# Run with real data (after testing)
python run_pipeline.py
```

## 📊 Data Sources

| Source | Category | Content Types | Processing |
|--------|----------|---------------|------------|
| BVA Emisores | Company Balances | EXCEL, PDF, TEXT | Structured + Vectorized |
| BVA Informes Diarios | Daily Movements | JSON | Structured Only |
| BVA Informes Mensuales | Monthly Volume | TEXT, PDF, JSON | Structured + Vectorized |
| BVA Informes Anuales | Annual Reports | TEXT, PDF | Structured + Vectorized |
| BCP, MIC, MEF | Macroeconomic Context | TEXT, PDF, EXCEL, PPT | Structured + Vectorized |
| DGEEC/INE | Social Statistics | PDF, EXCEL, PPT, TEXT | Structured + Vectorized |
| DNCP | Public Contracts | TEXT | Structured + Vectorized |
| DNIT | Investment Data | TEXT, PNG, PDF | Structured + Vectorized |

## 🗄️ Database Schema

### Supabase (PostgreSQL)
- **Lookup Tables**: `Categoria_Emisor`, `Emisores`, `Moneda`, `Frecuencia`, etc.
- **Data Tables**: `Informe_General`, `Resumen_Informe_Financiero`, `Dato_Macroeconomico`, etc.
- **Transaction Tables**: `Movimiento_Diario_Bolsa`, `Licitacion_Contrato`

### Pinecone (Vector Database)
- **Indexes**: 4 separate indexes for different content types
- **Dimensions**: Variable (Google embeddings - typically 768 or 1536)
- **Metric**: Cosine similarity
- **Collections**: documentos-informes, noticia-relevante, dato-macroeconomico, licitacion-contrato

## 🤖 AI Models

### Google Gemini 2.5 Flash-Lite
- **Purpose**: LLM for data processing and agent orchestration
- **Cost**: $0.10/1M input tokens, $0.40/1M output tokens
- **Free Tier**: Available for development/testing
- **Context**: Up to 1M tokens

### Google Text Embedding (text-embedding-004)
- **Purpose**: Semantic embeddings for vector search
- **Cost**: $0.15/1M tokens
- **Free Tier**: Available for development/testing
- **Dimensions**: Dynamic (typically 768 or 1536)

## 🧪 Testing Framework

Located in `pipeline_test/`:

### Agent-by-Agent Testing
```bash
cd pipeline_test
python test_output.py --agent-tests
```

### Crew End-to-End Testing
```bash
cd pipeline_test
python test_output.py --crew-tests
```

### Validation
```bash
cd pipeline_test
python validate_test_output.py
```

**Testing Strategy:**
1. **Synthetic Data** → Test with fake data (no database writes)
2. **Real Data Testing** → Test with actual sources (simulation mode)
3. **Database Integration** → Full pipeline with actual writes

## 💡 Usage Examples

### Basic Pipeline Execution
```python
from src.crew_orchestrator import execute_pipeline_with_sources

# Define data sources
sources = [
    {
        "category": "BVA_EMISORES",
        "url": "https://example.com/data",
        "content_type": "JSON"
    }
]

# Execute with simulation mode
result = execute_pipeline_with_sources(sources, simulation_mode=True)
```

### Individual Agent Usage
```python
from src.extraction.extraction_agent import ExtractionAgent

# Create agent
agent = ExtractionAgent()

# Get CrewAI agent for task assignment
crew_agent = agent.get_agent()
```

## 🚀 Production Deployment

1. **Scale Configuration**: Update token limits in `src/utils/config.py`
2. **Database Setup**: Ensure Supabase tables and Pinecone indexes exist
3. **Monitoring**: Enable metrics collection
4. **Scheduling**: Set up cron jobs or task schedulers
5. **Error Handling**: Configure alerting for failed runs

## 📈 Cost Optimization

- **Free Tier**: Use Google AI free tier for development
- **Context Limits**: Small chunks (300 tokens) for cost control
- **Batch Processing**: Process 1-2 items at a time during testing
- **Conservative Rate Limits**: 20 requests/minute for cost control

## 🔧 Configuration

Key settings in `src/utils/config.py`:
- `max_input_tokens`: 500 (context-efficient)
- `max_output_tokens`: 300 (cost control)
- `chunk_size`: 300 (small embeddings)
- `batch_size`: 2 (testing-friendly)

## 📝 Contributing

1. Follow the modular architecture
2. Update tests when adding features
3. Use simulation mode for development
4. Maintain cost efficiency
5. Document all changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the testing framework output
2. Verify configuration with `connection_test/run_tests.py`
3. Review logs in the console output
4. Ensure API keys are correctly configured

---

**Note**: This pipeline is optimized for cost-efficient development and testing using Google AI's free tier, with easy scaling to production when ready. 