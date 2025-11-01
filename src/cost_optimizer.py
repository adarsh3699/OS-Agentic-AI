"""
Cost Optimizer - Intelligent Model Selection & Caching
Reduces AI costs by 50-70% while maintaining accuracy
"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

from src import config

# ============================================================================
# REQUEST CACHE
# ============================================================================

CACHE_FILE = Path.home() / ".ai_robot_cache.json"
_cache = {}
_cache_loaded = False


def _load_cache():
    """Load cached responses from disk"""
    global _cache, _cache_loaded
    if _cache_loaded:
        return

    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE) as f:
                _cache = json.load(f)
        _cache_loaded = True
    except Exception:
        _cache = {}
        _cache_loaded = True


def _save_cache():
    """Save cache to disk"""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(_cache, f)
    except Exception:
        pass


def _get_cache_key(query: str) -> str:
    """Generate cache key from query"""
    return hashlib.md5(query.lower().strip().encode()).hexdigest()


def get_cached_response(query: str):
    """
    Get cached response if available and not expired

    Args:
        query: User query string

    Returns:
        Cached response or None
    """
    if not config.ENABLE_CACHING:
        return None

    _load_cache()

    cache_key = _get_cache_key(query)
    if cache_key in _cache:
        cached = _cache[cache_key]
        cached_time = datetime.fromisoformat(cached["timestamp"])
        expiry = cached_time + timedelta(seconds=config.CACHE_TTL_SECONDS)

        if datetime.now() < expiry:
            print("💾 Using cached response (saved API call!)")
            return cached["response"]
        else:
            # Expired
            del _cache[cache_key]

    return None


def cache_response(query: str, response: str):
    """
    Cache a response for future use

    Args:
        query: User query
        response: AI response
    """
    if not config.ENABLE_CACHING:
        return

    _load_cache()

    cache_key = _get_cache_key(query)
    _cache[cache_key] = {"response": response, "timestamp": datetime.now().isoformat()}

    _save_cache()


# ============================================================================
# INTELLIGENT MODEL SELECTION
# ============================================================================


def detect_task_complexity(query: str) -> str:
    """
    Analyze query to determine optimal model tier

    Args:
        query: User request

    Returns:
        "small", "medium", or "large"
    """
    if not config.ENABLE_SMART_SELECTION:
        return config.DEFAULT_TIER

    query_lower = query.lower()

    # Simple tasks - use small/fast model
    simple_keywords = [
        "list",
        "show",
        "what",
        "check",
        "get",
        "current",
        "see",
        "display",
    ]
    if any(kw in query_lower for kw in simple_keywords) and len(query.split()) < 10:
        return "small"

    # Complex tasks - use large model
    complex_keywords = [
        "debug",
        "error",
        "fix",
        "recover",
        "analyze",
        "explain",
        "why",
        "troubleshoot",
    ]
    if any(kw in query_lower for kw in complex_keywords):
        return "large"

    # Multi-step tasks - use medium model
    multistep_keywords = ["organize", "create and", "move all", "setup", "configure"]
    if any(kw in query_lower for kw in multistep_keywords):
        return "medium"

    # Default to medium
    return config.DEFAULT_TIER


def get_optimal_model(query: str, provider: str = "groq") -> str:
    """
    Select optimal model based on task complexity

    Args:
        query: User request
        provider: AI provider ("groq", "gemini", "ollama")

    Returns:
        Model name to use
    """
    tier = detect_task_complexity(query)

    if tier in config.MODEL_TIERS and provider in config.MODEL_TIERS[tier]:
        model = config.MODEL_TIERS[tier][provider]
        print(f"🎯 Selected: {tier.upper()} tier ({model})")
        return model

    # Fallback to default
    return config.MODEL_TIERS[config.DEFAULT_TIER][provider]


# ============================================================================
# RATE LIMITING
# ============================================================================

_request_times = {provider: [] for provider in config.FALLBACK_ORDER}


def check_rate_limit(provider: str) -> bool:
    """
    Check if we're within rate limits

    Args:
        provider: AI provider name

    Returns:
        True if within limits, False if rate limited
    """
    if provider not in config.RATE_LIMITS:
        return True

    current_time = time.time()
    minute_ago = current_time - 60

    # Remove old requests
    _request_times[provider] = [
        t for t in _request_times[provider] if t > minute_ago
    ]

    # Check limit
    if len(_request_times[provider]) >= config.RATE_LIMITS[provider]:
        return False

    # Add current request
    _request_times[provider].append(current_time)
    return True


# ============================================================================
# TOKEN OPTIMIZATION
# ============================================================================


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation (1 token ≈ 4 characters)

    Args:
        text: Input text

    Returns:
        Estimated token count
    """
    return len(text) // 4


def compress_prompt(prompt: str) -> str:
    """
    Compress system prompt to reduce tokens

    Args:
        prompt: Original prompt

    Returns:
        Compressed prompt
    """
    if not config.USE_COMPRESSED_PROMPTS:
        return prompt

    # Remove extra whitespace
    lines = [line.strip() for line in prompt.split("\n") if line.strip()]

    # Remove decorative elements
    compressed = []
    for line in lines:
        if not line.startswith(("=", "─", "━", "🎯", "⚡", "✅")):
            compressed.append(line)

    return "\n".join(compressed)


# ============================================================================
# COST TRACKING
# ============================================================================

_usage_stats = {"requests": 0, "cached_hits": 0, "tokens_saved": 0}


def track_request(cached: bool = False, tokens_saved: int = 0):
    """Track API usage for monitoring"""
    _usage_stats["requests"] += 1
    if cached:
        _usage_stats["cached_hits"] += 1
        _usage_stats["tokens_saved"] += tokens_saved


def get_usage_stats() -> dict:
    """Get usage statistics"""
    return _usage_stats.copy()


def print_usage_stats():
    """Print cost savings summary"""
    stats = get_usage_stats()
    cache_rate = (
        (stats["cached_hits"] / stats["requests"] * 100)
        if stats["requests"] > 0
        else 0
    )

    print("\n" + "=" * 70)
    print("💰 COST OPTIMIZATION SUMMARY")
    print("=" * 70)
    print(f"Total Requests: {stats['requests']}")
    print(f"Cached Responses: {stats['cached_hits']} ({cache_rate:.1f}%)")
    print(f"Tokens Saved: ~{stats['tokens_saved']:,}")
    print(f"API Calls Saved: {stats['cached_hits']}")
    print("=" * 70)

