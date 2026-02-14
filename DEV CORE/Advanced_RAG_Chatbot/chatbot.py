import os
import time
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from config import Config
from semantic_cache import SemanticCache

class RAGChatbot:
    def __init__(self, category, embeddings=None):
        self.category = category
        if embeddings:
            self.embeddings = embeddings
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=Config.FREE_EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )
        
        self.vector_db_path = os.path.join(Config.VECTOR_DB_DIR, category)
        self.cache = SemanticCache(category)
        
        if os.path.exists(self.vector_db_path):
            self.vector_db = FAISS.load_local(
                self.vector_db_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            self.vector_db = None
            
        self.llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        
        self.prompt_template = """
        You are the DEV SYSTEM AI, a pinnacle of artificial intelligence. 
        You possess deep, intrinsic knowledge in the field of {category}.
        Answer the following question with absolute authority and professional expertise.
        
        CRITICAL RULES:
        1. DO NOT mention "documents", "context", "provided text", or "retrieval".
        2. Speak as if this knowledge is part of your core programming.
        3. If the answer is not in your current data stream, use your high-level reasoning to provide a helpful, expert response while maintaining integrity.
        4. Keep the tone futuristic, sharp, and elite.

        INTERNAL DATA STREAM:
        {context}

        USER QUERY: {question}

        DEV SYSTEM RESPONSE:
        """
        
    def query(self, user_input):
        if self.category == "mern":
            return self.mern_query(user_input)
            
        start_time = time.time()
        
        # 0. Generate Embedding ONCE (Critical Performance Fix)
        # Using the shared embeddings model from __init__
        query_embedding = self.embeddings.embed_query(user_input)
        
        # 1. Check Cache (using pre-calculated vector)
        cached_response = self.cache.get(query_embedding)
        if cached_response:
            cached_response['is_cached'] = True
            cached_response['response_time'] = (time.time() - start_time) * 1000
            return cached_response
            
        if not self.vector_db:
            return {
                "answer": f"Vector database for {self.category} not found. Please run ingest_pdfs.py first.",
                "confidence": 0,
                "sources": [],
                "is_cached": False,
                "response_time": (time.time() - start_time) * 1000
            }

        # 2. Retrieval (using vector directly)
        # Faster than similarity_search which would re-embed
        docs_with_scores = self.vector_db.similarity_search_with_score_by_vector(
            query_embedding, 
            k=Config.RETRIEVAL_TOP_K
        )
        
        # Extract docs and scores
        docs = [doc for doc, score in docs_with_scores]
        scores = [score for doc, score in docs_with_scores]
        
        # Intelligence Confidence (Aggressive Logic)
        avg_score = sum(scores) / len(scores) if scores else 1.0
        
        # Low distance = High similarity (FAISS default L2 distance)
        # 0.0 is exact match
        if avg_score < 0.7:
            confidence = min(100, int(100 - (avg_score * 10)))
        elif avg_score < 1.1:
            confidence = int(95 - (avg_score - 0.7) * 100)
            confidence = max(75, confidence)
        else:
            confidence = max(30, int(70 - (avg_score - 1.1) * 50))
            
        if avg_score < 0.5: confidence = 100
        
        # 4. Generate Answer
        context_str = "\n".join([doc.page_content for doc in docs])
        
        display_category = "Unified Global Intelligence" if self.category == "unified" else self.category.capitalize()
        
        prompt = self.prompt_template.format(
            category=display_category,
            context=context_str,
            question=user_input
        )
        
        try:
            response = self.llm.invoke(prompt)
            answer = response.content
        except Exception as e:
            answer = f"Neural Link Interrupted: {str(e)}"
            confidence = 0
        
        # 5. Extract Sources
        sources = list(set([os.path.basename(doc.metadata.get('source', 'Unknown')) for doc in docs]))
        
        result = {
            "answer": answer,
            "confidence": confidence,
            "sources": sources,
            "is_cached": False,
            "response_time": (time.time() - start_time) * 1000
        }
        
        # 6. Save to Cache (store text + vector)
        self.cache.set(user_input, query_embedding, result)
        
        return result

    def mern_query(self, user_input):
        import requests
        start_time = time.time()
        try:
            response = requests.post("http://localhost:5000/api/df_text_query", json={
                "text": user_input,
                "userID": "dev-system-user"
            }, timeout=10)
            data = response.json()
            # Extract answer from fulfillmentText or the first fulfillmentMessage
            answer = data.get("fulfillmentText")
            if not answer and "fulfillmentMessages" in data:
                try:
                    answer = data["fulfillmentMessages"][0]["text"]["text"][0]
                except (KeyError, IndexError):
                    pass
            
            if not answer:
                answer = "I'm sorry, I couldn't process that request from the MERN Core."
                
            return {
                "answer": answer,
                "confidence": 100 if data.get("intent") else 50,
                "sources": ["MERN Legacy Knowledge Base"],
                "is_cached": False,
                "response_time": (time.time() - start_time) * 1000
            }
        except Exception as e:
            return {
                "answer": f"Connection to MERN Core failed: {str(e)}",
                "confidence": 0,
                "sources": [],
                "is_cached": False,
                "response_time": (time.time() - start_time) * 1000
            }
