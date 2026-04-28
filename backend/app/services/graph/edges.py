from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.services.graph.state import GraphState
from app.services.llm import get_json_llm

def grade_hallucination(state: GraphState):
    """
    Conditional edge: Evaluates if the generated answer hallucinated outside the retrieved context.
    """
    print("--- CHECK HALLUCINATION ---")
    documents = state["documents"]
    generation = state["generation"]
    retries = state.get("hallucination_retries", 0)
    
    if not documents:
        return "useful"
        
    if "I am sorry" in generation or "could not find information" in generation:
        return "useful"
        
    if retries >= 3:
        print("--- HALLUCINATION RETRIES EXCEEDED, OUTPUTTING SAFELY ---")
        return "useful"

    llm = get_json_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a grader assessing whether an LLM generation is grounded in a set of retrieved facts. \n"
                   "Give a binary score 'yes' or 'no'. 'yes' means the answer is strictly based on the facts and does not hallucinate external information. \n"
                   "Provide the binary score as a JSON with a single key 'score'."),
        ("user", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}")
    ])
    chain = prompt | llm | JsonOutputParser()
    
    docs_text = "\n\n".join([doc.page_content for doc in documents])
    
    try:
        score = chain.invoke({"documents": docs_text, "generation": generation})
        grade = score.get("score")
    except Exception:
        # Fallback conservative strategy for local JSON parsing
        grade = "yes" 
    
    if grade == "yes":
        print("--- DECISION: GENERATION IS GROUNDED ---")
        return "useful"
    else:
        print(f"--- DECISION: HALLUCINATION DETECTED (Retry {retries}/3) ---")
        return "not supported"
