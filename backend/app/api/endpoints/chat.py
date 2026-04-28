from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.graph.workflow import compile_workflow

router = APIRouter()
# We compile the graph once when the router starts
workflow = compile_workflow()

class ChatRequest(BaseModel):
    message: str

class Citation(BaseModel):
    page_number: int
    section_title: str
    text_preview: str

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation]
    retries_used: int

@router.post("/", response_model=ChatResponse)
def generate_chat_response(request: ChatRequest):
    try:
        initial_state = {
            "query": request.message,
            "documents": [],
            "generation": "",
            "hallucination_retries": 0
        }
        
        # Stream the graph execution synchronously
        final_state = workflow.invoke(initial_state)
        
        # Serialize the extracted metadata into Citation objects
        citations = []
        for doc in final_state.get("documents", []):
            citations.append(Citation(
                page_number=doc.metadata.get("page_number", 0),
                section_title=doc.metadata.get("section_title", "Unknown"),
                text_preview=doc.page_content[:150]
            ))
            
        return ChatResponse(
            response=final_state.get("generation", "Error generating response."),
            citations=citations,
            retries_used=final_state.get("hallucination_retries", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LangGraph execution failed: {str(e)}")
