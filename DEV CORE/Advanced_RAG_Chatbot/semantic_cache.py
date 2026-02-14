import os
import json
import numpy as np
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

class SemanticCache:
    def __init__(self, category):
        self.category = category
        self.cache_file = os.path.join(Config.CACHE_DIR, f"{category}_cache.json")
        self.cache_data = self._load()
        
    def _load(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache_data, f)

    def get(self, query_embedding, threshold=0.85):
        if not self.cache_data:
            return None
            
        # Ensure query_embedding is numpy array
        if not isinstance(query_embedding, np.ndarray):
            query_embedding = np.array(query_embedding)
        
        best_match = None
        max_similarity = -1
        
        for entry in self.cache_data:
            # Entry embedding is list from JSON
            cached_embedding = np.array(entry['embedding'])
            
            # Cosine similarity
            similarity = np.dot(query_embedding, cached_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(cached_embedding)
            )
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = entry
        
        if max_similarity >= threshold:
            print(f"Cache hit! Similarity: {max_similarity:.2f}")
            return best_match['response']
        
        return None

    def set(self, query, embedding, response):
        # Store embedding as list for JSON serialization
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
            
        self.cache_data.append({
            'query': query,
            'response': response,
            'embedding': embedding
        })
        self._save()

    def clear(self):
        self.cache_data = []
        self._save()
