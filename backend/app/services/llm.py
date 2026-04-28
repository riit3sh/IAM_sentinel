import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

def get_llm():
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_key:
        print("[Info] Using openrouter/free dynamic model")
        return ChatOpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            model="openrouter/free",
            temperature=0
        )
        
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        return ChatOpenAI(model="gpt-4o", temperature=0)
    else:
        print("[Warning] No OpenAI API Key found. Falling back to local Ollama Llama3.")
        return ChatOllama(model="llama3", temperature=0)

def get_json_llm():
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_key:
        return ChatOpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            model="openrouter/free",
            temperature=0,
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        return ChatOpenAI(model="gpt-4o", temperature=0, model_kwargs={"response_format": {"type": "json_object"}})
    else:
        return ChatOllama(model="llama3", temperature=0, format="json")
