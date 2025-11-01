"""
AI Model Configuration - Example Template
Copy this file to config.py and add your API keys
"""

# ============================================================================
# API KEYS
# ============================================================================

GROQ_API_KEY = ""  # Get from: console.groq.com
GEMINI_API_KEY = ""  # Get from: makersuite.google.com


# ============================================================================
# MODEL SELECTION
# ============================================================================

# Primary: Groq (Fast, free, powerful)
GROQ_MODEL = "llama-3.3-70b-versatile"  # Best reasoning model

# Fallback: Gemini (Google, reliable)
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Latest experimental model

# Final Fallback: Local Ollama
LOCAL_MODEL = "llama3.1:8b"  # Offline backup


# ============================================================================
# FALLBACK STRATEGY
# ============================================================================

FALLBACK_ORDER = [
    "groq",  # Try Groq first (fastest, most capable)
    "gemini",  # Fall back to Gemini
    "ollama",  # Final fallback to local
]


# ============================================================================
# MODEL CAPABILITIES
# ============================================================================

MODEL_INFO = {
    "groq": {
        "name": "Groq Llama 3.3 70B",
        "speed": "⚡⚡⚡⚡",
        "reasoning": "⭐⭐⭐⭐⭐",
        "cost": "FREE (30 req/min)",
    },
    "gemini": {
        "name": "Google Gemini 2.0 Flash",
        "speed": "⚡⚡⚡",
        "reasoning": "⭐⭐⭐⭐⭐",
        "cost": "FREE (15 req/min)",
    },
    "ollama": {
        "name": "Local Llama 3.1 8B",
        "speed": "⚡⚡",
        "reasoning": "⭐⭐",
        "cost": "FREE (offline)",
    },
}

