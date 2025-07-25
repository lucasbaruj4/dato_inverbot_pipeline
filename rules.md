# Development Rules and Guidelines
## Inverbot Data Pipeline

### 1. Project Structure Rules

#### 1.1 Modular Architecture
- **Separation of Concerns:** Each module must have a single, well-defined responsibility
- **Loose Coupling:** Modules should communicate through well-defined interfaces
- **High Cohesion:** Related functionality should be grouped together
- **Dependency Management:** Use dependency injection and avoid circular dependencies

#### 1.2 File Organization
```
inverbot_data_pipeline/
├── src/
│   ├── extraction/
│   ├── processing/
│   ├── vectorization/
│   ├── loading/
│   ├── orchestration/
│   └── utils/
├── tests/
├── config/
├── docs/
├── scripts/
└── notebooks/
```

#### 1.3 Naming Conventions
- **Files:** snake_case (e.g., `data_extractor.py`)
- **Classes:** PascalCase (e.g., `DataExtractor`)
- **Functions/Variables:** snake_case (e.g., `extract_data`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)
- **Modules:** snake_case (e.g., `data_processing`)

### 2. Code Quality Rules

#### 2.1 Code Style
- **PEP 8 Compliance:** Follow Python style guide
- **Type Hints:** Use type annotations for all function parameters and return values
- **Docstrings:** Include comprehensive docstrings for all classes and functions
- **Line Length:** Maximum 88 characters (Black formatter standard)

#### 2.2 Error Handling
- **Graceful Degradation:** Handle errors without crashing the entire pipeline
- **Logging:** Use structured logging for all operations
- **Retry Logic:** Implement exponential backoff for network operations
- **Validation:** Validate all inputs and outputs

#### 2.3 Performance
- **Memory Management:** Use generators for large datasets
- **Batch Processing:** Process data in appropriate batch sizes
- **Caching:** Cache expensive operations when appropriate
- **Async Operations:** Use async/await for I/O operations

### 3. Security Rules

#### 3.1 Environment Variables
- **Never Hardcode Secrets:** All sensitive data must be in environment variables
- **Secure Storage:** Use `.env` files (not committed to git) for local development
- **Validation:** Validate all required environment variables on startup
- **Rotation:** Regularly rotate API keys and credentials

#### 3.2 Data Protection
- **Input Validation:** Validate all external inputs
- **SQL Injection Prevention:** Use parameterized queries
- **Rate Limiting:** Respect API rate limits
- **Data Encryption:** Encrypt sensitive data in transit and at rest

### 4. Testing Rules

#### 4.1 Test Coverage
- **Minimum Coverage:** 80% code coverage for all modules
- **Unit Tests:** Test all public functions and methods
- **Integration Tests:** Test module interactions
- **End-to-End Tests:** Test complete pipeline workflows

#### 4.2 Test Structure
- **Test Organization:** Mirror source code structure in tests
- **Test Naming:** Use descriptive test names that explain the scenario
- **Mocking:** Mock external dependencies (APIs, databases)
- **Test Data:** Use fixtures and factories for test data

#### 4.3 Test Execution
- **Automated Testing:** Run tests on every commit
- **Test Isolation:** Each test should be independent
- **Fast Execution:** Unit tests should complete in under 30 seconds
- **CI/CD Integration:** Integrate tests into deployment pipeline

### 5. Documentation Rules

#### 5.1 Code Documentation
- **Function Documentation:** Document purpose, parameters, return values, and exceptions
- **Class Documentation:** Document purpose, attributes, and methods
- **Module Documentation:** Document module purpose and usage
- **Examples:** Include usage examples in docstrings

#### 5.2 Project Documentation
- **README.md:** Comprehensive project overview and setup instructions
- **API Documentation:** Document all public APIs
- **Architecture Documentation:** Document system design and data flow
- **Deployment Documentation:** Document deployment procedures

### 6. Version Control Rules

#### 6.1 Git Workflow
- **Branch Strategy:** Use feature branches for development
- **Commit Messages:** Use conventional commit format
- **Pull Requests:** Require code review for all changes
- **Merge Strategy:** Use squash and merge for feature branches

