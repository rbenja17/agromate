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


class GroqLLMClient(BaseLLMClient):
    """
    Real LLM client using Groq API (FREE TIER).
    
    Uses llama-3.1-70b-versatile for high-quality sentiment analysis.
    Free tier: 30 requests per minute, 14,400 per day.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the Groq LLM client.
        
        Args:
            api_key: Groq API key. If not provided, reads from GROQ_API_KEY env var.
            model: Model to use (default: llama-3.1-70b-versatile)
            
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        try:
            from groq import Groq
        except ImportError:
            raise ImportError(
                "groq package not installed. Run: pip install groq"
            )
        
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file:\n"
                "GROQ_API_KEY=your_api_key_here\n\n"
                "Get your free API key at: https://console.groq.com/keys"
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        
        # Import prompts
        from .prompts import SYSTEM_PROMPT, build_analysis_prompt
        self.system_prompt = SYSTEM_PROMPT
        self.build_prompt = build_analysis_prompt
        
        logger.info(f"GroqLLMClient initialized (model: {model} - FREE TIER)")
    
    def analyze(self, text: str, source: str = None) -> Dict[str, any]:
        """
        Analyze text and return sentiment classification using Groq.
        
        Args:
            text: The text to analyze (news headline)
            source: Optional source of the news
            
        Returns:
            Dictionary with 'sentiment', 'confidence', and optionally 'reasoning'
        """
        try:
            user_prompt = self.build_prompt(text, source)
            
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
            
            response_text = response.choices[0].message.content.strip()
            result = json.loads(response_text)
            
            # Validate and normalize
            sentiment = result.get("sentiment", "NEUTRAL").upper()
            if sentiment not in ["ALCISTA", "BAJISTA", "NEUTRAL"]:
                sentiment = "NEUTRAL"
            
            confidence = float(result.get("confidence", 0.5))
            confidence = max(0.0, min(1.0, confidence))
            
            # Validate and normalize commodity
            commodity = result.get("commodity", "GENERAL").upper()
            valid_commodities = ["SOJA", "MAÍZ", "TRIGO", "GIRASOL", "CEBADA", "SORGO", "GENERAL"]
            if commodity not in valid_commodities:
                commodity = "GENERAL"
            
            analysis_result = {
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "commodity": commodity
            }
            
            if "reasoning" in result:
                analysis_result["reasoning"] = result["reasoning"]
            
            logger.debug(f"Groq analysis: '{text[:50]}...' -> {analysis_result}")
            
            return analysis_result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {e}")
            return {"sentiment": "NEUTRAL", "confidence": 0.5, "error": "parse_error"}
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise RuntimeError(f"Groq API call failed: {e}")


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
