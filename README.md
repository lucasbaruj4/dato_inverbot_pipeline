# Inverbot Data Pipeline

A modular, production-ready data pipeline for collecting and processing Paraguayan financial/economic data to support the Inverbot RAG system for investment advice.

## 🎯 Project Overview

The Inverbot Data Pipeline is a sophisticated multi-agent AI system that automates the collection, processing, and storage of financial and economic data from various Paraguayan sources. The processed data is stored in both structured (PostgreSQL/Supabase) and vector (Pinecone) databases to support the Inverbot RAG system.

## 🏗️ Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Local Pipeline │    │   Databases     │
│                 │    │                 │    │                 │
│ • BVA (Bolsa)   │───▶│ • Extraction    │───▶│ • Supabase      │
│ • BCP (Central) │    │ • Processing    │    │   (Structured)  │
│ • INE/DGEEC     │    │ • Vectorization │    │                 │
│ • DNCP          │    │ • Loading       │    │ • Pinecone      │
│ • DNIT          │    │ • Orchestration │    │   (Vector)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Colab Models   │
                       │                 │
                       │ • Mistral-7B    │
                       │ • Embeddings    │
                       │ • Localtunnel   │
                       └─────────────────┘
```

### Module Structure
```
src/
├── extraction/          # Data extraction from various sources
├── processing/          # Structured data processing
├── vectorization/       # Text chunking and embedding generation
├── loading/            # Database operations (Supabase + Pinecone)
├── orchestration/      # CrewAI agent coordination
└── utils/              # Common utilities and configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Access to Google Colab (for model deployment)
- Supabase account and project
- Pinecone account and API key

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Inverbot_Data_Pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
```env
# Database Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_API_KEY=your_supabase_anon_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1

# Model Configuration (set after Colab deployment)
MISTRAL_MODEL_URL=https://your-mistral-subdomain.loca.lt
EMBEDDING_MODEL_URL=https://your-embedding-subdomain.loca.lt
```

### 3. Deploy Models on Colab

#### Mistral Model Deployment
1. Open `notebooks/01_mistral_model_deployment.ipynb` in Google Colab
2. Run all cells
3. Copy the localtunnel URL to your `.env` file as `MISTRAL_MODEL_URL`

#### Embedding Model Deployment
1. Open `notebooks/02_embedding_model_deployment.ipynb` in Google Colab
2. Run all cells
3. Copy the localtunnel URL to your `.env` file as `EMBEDDING_MODEL_URL`

### 4. Test Configuration
```bash
# Test configuration
python -c "from src.utils.config import validate_config; print('Config valid:', validate_config())"

# Test database connections
python scripts/test_connections.py
```

### 5. Run Pipeline
```bash
# Run complete pipeline
python main.py

# Run specific modules
python -m src.extraction
python -m src.processing
python -m src.vectorization
python -m src.loading
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
- **Dimensions**: 384 (sentence-transformers/all-MiniLM-L6-v2)
- **Metric**: Cosine similarity
- **Collections**: documentos-informes, noticia-relevante, dato-macroeconomico, licitacion-contrato

## 🤖 AI Models

### Mistral-7B-Instruct-v0.3
- **Purpose**: Structured data extraction and processing
- **Deployment**: Google Colab with localtunnel
- **Integration**: CrewAI-compatible HTTP API
- **Use Cases**: Financial data parsing, report analysis

### Sentence Transformers (all-MiniLM-L6-v2)
- **Purpose**: Text embedding generation
- **Deployment**: Google Colab with localtunnel
- **Dimensions**: 384
- **Use Cases**: Document vectorization, semantic search

## 🔧 Development

### Project Structure
```
Inverbot_Data_Pipeline/
├── src/                    # Source code
│   ├── extraction/         # Data extraction modules
│   ├── processing/         # Data processing modules
│   ├── vectorization/      # Vector processing modules
│   ├── loading/           # Database loading modules
│   ├── orchestration/     # CrewAI orchestration
│   └── utils/             # Common utilities
├── tests/                 # Test suite
├── config/                # Configuration files
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── notebooks/             # Colab deployment notebooks
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── .gitignore           # Git ignore rules
```

### Code Quality
```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
mypy src/

