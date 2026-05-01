from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Lazy-load the workflow to avoid blocking server startup
_workflow = None
def get_workflow():
    global _workflow
    if _workflow is None:
        from app.services.graph.workflow import compile_workflow
        _workflow = compile_workflow()
    return _workflow

class ChatRequest(BaseModel):
    message: str

class Citation(BaseModel):
    page_number: str
    section_title: str
    text_preview: str

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation]
    retries_used: int

_CHAT_CACHE = {}

@router.post("", response_model=ChatResponse)
def generate_chat_response(request: ChatRequest):
    query = request.message.strip()
    
    # Return instantly if repeated predefined question
    if query in _CHAT_CACHE:
        print(f"⚡ Serving cached response for: '{query}'")
        return _CHAT_CACHE[query]
        
    try:
        initial_state = {
            "query": query,
            "documents": [],
            "generation": "",
            "hallucination_retries": 0
        }
        
        # Stream the graph execution synchronously
        final_state = get_workflow().invoke(initial_state)
        
        # Serialize the extracted metadata into Citation objects
        citations = []
        for doc in final_state.get("documents", []):
            citations.append(Citation(
                page_number=str(doc.metadata.get("page_number", "Unknown")),
                section_title=doc.metadata.get("section_title", "Unknown"),
                text_preview=doc.page_content[:150]
            ))
            
        res = ChatResponse(
            response=final_state.get("generation", "Error generating response."),
            citations=citations,
            retries_used=final_state.get("hallucination_retries", 0)
        )
        
        # Cache answer
        _CHAT_CACHE[query] = res
        return res

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LangGraph execution failed: {str(e)}")
