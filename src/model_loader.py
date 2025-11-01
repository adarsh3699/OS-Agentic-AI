"""
Multi-Model Loader with Automatic Fallback
Tries: Groq → Gemini → Local Ollama
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from src import config


def get_model():
    """
    Load AI model with automatic fallback.

    Order:
    1. Groq (llama-3.3-70b) - Fast, powerful, free
    2. Gemini (2.0-flash-exp) - Google, reliable
    3. Ollama (llama3.1:8b) - Local backup

    Returns:
        LLM instance ready to use
    """
    errors = []

    for provider in config.FALLBACK_ORDER:
        try:
            if provider == "groq":
                print("🚀 Loading: Groq Llama 3.3 70B...")
                return _load_groq()

            elif provider == "gemini":
                print("🔷 Loading: Google Gemini 2.0 Flash...")
                return _load_gemini()

            elif provider == "ollama":
                print("🏠 Loading: Local Llama 3.1 8B...")
                return _load_ollama()

        except Exception as e:
            error_msg = f"{provider.upper()}: {str(e)}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg}")
            continue

    # If all fail, show errors and use local as last resort
    print("\n❌ All API providers failed!")
    for error in errors:
        print(f"   - {error}")
    print("\n🏠 Using local Ollama (limited capability)...\n")
    return ChatOllama(model=config.LOCAL_MODEL)


def _load_groq():
    """Load Groq model"""
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")

    llm = ChatGroq(
        model=config.GROQ_MODEL,
        api_key=config.GROQ_API_KEY,
        temperature=0.1,  # Lower = more focused
    )

    # Test connection
    llm.invoke("test")

    print(f"✅ {config.MODEL_INFO['groq']['name']}")
    print(f"   Speed: {config.MODEL_INFO['groq']['speed']}")
    print(f"   Reasoning: {config.MODEL_INFO['groq']['reasoning']}")
    print(f"   Cost: {config.MODEL_INFO['groq']['cost']}\n")

    return llm


def _load_gemini():
    """Load Gemini model"""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")

    llm = ChatGoogleGenerativeAI(
        model=config.GEMINI_MODEL,
        google_api_key=config.GEMINI_API_KEY,
        temperature=0.1,
    )

    # Test connection
    llm.invoke("test")

    print(f"✅ {config.MODEL_INFO['gemini']['name']}")
    print(f"   Speed: {config.MODEL_INFO['gemini']['speed']}")
    print(f"   Reasoning: {config.MODEL_INFO['gemini']['reasoning']}")
    print(f"   Cost: {config.MODEL_INFO['gemini']['cost']}\n")

    return llm


def _load_ollama():
    """Load local Ollama model"""
    llm = ChatOllama(model=config.LOCAL_MODEL)

    print(f"✅ {config.MODEL_INFO['ollama']['name']}")
    print(f"   Speed: {config.MODEL_INFO['ollama']['speed']}")
    print(f"   Reasoning: {config.MODEL_INFO['ollama']['reasoning']}")
    print(f"   Cost: {config.MODEL_INFO['ollama']['cost']}")
    print("   ⚠️  Note: Limited capability for complex tasks\n")

    return llm
