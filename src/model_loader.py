"""
Multi-Model Loader - COST OPTIMIZED
Intelligent model selection based on task complexity
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from src import config, cost_optimizer


def get_model(query: str = ""):
    """
    Load AI model with intelligent selection and fallback.

    Automatically selects optimal model tier based on task:
    - Simple tasks → Small/Fast model (saves cost)
    - Standard tasks → Medium model (balanced)
    - Complex tasks → Large model (best reasoning)

    Args:
        query: User query (for intelligent selection)

    Returns:
        LLM instance ready to use
    """
    errors = []

    for provider in config.FALLBACK_ORDER:
        # Check rate limits
        if not cost_optimizer.check_rate_limit(provider):
            print(f"⏱️  Rate limit reached for {provider}, trying next...")
            continue

        try:
            if provider == "groq":
                print("🚀 Loading: Groq...")
                return _load_groq(query)

            elif provider == "gemini":
                print("🔷 Loading: Gemini...")
                return _load_gemini(query)

            elif provider == "ollama":
                print("🏠 Loading: Local Ollama...")
                return _load_ollama()

        except Exception as e:
            error_msg = f"{provider.upper()}: {str(e)}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg}")
            continue

    # If all fail, use local as last resort
    print("\n❌ All API providers failed!")
    for error in errors:
        print(f"   - {error}")
    print("\n🏠 Using local Ollama (limited capability)...\n")
    return ChatOllama(model=config.MODEL_TIERS[config.DEFAULT_TIER]["ollama"])


def _load_groq(query: str = ""):
    """Load Groq with intelligent model selection"""
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")

    # Select optimal model based on task
    model = cost_optimizer.get_optimal_model(query, "groq")

    llm = ChatGroq(
        model=model,
        api_key=config.GROQ_API_KEY,
        temperature=0.1,
        max_tokens=config.MAX_TOKENS_PER_REQUEST,
    )

    # Test connection
    llm.invoke("test")

    print(f"✅ {config.MODEL_INFO['groq']['name']}")
    print(f"   Model: {model}")
    print(f"   Speed: {config.MODEL_INFO['groq']['speed']}")
    print(f"   Cost: {config.MODEL_INFO['groq']['cost']}")
    if config.ENABLE_CACHING:
        print("   💾 Caching: ENABLED")
    print()

    return llm


def _load_gemini(query: str = ""):
    """Load Gemini with intelligent model selection"""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")

    # Select optimal model
    model = cost_optimizer.get_optimal_model(query, "gemini")

    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=config.GEMINI_API_KEY,
        temperature=0.1,
        max_tokens=config.MAX_TOKENS_PER_REQUEST,
    )

    # Test connection
    llm.invoke("test")

    print(f"✅ {config.MODEL_INFO['gemini']['name']}")
    print(f"   Model: {model}")
    print(f"   Speed: {config.MODEL_INFO['gemini']['speed']}")
    print(f"   Cost: {config.MODEL_INFO['gemini']['cost']}")
    if config.ENABLE_CACHING:
        print("   💾 Caching: ENABLED")
    print()

    return llm


def _load_ollama():
    """Load local Ollama"""
    model = config.MODEL_TIERS[config.DEFAULT_TIER]["ollama"]
    llm = ChatOllama(model=model)

    print(f"✅ {config.MODEL_INFO['ollama']['name']}")
    print(f"   Model: {model}")
    print(f"   Speed: {config.MODEL_INFO['ollama']['speed']}")
    print(f"   Cost: {config.MODEL_INFO['ollama']['cost']}")
    print("   ⚠️  Limited capability for complex tasks\n")

    return llm
