# Project Requirements Document (PRD)
## Inverbot Data Pipeline - Local Development Migration

### 1. Project Overview

**Project Name:** Inverbot Data Pipeline  
**Version:** 2.0 (Local Development Migration)  
**Date:** December 2024  
**Status:** In Development  

### 2. Project Vision

Transform the Inverbot Data Pipeline from a Colab notebook-based system to a production-ready, modular local development environment that supports the RAG (Retrieval-Augmented Generation) system for Inverbot, an AI application providing investment advice for the Paraguayan market.

### 3. Business Objectives

- **Primary Goal:** Create a robust, automated data pipeline for collecting and processing Paraguayan financial/economic data
- **Secondary Goal:** Support Inverbot's RAG system with high-quality, structured data for investment advice generation
- **Tertiary Goal:** Establish a scalable, maintainable architecture for future enhancements

### 4. Technical Requirements

#### 4.1 Architecture Requirements
- **Modular Design:** Separate concerns into distinct modules (extraction, processing, loading, orchestration)
- **Local Development:** Full development capability in Cursor IDE
- **Remote Model Execution:** LLM models deployed on Colab with localtunnel access
- **Dual Database Strategy:** PostgreSQL (Supabase) + Vector Database (Pinecone)
- **Multi-Agent System:** CrewAI orchestration for automated data processing

#### 4.2 Data Sources
Based on `Fuentes_Inverbot_Pipeline.md`:

| Category | Source | Content Types | Processing |
|----------|--------|---------------|------------|
| Company Balances | BVA Emisores | EXCEL, PDF, TEXT | Structured + Vectorized |
| Daily Movements | BVA Informes Diarios | JSON | Structured Only |
| Monthly Volume | BVA Informes Mensuales | TEXT, PDF, JSON | Structured + Vectorized |
| Annual Reports | BVA Informes Anuales | TEXT, PDF | Structured + Vectorized |
| Macroeconomic Context | BCP, MIC, MEF | TEXT, PDF, EXCEL, PPT | Structured + Vectorized |
| Social Statistics | DGEEC/INE | PDF, EXCEL, PPT, TEXT | Structured + Vectorized |
| Public Contracts | DNCP | TEXT | Structured + Vectorized |
| Investment Data | DNIT | TEXT, PNG, PDF | Structured + Vectorized |
| Financial Reports | DNIT | TEXT, PDF | Structured + Vectorized |

#### 4.3 Database Schema Requirements
Based on `Estructura_Datos_Inverbot.md`:

**Supabase (PostgreSQL) Tables:**
- `Categoria_Emisor`, `Emisores`, `Moneda`, `Frecuencia`, `Tipo_Informe`, `Periodo_Informe`
- `Unidad_Medida`, `Fuente_Noticia`, `Instrumento`, `Informe_General`
- `Resumen_Informe_Financiero`, `Dato_Macroeconomico`, `Movimiento_Diario_Bolsa`, `Licitacion_Contrato`

**Pinecone Indexes:**
- `documentos-informes-vector` (384 dimensions, cosine metric)
- `noticia-relevante-vector` (384 dimensions, cosine metric)
- `dato-macroeconomico-vector` (384 dimensions, cosine metric)
- `licitacion-contrato-vector` (384 dimensions, cosine metric)

#### 4.4 Model Requirements
- **LLM Model:** mistralai/Mistral-7B-Instruct-v0.3 (deployed on Colab)
- **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2 (deployed on Colab)
- **Access Method:** HTTP API via localtunnel
- **Integration:** CrewAI-compatible LLM wrapper

### 5. Functional Requirements

#### 5.1 Data Extraction Module
- **Web Scraping:** Extract content from HTML pages
- **File Download:** Download PDFs, Excel files, images
- **API Integration:** Fetch JSON data from endpoints
- **Content Type Detection:** Automatically identify content types
- **Error Handling:** Graceful handling of network issues and missing content

#### 5.2 Structured Processing Module
- **Schema Mapping:** Map extracted data to Supabase schemas
- **Data Validation:** Ensure data quality and type consistency
- **LLM Integration:** Use Mistral model for intelligent data extraction
- **Multi-format Support:** Handle JSON, text, and document content

#### 5.3 Vector Processing Module
- **Text Chunking:** Split documents into appropriate chunks
- **Embedding Generation:** Create vector embeddings for each chunk
- **Metadata Preparation:** Prepare metadata for Pinecone storage
- **Batch Processing:** Handle large volumes efficiently

