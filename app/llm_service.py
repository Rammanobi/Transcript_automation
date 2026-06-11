import os
import json
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # Requires OPENAI_API_KEY environment variable to be set
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    async def extract_action_items(self, chunk_id: int, content: str) -> list:
        prompt = f"""
        You are an expert meeting transcript analyzer. Extract all action items from the provided transcript chunk.
        
        Requirements:
        1. Extract explicit and implicit action items.
        2. Identify assignees, deadlines (due_context), priority, and dependencies/context (description).
        3. Rate your confidence in the extraction (0.0 to 1.0).
        4. MUST RETURN A JSON OBJECT containing an 'items' array. NO MARKDOWN. NO EXPLANATION.
        
        Output format:
        {{
            "items": [
                {{
                    "title": "Actionable Title",
                    "description": "Context and details",
                    "assignee": "Name or empty string",
                    "priority": "High/Medium/Low or empty string",
                    "due_context": "Deadline or empty string",
                    "chunk_id": {chunk_id},
                    "confidence": 0.95
                }}
            ]
        }}
        
        Transcript Chunk:
        {content}
        """
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        raw_content = response.choices[0].message.content
        data = json.loads(raw_content)
        return data.get("items", [])
