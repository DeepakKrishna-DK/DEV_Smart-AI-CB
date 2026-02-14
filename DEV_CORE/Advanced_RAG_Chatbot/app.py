import streamlit as st
import os
import pandas as pd
import plotly.express as px
from config import Config
from themes import apply_theme, THEMES
from chatbot import RAGChatbot

# Force CPU for stability
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Page Config
st.set_page_config(
    page_title="DEV SYSTEM - Unified Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Resource Caching for Speed
@st.cache_resource
def get_embeddings():
    import torch
    # Deep force CPU
    device = "cpu"
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    
    return HuggingFaceEmbeddings(
        model_name=Config.FREE_EMBEDDING_MODEL,
        model_kwargs={'device': device}
    )

@st.cache_resource
def load_chatbot(category):
    embeddings = get_embeddings()
    # Path check for developer friendliness
    db_path = os.path.join(Config.VECTOR_DB_DIR, category)
    if not os.path.exists(db_path) and category != "mern":
        st.error(f"⚠️ Unified Intelligence Core is still synchronizing. Please wait 2-3 minutes for the first-time setup to complete.")
        st.stop()
    return RAGChatbot(category, embeddings=embeddings)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stats" not in st.session_state:
    st.session_state.stats = {
        "queries": 0,
        "total_time": 0,
        "cache_hits": 0,
        "history": []
    }

# Initialization is now lazy - instances created only when selected

# Sidebar
st.sidebar.title("🤖 DEV CORE")
chatbot_type = st.sidebar.selectbox("🎯 Neural Pathway", ["Unified Neural Core", "Legacy Logic Core"], index=0)
category_map = {
    "Unified Neural Core": "unified",
    "Legacy Logic Core": "mern"
}
category = category_map[chatbot_type]

theme_choice = st.sidebar.selectbox("🎨 UI Theme", list(THEMES.keys()), index=0)
apply_theme(theme_choice)

st.sidebar.divider()

# Analytics Section
st.sidebar.subheader("📊 Performance Analytics")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Queries", st.session_state.stats["queries"])
with col2:
    hit_rate = (st.session_state.stats["cache_hits"] / st.session_state.stats["queries"] * 100) if st.session_state.stats["queries"] > 0 else 0
    st.metric("Cache Hit Rate", f"{hit_rate:.1f}%")

avg_time = (st.session_state.stats["total_time"] / st.session_state.stats["queries"]) if st.session_state.stats["queries"] > 0 else 0
st.sidebar.metric("Avg Response Time", f"{avg_time:.0f} ms")

if st.sidebar.button("🗑️ Clear Cache"):
    load_chatbot(category).cache.clear()
    st.sidebar.success("Cache cleared!")

st.sidebar.divider()
st.sidebar.markdown(f"**Mode:** {'Unified DEV System'}")
st.sidebar.caption(f"System State: Online")

# Main Header
st.title(f"🚀 {chatbot_type.upper()}")
st.markdown(f"**Status:** Neural Link Synchronized | **Systems:** Operational")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "confidence" in message:
            # Show confidence and sources
            conf = message["confidence"]
            color = "green" if conf > 70 else "orange" if conf > 40 else "red"
            st.markdown(f"""
                <div class='cache-indicator'>{'⚡ Cached Response' if message.get('is_cached') else f'⏱️ Generated in {message.get("response_time", 0):.0f}ms'}</div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 0.8rem;'>Confidence: {conf}%</span>
                    <div class='confidence-meter' style='flex-grow: 1; height: 5px;'>
                        <div class='confidence-fill' style='width: {conf}%; background: {color}; height: 100%;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("🧠 Verified Neural Nodes"):
                for source in message.get("sources", []):
                    st.write(f"- {source}")

# User Input
if prompt := st.chat_input("Query the Unified Intelligence Core..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Initializing Neural Core..."):
            chatbot = load_chatbot(category)
            result = chatbot.query(prompt)
            
            # Update Stats
            st.session_state.stats["queries"] += 1
            st.session_state.stats["total_time"] += result["response_time"]
            if result["is_cached"]:
                st.session_state.stats["cache_hits"] += 1
            
            # Display
            st.markdown(result["answer"])
            
            # Confidence UI
            conf = result["confidence"]
            color = "green" if conf > 70 else "orange" if conf > 40 else "red"
            st.markdown(f"""
                <div class='cache-indicator'>{'⚡ Cached Response' if result['is_cached'] else f'⏱️ Generated in {result["response_time"]:.0f}ms'}</div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 0.8rem;'>Confidence: {conf}%</span>
                    <div class='confidence-meter' style='flex-grow: 1; height: 5px;'>
                        <div class='confidence-fill' style='width: {conf}%; background: {color}; height: 100%;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🧠 Verified Neural Nodes"):
                for source in result["sources"]:
                    st.write(f"- {source}")
            
            # Add to history
            assistant_message = {
                "role": "assistant", 
                "content": result["answer"],
                "confidence": result["confidence"],
                "sources": result["sources"],
                "is_cached": result["is_cached"],
                "response_time": result["response_time"]
            }
            st.session_state.messages.append(assistant_message)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Built with ❤️ for the AI community</div>", unsafe_allow_html=True)
