# NEURAL CONNECTION GUIDE - USER MANUAL

## 🔌 Establishing a Connection

To activate the system properly, follow these steps:

1. **Environment Setup**:
   Ensure `.env` files in `DEV CORE` and `Advanced_RAG_Chatbot` are configured with valid API keys (Groq, etc.).

2. **System Activation**:
   Launch the system via terminal:
   ```powershell
   ./unified_launcher.ps1
   ```

3. **Interface Selection**:
   - Use the **Neural UI** (Streamlit) for advanced RAG queries.
   - Use the **Legacy Interface** for standard chatbot interactions.

## 🧠 Interacting with the Unified Core

- **Direct Queries**: Ask anything from general coding questions to complex security audits.
- **Source Verification**: Use the "Verified Neural Nodes" expander to see which documents informed the response.
- **Analytics**: Monitor response times and confidence levels in the sidebar.

## 📂 Document Ingestion
To add new knowledge to the core:
1. Place PDFs in `Advanced_RAG_Chatbot/pdfs/unified`.
2. Run the ingestion script:
   ```bash
   cd Advanced_RAG_Chatbot
   venv/Scripts/python.exe ingest_pdfs.py
   ```

---
*Status: All Systems Operational*
