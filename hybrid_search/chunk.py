from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

from hybrid_search.utils import singleton

@singleton
class SemanticChunk:
    def __init__(self):
        self.hf_embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.text_splitter = SemanticChunker(self.hf_embedder, breakpoint_threshold_type="percentile")
    
    def split(self, text):
        docs = self.text_splitter.split_text(text)
        return docs
