# Sentinel AI - Company Internal RAG Chatbot with RBAC

A secure, production-ready Retrieval-Augmented Generation (RAG) chatbot system with comprehensive role-based access control, JWT authentication, and complete audit logging.

## 🚀 Features

### Core Functionality
- **AI-Powered Q&A**: Ask questions about company documents and receive intelligent, context-aware answers
- **Vector Similarity Search**: ChromaDB-based semantic search with configurable retrieval parameters
- **LLM Integration**: Support for multiple LLM providers (Ollama, HuggingFace)
- **Source Citations**: Every answer includes citations to source documents with similarity scores

### Security & Access Control
- **JWT Authentication**: Secure token-based authentication with access and refresh tokens
- **Role-Based Access Control (RBAC)**: Department-specific document access based on user roles
- **Token Blacklisting**: Logout invalidates tokens to prevent unauthorized reuse
- **Audit Logging**: Comprehensive logging of authentication, access control, and query events

### User Experience
- **Modern Streamlit UI**: Clean, responsive interface with real-time chat
- **Admin Dashboard**: User management, audit log viewing, and system monitoring
- **Session Management**: Automatic token refresh and session duration tracking
- **Configurable Search**: Adjustable number of results and response length

## 📋 System Architecture

### Backend (FastAPI)
```
┌─────────────────────────────────────┐
│         FastAPI Backend             │
├─────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐ │
│  │ Auth Layer   │  │ RBAC Engine  │ │
│  │ - JWT        │  │ - Roles      │ │
│  │ - Passwords  │  │ - Permissions│ │
│  └──────────────┘  └──────────────┘ │
│  ┌──────────────────────────────────┤
│  │     RAG Pipeline                 │
│  │ ┌──────┐ ┌─────────┐ ┌─────────┐ │
│  │ │Query │→│Retrieval│→│Re-Rank  │ │
│  │ │Norm  │ │(Vector) │ │& Filter │ │
│  │ └──────┘ └─────────┘ └─────────┘ │
│  │           ↓                      │
│  │     ┌──────────┐                 │
│  │     │   LLM    │                 │
│  │     │Response  │                 │
│  │     └──────────┘                 │
│  └──────────────────────────────────┤
│  ┌──────────────────────────────────┤
│  │  Audit Logger & Database         │
│  └──────────────────────────────────┘
└─────────────────────────────────────┘
```

### Frontend (Streamlit)
```
┌──────────────────────────────────────┐
│        Streamlit Frontend            │
├──────────────────────────────────────┤
│  ┌────────────┐  ┌────────────────┐  │
│  │  Login     │  │  Chat Interface│  │
│  └────────────┘  └────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │      Admin Dashboard           │  │
│  │  - User Management             │  │
│  │  - Audit Logs                  │  │
│  │  - System Stats                │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

### Key Components

#### RAG Pipeline Flow
1. **Query Normalization**: Clean and expand user queries (abbreviations, ranges)
2. **RBAC Resolution**: Determine accessible departments based on user role
3. **Vector Retrieval**: Search ChromaDB collections per department
4. **Re-Ranking**: Score and deduplicate results by similarity
5. **Prompt Building**: Construct context-aware prompt with RBAC constraints
6. **LLM Generation**: Generate answer using configured LLM provider
7. **Source Formatting**: Group and format source citations

#### Authentication Flow
```
User Login → Validate Credentials → Generate JWT Tokens
                ↓
         Store in Session
                ↓
    Auto-Refresh Before Expiry
                ↓
         Logout Invalidates Tokens
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.10
- SQLite
- ChromaDB
- Ollama (optional, for local LLM)
- HuggingFace API key (optional, for HF models)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Internal-Chatbot-with-RBAC-Project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Database
DATABASE_URL=sqlite:///database/users.db

# APIs
OLLAMA_API_URL=http://localhost:11434/api/generate
HF_API_TOKEN=your-huggingface-api-token
```

4. **Initialize the database**
```bash
python -m auth.database_manager
```

5. **Prepare document data**

Ensure the following files exist in the `data/` directory:
- `all_chunks.json` - Document chunks
- `all_metadata.json` - Chunk metadata
- `chunk_embeddings.npy` - Pre-computed embeddings
- `rbac_permissions.json` - RBAC configuration
- `ABBREVIATIONS.json` - Query expansion rules
- `vector_db/` - ChromaDB persistent storage
- `documents/` - Actual documents for rendering

## 🚀 Running the Application

### Start the Backend (FastAPI)
```bash
cd backend/
uvicorn main:app --reload --host localhost --port 8000
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

### Start the Frontend (Streamlit)
```bash
cd frontend/
streamlit run app.py
```

The UI will open at `http://localhost:8501`

## 📁 Project Structure

