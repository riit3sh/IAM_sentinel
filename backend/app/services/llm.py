import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

def get_llm():
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_key:
        # A cascade of reliable free models to handle token exhaustion gracefully
        models = [
            os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash:free"),
            "meta-llama/llama-3.1-8b-instruct:free",
            "meta-llama/llama-3.1-70b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "openrouter/free"
        ]
        
        print(f"[Info] Initializing LLM chain with fallbacks. Primary: {models[0]}")
        
        llm_instances = [
            ChatOpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
                model=m,
                temperature=0.2
            )
            for m in models
        ]
        
        # Returns the primary model with a built-in fallback chain
        return llm_instances[0].with_fallbacks(llm_instances[1:])
        
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        return ChatOpenAI(model="gpt-4o", temperature=0.2)
    else:
        print("[Warning] No OpenAI API Key found. Falling back to local Ollama Llama3.")
        return ChatOllama(model="llama3", temperature=0.2)

def get_json_llm():
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_key:
        models = [
            os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash:free"),
            "meta-llama/llama-3.1-8b-instruct:free",
            "meta-llama/llama-3.1-70b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "openrouter/free"
        ]
        
        llm_instances = [
            ChatOpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
                model=m,
                temperature=0,
                model_kwargs={"response_format": {"type": "json_object"}}
            )
            for m in models
        ]
        
        return llm_instances[0].with_fallbacks(llm_instances[1:])
        
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        return ChatOpenAI(model="gpt-4o", temperature=0, model_kwargs={"response_format": {"type": "json_object"}})
    else:
        return ChatOllama(model="llama3", temperature=0, format="json")


