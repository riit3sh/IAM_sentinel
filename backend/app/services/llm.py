import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

def get_llm():
    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key:
        # A cascade of reliable models hosted specifically on Groq
        models = [
            os.getenv("GROQ_MODEL", "llama3-8b-8192"),
            "llama3-70b-8192",
            "mixtral-8x7b-32768"
        ]
        
        print(f"[Info] Initializing Groq LLM chain with fallbacks. Primary: {models[0]}")
        
        llm_instances = [
            ChatOpenAI(
                api_key=groq_key,
                base_url="https://api.groq.com/openai/v1",
                model=m,
                temperature=0.2
            )
            for m in models
        ]
        
        return llm_instances[0].with_fallbacks(llm_instances[1:])
        
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        return ChatOpenAI(model="gpt-4o", temperature=0.2)
    else:
        print("[Warning] No API Keys found. Falling back to local Ollama Llama3.")
        return ChatOllama(model="llama3", temperature=0.2)

def get_json_llm():
    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key:
        models = [
            os.getenv("GROQ_MODEL", "llama3-8b-8192"),
            "llama3-70b-8192",
            "mixtral-8x7b-32768"
        ]
        
        llm_instances = [
            ChatOpenAI(
                api_key=groq_key,
                base_url="https://api.groq.com/openai/v1",
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