#### 5.4 Loading Module
- **Database Operations:** Insert/update data in Supabase
- **Vector Storage:** Upsert vectors in Pinecone
- **Transaction Management:** Ensure data consistency
- **Conflict Resolution:** Handle duplicate data scenarios

#### 5.5 Orchestration Module
- **CrewAI Integration:** Coordinate multi-agent workflow
- **Pipeline Management:** Execute sequential processing stages
- **Error Recovery:** Handle failures and retry mechanisms
- **Monitoring:** Track pipeline execution and performance

### 6. Non-Functional Requirements

#### 6.1 Performance
- **Processing Speed:** Handle 100+ documents per hour
- **Memory Efficiency:** Optimize for large document processing
- **Concurrent Processing:** Support parallel data source processing

#### 6.2 Reliability
- **Error Recovery:** Automatic retry mechanisms
- **Data Integrity:** Ensure no data loss during processing
- **Backup Strategy:** Regular data backups

#### 6.3 Security
- **API Key Management:** Secure storage of credentials
- **Data Privacy:** Protect sensitive financial information
- **Access Control:** Restrict database access

#### 6.4 Maintainability
- **Modular Code:** Clear separation of concerns
- **Documentation:** Comprehensive code and API documentation
- **Testing:** Unit and integration test coverage
- **Logging:** Detailed execution logs

### 7. Development Environment Requirements

#### 7.1 Local Development
- **IDE:** Cursor with Python support
- **Version Control:** Git with proper branching strategy
- **Environment Management:** Virtual environment with dependency management
- **Configuration:** Environment variables for sensitive data

#### 7.2 Remote Model Deployment
- **Colab Setup:** Dedicated notebooks for model deployment
- **Localtunnel Configuration:** HTTP API exposure for local access
- **Model Persistence:** Ensure models remain loaded during development
- **API Documentation:** Clear endpoint specifications

### 8. Success Criteria

#### 8.1 Technical Success
- [ ] All modules successfully extract from Colab notebook
- [ ] Local development environment fully functional
- [ ] Models accessible via localtunnel from local environment
- [ ] Complete data pipeline executes without errors
- [ ] All database operations successful

#### 8.2 Quality Success
- [ ] Code follows modular architecture principles
- [ ] Comprehensive test coverage implemented
- [ ] Documentation complete and up-to-date
- [ ] Error handling robust and informative
- [ ] Performance meets specified requirements

#### 8.3 Business Success
- [ ] Pipeline successfully processes all data sources
- [ ] Data quality meets Inverbot RAG system requirements
- [ ] System ready for production deployment
- [ ] Scalable architecture supports future growth

### 9. Constraints and Assumptions

#### 9.1 Constraints
- **Resource Limitations:** Local machine cannot run large LLM models
- **Network Dependencies:** Requires stable internet for Colab model access
- **API Rate Limits:** Respect source website rate limits
- **Data Volume:** Handle varying data volumes efficiently

#### 9.2 Assumptions
- **Colab Availability:** Google Colab remains accessible and stable
- **Model Compatibility:** Mistral model works with CrewAI framework
- **Data Source Stability:** Source websites maintain consistent structure
- **API Access:** Required APIs remain available and functional

### 10. Risk Assessment

#### 10.1 Technical Risks
- **Model Integration:** CrewAI compatibility with custom LLM setup
- **Network Reliability:** Localtunnel connection stability
- **Data Source Changes:** Website structure modifications
- **Performance Issues:** Large document processing bottlenecks

#### 10.2 Mitigation Strategies
- **Fallback Options:** Alternative model deployment strategies
- **Monitoring:** Real-time connection and performance monitoring
- **Adaptive Processing:** Flexible content extraction logic
- **Optimization:** Performance profiling and optimization

### 11. Timeline and Milestones

#### Phase 1: Foundation (Week 1)
- Git repository setup
- Project structure creation
- Environment configuration
- Colab model deployment

#### Phase 2: Core Modules (Week 2-3)
- Extraction module development
- Processing module development
- Loading module development
- Basic integration testing

#### Phase 3: Orchestration (Week 4)
- CrewAI integration
- Pipeline orchestration
- End-to-end testing
- Documentation completion

#### Phase 4: Production Readiness (Week 5)
- Performance optimization
- Error handling refinement
- Monitoring implementation
- Deployment preparation 