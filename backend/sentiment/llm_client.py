"""
LLM Clients for Agromate sentiment analysis.
Supports Groq (free), Gemini, and Mock clients.
"""

import os
import json
import random
import time
import logging
from typing import Dict, Literal, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

SentimentType = Literal["ALCISTA", "BAJISTA", "NEUTRAL"]


class BaseLLMClient(ABC):
    """Base class for LLM clients."""
    
    @abstractmethod
    def analyze(self, text: str, source: str = None) -> Dict[str, any]:
        """Analyze text and return sentiment classification."""
        pass
    
    def analyze_batch(self, texts: list[str], sources: list[str] = None) -> list[Dict[str, any]]:
        """Analyze multiple texts in batch."""
        sources = sources or [None] * len(texts)
        results = []
        for i, text in enumerate(texts):
            source = sources[i] if i < len(sources) else None
            results.append(self.analyze(text, source))
        return results



# Import Pydantic at module level
try:
    from pydantic import BaseModel, Field, validator, ValidationError
except ImportError:
    # Fallback/mock for Pydantic if missing (though it should be there)
    BaseModel = object
    Field = lambda *args, **kwargs: None
    validator = lambda *args, **kwargs: lambda f: f

class AgroSentimentResponse(BaseModel):
    sentiment: str = Field(..., description="ALCISTA, BAJISTA, or NEUTRAL")
    confidence: float = Field(..., ge=0.0, le=1.0)
    commodity: str = Field("GENERAL", description="Primary commodity or GENERAL")
    reasoning: str = Field(None, description="Brief explanation")

    @validator("sentiment")
    def validate_sentiment(cls, v):
        v = v.upper()
        if v not in ["ALCISTA", "BAJISTA", "NEUTRAL"]:
            return "NEUTRAL"
        return v

    @validator("commodity")
    def validate_commodity(cls, v):
        if not v:
            return "GENERAL"
        v = v.upper().strip()
        
        # Handle irrelevant explicitly
        if "IRRELEVANT" in v:
            return "IRRELEVANT"
            
        # Allow multi-commodity (comma separated)
        parts = [p.strip() for p in v.split(",") if p.strip()]
        valid_list = ["SOJA", "MAÍZ", "TRIGO", "GIRASOL", "CEBADA", "SORGO", "GENERAL"]
        mapping = {
            "MAIZ": "MAÍZ", "SOYBEAN": "SOJA", "WHEAT": "TRIGO", 
            "CORN": "MAÍZ", "SUNFLOWER": "GIRASOL", "SORGHUM": "SORGO",
            "BARLEY": "CEBADA"
        }
        
        cleaned_parts = []
        for p in parts:
            if p in mapping:
                cleaned_parts.append(mapping[p])
            elif p in valid_list:
                cleaned_parts.append(p)
            # If part is not valid, ignore or map to GENERAL if it's the only one?
            # Let's be permissive: if it contains valid ones, keep them.
        
        if not cleaned_parts:
            return "GENERAL" # Fallback if no valid commodity found
            
        return ", ".join(list(set(cleaned_parts))) # Remove duplicates