# Run tests
pytest tests/ -v --cov=src
```

### Adding New Data Sources
1. Define source in `src/extraction/sources.py`
2. Implement extraction logic in `src/extraction/extractors/`
3. Add processing logic in `src/processing/`
4. Update database schemas if needed
5. Add tests in `tests/`

## 🧪 Testing

### Test Structure
```
tests/
├── unit/                  # Unit tests
├── integration/           # Integration tests
├── fixtures/              # Test data
└── conftest.py           # Test configuration
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

## 📈 Monitoring and Logging

### Logging
- **Structured Logging**: JSON format in production, rich console in development
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Files**: Rotated daily, compressed after 7 days

### Metrics
- **Pipeline Performance**: Processing time, success rates
- **Model Performance**: Response times, error rates
- **Database Performance**: Query times, connection health
- **Resource Usage**: Memory, CPU, network

## 🔒 Security

### Data Protection
- **Environment Variables**: All secrets stored in `.env` (not committed)
- **API Security**: Rate limiting, input validation
- **Database Security**: Connection encryption, access control
- **Model Security**: Secure API endpoints, authentication

### Best Practices
- Never commit `.env` files
- Use strong, unique API keys
- Regularly rotate credentials
- Monitor for suspicious activity

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**: Configure production environment variables
2. **Model Deployment**: Deploy models on production Colab instances
3. **Database Setup**: Configure production databases
4. **Monitoring**: Set up logging and monitoring
5. **CI/CD**: Configure automated testing and deployment

### Docker Deployment
```bash
# Build image
docker build -t inverbot-pipeline .

# Run container
docker run -d --name inverbot-pipeline \
  --env-file .env \
  inverbot-pipeline
```

## 🤝 Contributing

### Development Workflow
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes following coding standards
3. Add tests for new functionality
4. Run tests and linting: `make test`
5. Submit pull request with detailed description

### Code Standards
- Follow PEP 8 style guide
- Use type hints for all functions
- Write comprehensive docstrings
- Maintain 80%+ test coverage
- Use conventional commit messages

## 📚 Documentation

### Documentation
- **API Documentation**: Available in each module's docstrings
- **Database Schema**: Documented in `docs/database_schema.md`
- **Deployment Guide**: Available in `docs/deployment.md`

### API Documentation
- **Extraction API**: Documented in `src/extraction/`
- **Processing API**: Documented in `src/processing/`
- **Vectorization API**: Documented in `src/vectorization/`
- **Loading API**: Documented in `src/loading/`
- **Orchestration API**: Documented in `src/orchestration/`

## 🆘 Troubleshooting

### Common Issues

#### Model Connection Issues
```bash
# Test model connectivity
curl -X GET https://your-model-subdomain.loca.lt/health \
  -H 'bypass-tunnel-reminder: true'
```

#### Database Connection Issues
```bash
# Test Supabase connection
python scripts/test_supabase.py

# Test Pinecone connection
python scripts/test_pinecone.py
```

#### Pipeline Errors
```bash
# Check logs
tail -f logs/pipeline.log

# Validate configuration
python -c "from src.utils.config import validate_config; validate_config()"
```

### Getting Help
1. Check the [troubleshooting guide](docs/troubleshooting.md)
2. Check [open issues](https://github.com/your-repo/issues)
3. Create new issue with detailed error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent orchestration framework
- **Supabase**: Database and authentication services
- **Pinecone**: Vector database for embeddings
- **Hugging Face**: Model hosting and transformers library
- **Google Colab**: Free GPU resources for model deployment

---

**Note**: This is a development version. For production use, ensure all security measures are properly configured and tested. 