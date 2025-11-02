"""
AI Model Configuration - OPTIMIZED FOR COST EFFICIENCY
Intelligent model selection based on task complexity

Copy this file to config.py and add your API keys
"""

# ============================================================================
# API KEYS
# ============================================================================

GROQ_API_KEY = ""  # Get from: console.groq.com
GEMINI_API_KEY = ""  # Get from: makersuite.google.com


# ============================================================================
# INTELLIGENT MODEL TIERS (Auto-select based on task complexity)
# ============================================================================

MODEL_TIERS = {
    # Small/Fast - Simple tasks (file listing, basic commands)
    "small": {
        "groq": "llama-3.1-8b-instant",  # Ultra-fast, 30/min
        "gemini": "gemini-2.0-flash",  # ✅ WORKS with tools! 200 RPD
        "ollama": "llama3.1:8b",  # 🏆 Meta's best 8B - PROPER function calling (4.9 GB)
        "use_for": ["list", "check", "simple_command"],
    },
    # Medium - Standard tasks (file organization, multi-step)
    "medium": {
        "groq": "llama-3.3-70b-versatile",  # Best model, 30/min (prioritize!)
        "gemini": "gemini-2.0-flash",  # ✅ ACTUALLY USES TOOLS! 200 RPD
        "ollama": "llama3.1:8b",  # 🏆 Trained for tool calling - reliable (4.9 GB)
        "use_for": ["organize", "move", "create", "verify"],
    },
    # Large - Complex reasoning (debugging, error recovery)
    "large": {
        "groq": "llama-3.3-70b-versatile",  # Most capable, 30/min
        "gemini": "gemini-2.0-flash",  # ✅ Tool calling works! 200 RPD
        "ollama": "llama3.1:8b",  # 🏆 Best local model - excellent reasoning (4.9 GB)
        "use_for": ["debug", "complex", "multi_tool"],
    },
}

# Default tier for unknown tasks
DEFAULT_TIER = "medium"


# ============================================================================
# COST OPTIMIZATION SETTINGS
# ============================================================================

# Enable intelligent model selection (use smaller models when possible)
ENABLE_SMART_SELECTION = True

# Enable response caching (avoid duplicate API calls)
ENABLE_CACHING = True
CACHE_TTL_SECONDS = 300  # 5 minutes

# Maximum tokens per request (prevent excessive costs)
MAX_TOKENS_PER_REQUEST = 2000

# Rate limiting (requests per minute)
RATE_LIMITS = {
    "groq": 30,  # Free tier: 30 req/min, 100k tokens/day
    "gemini": 15,  # Free tier: 15 req/min, 200 req/day (gemini-2.0-flash)
    "ollama": 999,  # No limit (local)
}


# ============================================================================
# FALLBACK STRATEGY
# ============================================================================

FALLBACK_ORDER = [
    "groq",  # Primary: Fastest free tier (when available)
    "gemini",  # Fallback: Gemini 2.0 Flash - WORKS with tools! ✅
    "ollama",  # Last resort: LOCAL - Always works! (Qwen 2.5 14B)
]


# ============================================================================
# MODEL CAPABILITIES & COSTS
# ============================================================================

MODEL_INFO = {
    "groq": {
        "name": "Groq Llama 3.3 70B",
        "speed": "⚡⚡⚡⚡",
        "reasoning": "⭐⭐⭐⭐⭐",
        "cost": "FREE (30 req/min, 100k tokens/day)",
        "rpm": 30,  # Requests per minute
    },
    "gemini": {
        "name": "Google Gemini 2.0 Flash",
        "speed": "⚡⚡⚡⚡",
        "reasoning": "⭐⭐⭐⭐⭐",
        "cost": "FREE (15 req/min, 200 req/day)",
        "rpm": 15,  # 2.0 - Actually works with tool calling! ✅
    },
    "ollama": {
        "name": "Local Llama 3.1 8B",
        "speed": "⚡⚡⚡⚡",
        "reasoning": "⭐⭐⭐⭐⭐",
        "cost": "FREE (offline, unlimited)",
        "rpm": 999,
    },
}


# ============================================================================
# PROMPT OPTIMIZATION
# ============================================================================

# Use compressed prompts (fewer tokens = lower cost)
USE_COMPRESSED_PROMPTS = True

# Remove verbose examples from system prompt
MINIMAL_PROMPTS = True
