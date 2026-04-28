from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from app.services.llm import get_llm, get_json_llm
from app.services.hybrid_retriever import HybridRetriever
from app.services.qdrant_store import get_vector_store
from app.services.reranker import DocumentReranker
from app.services.graph.state import GraphState

def retrieve_node(state: GraphState):
    print("--- RETRIEVE ---")
    query = state["query"]
    
    qdrant = get_vector_store()
    retriever = qdrant.as_retriever(search_kwargs={"k": 10})
    hybrid = HybridRetriever(qdrant_retriever=retriever)
    docs = hybrid.get_relevant_documents(query)
    
    # Skip memory-heavy reranker for Render deployment
    # Just take the top 3 highest scored docs from the Hybrid Retriever
    reranked_docs = docs[:3]
    
    return {"documents": reranked_docs, "query": query, "hallucination_retries": state.get("hallucination_retries", 0)}

def grade_docs_node(state: GraphState):
    print("--- GRADE DOCUMENTS ---")
    query = state["query"]
    documents = state["documents"]
    
    llm = get_json_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a grader assessing relevance of a retrieved document to a user question. "
                   "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. "
                   "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.\n"
                   "Provide the binary score as a JSON with a single key 'score' and no preamble or explanation."),
        ("user", "Question: {query}\n\nDocument: {document}")
    ])
    chain = prompt | llm | JsonOutputParser()
    
    filtered_docs = []
    for doc in documents:
        try:
            score = chain.invoke({"query": query, "document": doc.page_content})
            if score.get("score") == "yes":
                filtered_docs.append(doc)
        except Exception as e:
            # Output parser fails generally mean local model hallucinated the json format, include conservatively
            filtered_docs.append(doc)
            
    if not filtered_docs:
        print("--- ALL DOCUMENTS IRRELEVANT ---")
    
    return {"documents": filtered_docs, "query": query}

def generate_node(state: GraphState):
    print("--- GENERATE ANSWER ---")
    query = state["query"]
    documents = state["documents"]
    retries = state.get("hallucination_retries", 0)
    
    if not documents:
        return {"generation": "I am sorry, but I could not find information regarding your query strictly inside the AWS IAM User Guide.", "query": query}

    # Format documents with mandatory citations
    context = ""
    for idx, doc in enumerate(documents):
        page = doc.metadata.get('page_number', 'Unknown')
        section = doc.metadata.get('section_title', 'Unknown')
        context += f"--- Document Ref [{idx+1}] (Page {page}, Section: {section}) ---\n{doc.page_content}\n\n"

    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AWS IAM Sentinel. "
                   "Answer the user's question using ONLY the provided retrieved context. "
                   "Do not hallucinate external commands. Be concise. "
                   "CRITICAL REQUIREMENT: For every fact or sentence you output, you MUST append an inline citation referencing the page number, exactly formatted as [Page X, Section Y].\n\n"
                   "Context:\n{context}"),
        ("user", "Question: {query}")
    ])
    chain = prompt | llm | StrOutputParser()
    generation = chain.invoke({"context": context, "query": query})
    
    return {"documents": documents, "query": query, "generation": generation, "hallucination_retries": retries + 1}
