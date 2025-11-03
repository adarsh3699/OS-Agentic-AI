"""
Dynamic Model Switcher - OPTIMIZED & CONSOLIDATED
Auto-switches on rate limit errors. All model loading logic in one place.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from src import config, cost_optimizer

# ============================================================================
# PROVIDER CONFIGURATION
# ============================================================================

PROVIDER_CONFIG = {
    "groq": {
        "icon": "🚀",
        "name": "Groq",
        "loader": lambda model: ChatGroq(
            model=model,
            api_key=config.GROQ_API_KEY,
            temperature=0.1,
            max_tokens=config.MAX_TOKENS_PER_REQUEST,
        ),
        "requires_api_key": True,
        "api_key": lambda: config.GROQ_API_KEY,
    },
    "gemini": {
        "icon": "🔷",
        "name": "Gemini",
        "loader": lambda model: ChatGoogleGenerativeAI(
            model=model,
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.1,
            max_tokens=config.MAX_TOKENS_PER_REQUEST,
        ),
        "requires_api_key": True,
        "api_key": lambda: config.GEMINI_API_KEY,
    },
    "ollama": {
        "icon": "🏠",
        "name": "Local Ollama",
        "loader": lambda model: ChatOllama(
            model=model,
            temperature=0.1,  # Slightly higher for better creativity in tool calling
            num_predict=512,  # More tokens for complex tasks
            top_p=0.9,  # More focused sampling
            repeat_penalty=1.15,  # Stronger penalty to prevent loops
            num_ctx=4096,  # Larger context window for better reasoning
            # NO format="json" - this breaks LangChain tool calling!
        ),
        "requires_api_key": False,
        "api_key": lambda: None,
    },
}


# ============================================================================
# DYNAMIC MODEL SWITCHER
# ============================================================================


class DynamicModelSwitcher:
    """
    Intelligent model switcher with automatic fallback on rate limit errors.
    Consolidated loading logic for all providers.
    """

    def __init__(self):
        self.current_provider = None
        self.failed_providers = []
        self.model = None

    def get_model(self, query: str = ""):
        """Load initial model with intelligent selection"""
        for provider in config.FALLBACK_ORDER:
            if not cost_optimizer.check_rate_limit(provider):
                print(f"⏱️  Rate limit reached for {provider}, trying next...")
                continue

            model = self._try_load_provider(provider, query)
            if model:
                return model

        # Last resort: local Ollama
        return self._load_fallback()

    def switch_provider(self, error_msg: str = ""):
        """Switch to next available provider on error"""
        print(f"\n⚠️  Provider {self.current_provider.upper()} failed: {error_msg}")
        print("🔄 Switching to next provider...")

        if self.current_provider not in self.failed_providers:
            self.failed_providers.append(self.current_provider)

        for provider in config.FALLBACK_ORDER:
            if provider in self.failed_providers:
                continue

            model = self._try_load_provider(provider, "", switching=True)
            if model:
                print(f"✅ Successfully switched to {PROVIDER_CONFIG[provider]['name']}!")
                return model

        # All exhausted
        return self._load_fallback()

    def _try_load_provider(self, provider: str, query: str = "", switching: bool = False):
        """Try to load a specific provider"""
        try:
            config_data = PROVIDER_CONFIG[provider]
            action = "Switching to" if switching else "Loading"
            print(f"{config_data['icon']} {action}: {config_data['name']}...")

            # Check API key if required
            if config_data["requires_api_key"] and not config_data["api_key"]():
                raise ValueError(f"{provider.upper()}_API_KEY not set")

            # Get optimal model for this provider
            model_name = cost_optimizer.get_optimal_model(query, provider)

            # Load model using provider-specific loader
            llm = config_data["loader"](model_name)

            # Test connection
            llm.invoke("test")

            # Print success info
            self._print_model_info(provider, model_name)

            # Update state
            self.model = llm
            self.current_provider = provider
            return llm

        except Exception as e:
            print(f"⚠️  {provider.upper()} failed: {e}")
            if provider not in self.failed_providers:
                self.failed_providers.append(provider)
            return None

    def _load_fallback(self):
        """Load local Ollama as final fallback"""
        print("\n❌ All providers exhausted! Using local Ollama...")
        model = config.MODEL_TIERS[config.DEFAULT_TIER]["ollama"]
        self.model = ChatOllama(model=model)
        self.current_provider = "ollama"
        self._print_model_info("ollama", model)
        return self.model

    def _print_model_info(self, provider: str, model: str):
        """Print model information (DRY)"""
        info = config.MODEL_INFO[provider]
        print(f"✅ {info['name']}")
        print(f"   Model: {model}")
        print(f"   Cost: {info['cost']}")

        if config.ENABLE_CACHING and provider != "ollama":
            print("   💾 Caching: ENABLED")

        if provider == "ollama":
            print("   ⚠️  Limited capability for complex tasks")

        print()