```
Internal-Chatbot-with-RBAC/
│
├── auth/                          # Authentication & User Management
│   ├── auth_handler.py            # JWT token creation/validation
│   ├── database_manager.py        # User CRUD operations
│   ├── models.py                  # Pydantic models for auth
│   └── token_blacklist.py         # Token invalidation
│
├── rbac/                          # Role-Based Access Control
│   ├── RBACEngine.py              # Role resolution & permissions
│   ├── rbac_middleware.py         # FastAPI RBAC middleware
│   └── VectorRetriever.py         # Department-filtered search
│
├── rag/                           # RAG Pipeline Components
│   ├── RAGPipeline.py             # Complete RAG orchestration
│   ├── llm_service.py             # LLM provider integration
│   └── prompt_builder.py          # Prompt templates & formatting
│
├── services/                      # Shared Services
│   ├── audit_logger.py            # Comprehensive audit logging
│   ├── QueryNormalizer.py         # Query preprocessing
│   └── ReRanker.py                # Result re-ranking & deduplication
│
├── models/                        # Data Models
│   └── chat.py                    # Chat request/response models
│
├── components/                    # Streamlit UI Components
│   ├── login.py                   # Login interface
│   ├── chat.py                    # Chat interface
│   ├── sidebar.py                 # Settings & user info
│   └── admin.py                   # Admin dashboard
│
├── utils/                         # Frontend Utilities
│   ├── api_client.py              # Backend API wrapper
│   └── session_manager.py         # Streamlit session state
│
├── config/                        # Configuration
│   ├── config.py                  # Backend configuration
│   └── settings.py                # Frontend configuration
│
├── data/                          # Data & Logs
│   ├── documents/                 # Source documents
│   ├── vector_db/                 # ChromaDB storage
│   ├── all_chunks.json
│   ├── all_metadata.json
│   ├── chunk_embeddings.npy
│   ├── rbac_permissions.json
│   └── ABBREVIATIONS.json
│
├── logs/                          # Audit Logs
│   ├── auth_audit.log
│   ├── access_audit.log
│   └── rag_audit.log
│
├── main.py                        # FastAPI backend entry point
├── app.py                         # Streamlit frontend entry point
├── create_rag.py                  # RAG pipeline initialization
├── requirements.txt
└── README.md
```

## 👥 User Roles & Permissions

### Role Hierarchy
```
admin (All Permissions)
  ├── manager
  │   ├── finance_analyst (Finance Department)
  │   ├── hr_manager (HR Department)
  │   ├── engineering_lead (Engineering Department)
  │   └── marketing_manager (Marketing Department)
  └── intern (Limited Access)

  For detailed hierarchy you can refer to rbac_permissons.json inside data/ folder.
```

### Default Users
The system must be seeded with the users for usage you can do it by commenting out DEFAULT_USERS line in config and seed_users funtion inside startup located in main.py

## 🎯 Usage Guide

### For Regular Users

1. **Login** with your credentials
2. **Ask questions** in the chat interface
3. **View sources** to verify information
4. **Adjust settings** in the sidebar:
   - Number of documents to retrieve
   - Maximum response length
   - Toggle source citations and confidence scores

### For Administrators

1. **Access Admin Panel** via the sidebar
2. **Manage Users**:
   - Create new users
   - Update user roles
   - Activate/deactivate accounts
3. **View Audit Logs**:
   - Authentication events
   - Access control decisions
   - RAG query history
4. **Monitor System**:
   - Pipeline statistics
   - Component health
   - User activity

## 🔧 Configuration

### LLM Providers (initialise anyone)

**Ollama (Local)**
```python
LLM_PROVIDER = "ollama"
LLM_MODEL = "mistral"
OLLAMA_API_URL = "http://localhost:11434/api/generate" #in .env
```

**HuggingFace (Cloud)**
```python
LLM_PROVIDER = "hf_mistral"
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HF_API_TOKEN = "your-token" #in .env
```

**HuggingFace (Local T5)**
```python
LLM_PROVIDER = "huggingface"
LLM_MODEL = "google/flan-t5-base" #firstly download this model locally
```

### RAG Parameters

Adjust in `config.py`:
```python
TOP_K_RETRIEVAL = 4              # Documents per query
SIMILARITY_THRESHOLD = 0.3       # Minimum similarity score
MAX_CONTEXT_LENGTH = 2000        # Max tokens for context
```

## 🔐 Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Signed with HS256 algorithm
- **Token Expiry**: 15 minutes (access), 7 days (refresh)
- **Token Blacklisting**: Logout invalidates tokens
- **RBAC Enforcement**: Department-level access control
- **Audit Logging**: All security events logged with timestamps
- **Input Validation**: Pydantic models validate all inputs

## 📊 Monitoring & Logging

### Log Files
- `logs/auth_audit.log` - Authentication events (login, logout, refresh)
- `logs/access_audit.log` - Authorization decisions
- `logs/rag_audit.log` - RAG pipeline execution logs

### Metrics Available
- Total chunks indexed
- Active users
- Query processing time
- Similarity scores
- LLM provider status

## 🐛 Troubleshooting

### Backend won't start
- Verify `.env` file exists with required variables
- Check database path is writable
- Ensure port 8000 is available

### Frontend can't connect
- Verify backend is running at `http://localhost:8000`
- Check API_BASE_URL in `config/settings.py`
- Test health endpoint: `curl http://localhost:8000/`

### LLM errors
- **Ollama**: Ensure Ollama is running (`ollama serve`)
- **HuggingFace**: Verify API token is valid
- Check `llm_service.py` logs for detailed errors

### RBAC issues
- Verify `data/rbac_permissions.json` exists
- Check user role in database
- Review audit logs for access denial reasons

### Document not found
- Ensure document exists in `data/documents/`
- Verify user has department access
- Check ChromaDB collections are populated

## 🤝 Contributing

This is an internal company project. For questions or issues, contact at `akshithnalimela@gmail.com`.

## 📄 License

Internal use only. All rights reserved.

---

**Built by**: `Akshith Nalimela`