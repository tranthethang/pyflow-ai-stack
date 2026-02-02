# FastAPI Node Boilerplate

A high-performance **FastAPI** boilerplate specifically designed for developing **nodes** and **workers** within microservices or **Workflow Automation systems** (such as **Dify**).

This project provides a robust foundation for AI-powered components, featuring native integration with Google Gemini, asynchronous caching, and scalable object storage.

## 🚀 Purpose
This boilerplate is optimized for:
- **Microservices**: Acting as a specialized node for processing specific tasks.
- **Workflow Automation**: Easily integrate as a custom tool or worker in platforms like **Dify**, LangChain, or internal automation pipelines.
- **AI Workers**: Native support for LLM-driven tasks with pre-configured Gemini API integration.

## ✨ Key Features
- **FastAPI**: Modern, high-performance web framework.
- **Gemini AI**: Built-in service for Google's Generative AI models.
- **Redis Caching**: Asynchronous caching to optimize performance and reduce API costs.
- **AWS S3 / MinIO**: Scalable object storage for handling documents, images, or datasets.
- **Health Diagnostics**: Integrated `verify.py` to ensure all external services (Redis, S3, Gemini) are correctly configured.
- **Developer Experience**: Pre-configured `black` and `isort` for formatting, and `pytest` for comprehensive testing.

## 🛠️ Getting Started

### Prerequisites
- Python 3.9+
- Redis (local or remote)
- AWS S3 or MinIO credentials
- Google Gemini API Key

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fastapi-node-boilerplate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r [./requirements.txt](./requirements.txt)
   ```

3. **Environment Setup**:
   ```bash
   cp [./.env.example](./.env.example) .env
   # Edit .env with your specific credentials
   ```

## 📂 Project Structure
- [./app/](./app/): Core application logic.
  - [./app/api/](./app/api/): API versioned routes.
  - [./app/services/](./app/services/): Business logic for Gemini, Redis, and S3.
- [./verify.py](./verify.py): Diagnostic tool for service connectivity.
- [./tests/](./tests/): Comprehensive test suite.

## 🛠️ Usage

### Run the Application
```bash
sh [./bin/start.sh](./bin/start.sh)
```

### Verify System Health
Before deploying, ensure all services are connected:
```bash
python [./verify.py](./verify.py)
```

### Formatting
```bash
sh [./bin/format.sh](./bin/format.sh)
```

### Testing
```bash
sh [./bin/test.sh](./bin/test.sh)
```
