import httpx
import logging
import asyncio
from .models import Phase3Output

logger = logging.getLogger(__name__)

class WebhookDelivery:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def deliver(self, data: Phase3Output, max_retries=3) -> bool:
        if not self.webhook_url:
            logger.warning("No webhook URL configured. Skipping delivery.")
            return False
            
        payload = data.model_dump()
        
        for attempt in range(1, max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        self.webhook_url,
                        json=payload
                    )
                    response.raise_for_status()
                    logger.info(f"Successfully delivered to n8n on attempt {attempt}. Status: {response.status_code}")
                    return True
            except httpx.RequestError as e:
                logger.error(f"Request error on attempt {attempt} to deliver to webhook: {e}")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code} on attempt {attempt} to deliver to webhook")
            
            if attempt < max_retries:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
        logger.error("Failed to deliver to webhook after all attempts.")
        return False
