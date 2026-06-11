import asyncio
import time
import logging
from typing import List, Dict, Any
from .models import Chunk, ChunkResult, Phase2Output, ActionItemCandidate
from .llm_service import LLMService

logger = logging.getLogger(__name__)

class MapEngine:
    def __init__(self):
        self.llm_service = LLMService()
        self.max_retries = 5
        self.backoff_sequence = [1, 2, 4, 8, 10]
        self.concurrency_limit = 2

    async def _process_chunk_with_retry(self, chunk: Chunk) -> Dict[str, Any]:
        start_time = time.time()
        for attempt in range(self.max_retries):
            try:
                items_data = await self.llm_service.extract_action_items(chunk.chunk_id, chunk.content)
                
                valid_items = []
                for item in items_data:
                    # Enforce chunk_id matching
                    item['chunk_id'] = chunk.chunk_id
                    try:
                        candidate = ActionItemCandidate(**item)
                        valid_items.append(candidate)
                    except Exception as ve:
                        logger.warning(f"Chunk {chunk.chunk_id} produced an invalid item: {ve}")
                
                duration = time.time() - start_time
                logger.info(f"Chunk {chunk.chunk_id} Success. Duration: {duration:.2f}s, Retries: {attempt}")
                
                return {
                    "chunk_id": chunk.chunk_id,
                    "success": True,
                    "items": valid_items,
                    "retries": attempt,
                    "duration": duration
                }

            except Exception as e:
                logger.error(f"Chunk {chunk.chunk_id} Failed on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.backoff_sequence[attempt])
                else:
                    duration = time.time() - start_time
                    logger.error(f"Chunk {chunk.chunk_id} completely failed after {self.max_retries} attempts.")
                    return {
                        "chunk_id": chunk.chunk_id,
                        "success": False,
                        "items": [],
                        "retries": attempt,
                        "duration": duration
                    }

    async def process_chunks(self, chunks: List[Chunk]) -> Phase2Output:
        semaphore = asyncio.Semaphore(self.concurrency_limit)
        
        async def bounded_process(chunk: Chunk):
            async with semaphore:
                return await self._process_chunk_with_retry(chunk)

        tasks = [bounded_process(chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)
        
        successful_chunks = 0
        failed_chunks = 0
        raw_results = []
        
        for res in results:
            if res["success"]:
                successful_chunks += 1
                raw_results.append(ChunkResult(chunk_id=res["chunk_id"], items=res["items"]))
            else:
                failed_chunks += 1
                
        return Phase2Output(
            processed_chunks=len(chunks),
            successful_chunks=successful_chunks,
            failed_chunks=failed_chunks,
            raw_results=raw_results
        )