class GroqLLMClient(BaseLLMClient):
    """
    Real LLM client using Groq API (FREE TIER).
    
    Uses llama-3.3-70b-versatile for high-quality sentiment analysis.
    Free tier: 30 requests per minute, 14,400 per day.
    Rate limiter: 2s delay between calls to stay well within limits.
    """
    
    MAX_RETRIES = 3
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")
        
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set it in .env or environment.\n"
                "Get your free key at: https://console.groq.com/keys"
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self._last_call_time = 0.0
        
        from .prompts import SYSTEM_PROMPT, build_analysis_prompt
        self.system_prompt = SYSTEM_PROMPT
        self.build_prompt = build_analysis_prompt
        
        logger.info(f"GroqLLMClient initialized (model: {model})")
    
    def _call_groq(self, user_prompt: str) -> str:
        """Make a single Groq API call."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content.strip()
    
    def analyze(self, text: str, source: str = None) -> Dict[str, any]:
        """Analyze text with retry logic and detailed logging."""
        user_prompt = self.build_prompt(text, source)
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response_text = self._call_groq(user_prompt)
                
                # Log raw LLM response for debugging
                logger.info(f"[Groq raw] '{text[:50]}' -> {response_text[:120]}")
                
                # Clean markdown code blocks
                clean_text = response_text
                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_text:
                    clean_text = clean_text.split("```")[1].split("```")[0].strip()
                
                result_dict = json.loads(clean_text)
                validated = AgroSentimentResponse(**result_dict)
                
                final_sentiment = validated.sentiment
                final_confidence = validated.confidence
                
                # Rule: Very low confidence (< 0.3) -> NEUTRAL
                if final_confidence < 0.3:
                    final_sentiment = "NEUTRAL"
                
                analysis_result = {
                    "sentiment": final_sentiment,
                    "confidence": round(final_confidence, 2),
                    "commodity": validated.commodity
                }
                if validated.reasoning:
                    analysis_result["reasoning"] = validated.reasoning
                
                logger.info(f"[Groq OK] '{text[:40]}' -> {final_sentiment} ({final_confidence:.2f}) [{validated.commodity}]")
                return analysis_result
                
            except json.JSONDecodeError as e:
                logger.warning(f"[Groq attempt {attempt}/{self.MAX_RETRIES}] JSON parse error for '{text[:40]}': {e}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return {"sentiment": "NEUTRAL", "confidence": 0.0, "commodity": "GENERAL", "error": "json_parse_error"}
                
            except Exception as e:
                error_str = str(e)
                logger.warning(f"[Groq attempt {attempt}/{self.MAX_RETRIES}] Error for '{text[:40]}': {error_str[:100]}")
                
                # Check for rate limit errors specifically
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    wait_time = 60 if attempt == self.MAX_RETRIES else (5 * attempt)
                    logger.warning(f"Rate limit hit! Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                elif attempt < self.MAX_RETRIES:
                    time.sleep(2 ** attempt)
                
                if attempt == self.MAX_RETRIES:
                    logger.error(f"[Groq FAILED] All {self.MAX_RETRIES} attempts failed for '{text[:50]}': {error_str[:100]}")
                    return {"sentiment": "NEUTRAL", "confidence": 0.0, "commodity": "GENERAL", "error": "api_error"}
        
        return {"sentiment": "NEUTRAL", "confidence": 0.0, "commodity": "GENERAL", "error": "unknown"}


class MockLLMClient(BaseLLMClient):
    """
    Mock LLM client for development and testing without API calls.
    """
    
    def __init__(self, simulate_latency: bool = True, latency_seconds: float = 0.3):
        self.simulate_latency = simulate_latency
        self.latency_seconds = latency_seconds
        self.sentiments: list[SentimentType] = ["ALCISTA", "BAJISTA", "NEUTRAL"]
        logger.info("MockLLMClient initialized (simulated mode)")
    
    def analyze(self, text: str, source: str = None) -> Dict[str, any]:
        if self.simulate_latency:
            time.sleep(self.latency_seconds)
        
        sentiment = random.choice(self.sentiments)
        confidence = random.uniform(0.70, 0.95) if sentiment != "NEUTRAL" else random.uniform(0.80, 0.99)
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2)
        }


def get_llm_client(use_mock: bool = False) -> BaseLLMClient:
    """
    Factory function to get the appropriate LLM client.
    Tries Groq first, falls back to Mock.
    """
    if use_mock:
        return MockLLMClient()
    
    # Try Groq first (free tier)
    try:
        return GroqLLMClient()
    except (ValueError, ImportError) as e:
        logger.warning(f"Could not initialize GroqLLMClient: {e}")
    
    logger.warning("Falling back to MockLLMClient")
    return MockLLMClient()