#### 6.2 Commit Guidelines
```
feat: add new data extraction module
fix: resolve memory leak in vector processing
docs: update API documentation
test: add unit tests for extraction module
refactor: improve error handling in loading module
```

### 7. Database Rules

#### 7.1 Data Integrity
- **No Data Deletion:** Never delete data without explicit user confirmation
- **Transaction Management:** Use transactions for multi-step operations
- **Backup Strategy:** Regular automated backups
- **Data Validation:** Validate data before insertion

#### 7.2 Schema Management
- **Migration Strategy:** Use database migrations for schema changes
- **Version Control:** Track all schema changes in version control
- **Backward Compatibility:** Maintain backward compatibility when possible
- **Indexing:** Create appropriate indexes for performance

### 8. Model Integration Rules

#### 8.1 Colab Model Deployment
- **Localtunnel Setup:** Use localtunnel for secure model access
- **API Design:** Design RESTful APIs for model interactions
- **Error Handling:** Handle model unavailability gracefully
- **Monitoring:** Monitor model performance and availability

#### 8.2 Model Communication
- **Headers:** Use required headers for localtunnel communication
- **Retry Logic:** Implement retry logic for model API calls
- **Timeout Handling:** Set appropriate timeouts for model requests
- **Fallback Strategy:** Have fallback options when models are unavailable

### 9. Pipeline Rules

#### 9.1 Data Flow
- **Idempotency:** Pipeline should be idempotent (safe to run multiple times)
- **Checkpointing:** Save progress to allow resuming from failures
- **Monitoring:** Track pipeline progress and performance
- **Alerting:** Alert on pipeline failures

#### 9.2 Resource Management
- **Memory Usage:** Monitor and optimize memory usage
- **CPU Usage:** Optimize CPU-intensive operations
- **Network Usage:** Minimize network overhead
- **Storage Usage:** Manage temporary file storage

### 10. Deployment Rules

#### 10.1 Environment Management
- **Environment Separation:** Separate development, staging, and production
- **Configuration Management:** Use configuration files for different environments
- **Dependency Management:** Pin all dependency versions
- **Containerization:** Use Docker for consistent deployments

#### 10.2 Monitoring and Logging
- **Application Logging:** Log all important events
- **Performance Monitoring:** Monitor application performance
- **Error Tracking:** Track and alert on errors
- **Health Checks:** Implement health check endpoints

### 11. Specific Project Rules

#### 11.1 CrewAI Integration
- **Agent Design:** Design agents with clear, single responsibilities
- **Task Definition:** Define tasks with clear inputs and outputs
- **Tool Integration:** Integrate tools properly with agents
- **Error Recovery:** Implement error recovery in agent workflows

#### 11.2 Data Source Handling
- **Rate Limiting:** Respect source website rate limits
- **Robust Scraping:** Handle website structure changes gracefully
- **Content Validation:** Validate extracted content quality
- **Source Attribution:** Track data source for all extracted data

#### 11.3 Vector Database Operations
- **Batch Operations:** Use batch operations for vector insertions
- **Metadata Management:** Ensure consistent metadata structure
- **Index Management:** Monitor and optimize Pinecone indexes
- **Vector Quality:** Validate embedding quality and consistency

### 12. Code Review Rules

#### 12.1 Review Process
- **Required Reviews:** All code changes require at least one review
- **Review Checklist:** Use standardized review checklist
- **Automated Checks:** Run automated checks before review
- **Documentation Review:** Review documentation updates

#### 12.2 Review Criteria
- **Functionality:** Code works as intended
- **Performance:** No performance regressions
- **Security:** No security vulnerabilities
- **Maintainability:** Code is maintainable and readable

### 13. Emergency Procedures

#### 13.1 Incident Response
- **Immediate Actions:** Stop pipeline if data corruption detected
- **Investigation:** Investigate root cause thoroughly
- **Communication:** Communicate issues to stakeholders
- **Recovery:** Implement recovery procedures

#### 13.2 Rollback Procedures
- **Database Rollback:** Procedures for database rollback
- **Code Rollback:** Procedures for code rollback
- **Configuration Rollback:** Procedures for configuration rollback
- **Testing:** Test rollback procedures regularly 