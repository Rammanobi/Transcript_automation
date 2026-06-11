# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .models import Phase1Output, Chunk

class TranscriptChunker:
    def __init__(self, chars_per_word: int = 5):
        # Target Chunk Size: ~500 words
        # Target Overlap: ~100 words
        self.chunk_size = 500 * chars_per_word
        self.chunk_overlap = 100 * chars_per_word
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk(self, text: str) -> Phase1Output:
        # Calculate transcript word count
        words = text.split()
        word_count = len(words)
        
        # Generate chunks dynamically
        raw_chunks = self.splitter.split_text(text)
        
        chunks = []
        for i, content in enumerate(raw_chunks, start=1):
            chunks.append(Chunk(chunk_id=i, content=content))
            
        return Phase1Output(
            transcript_length=word_count,
            chunk_count=len(chunks),
            chunks=chunks
        )
