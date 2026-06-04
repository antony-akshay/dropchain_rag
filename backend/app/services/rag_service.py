from typing import Dict, Any
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.utils.text_splitter import get_splitter
from app.services.vectorstore import create_vectorstore, load_vectorstore
from app.config import GROQ_MODEL, GROQ_API_KEY

llm = ChatGroq(
    model=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0
)

rag_prompt = ChatPromptTemplate.from_template(
    '''
You are a document question-answering assistant.

Use ONLY the provided context to answer the user's question.

Rules:
- Do not use outside knowledge.
- Do not guess.
- If the answer cannot be found in the context, respond exactly:
  "I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer:
'''
)

def format_docs(docs) -> str:
    return "\n\n---\n\n".join(d.page_content for d in docs)

def ingest_document(file_path: str) -> int:
    """Ingests a document from the provided path, embeds its chunks, and returns chunk count."""
    loader = TextLoader(file_path)
    docs = loader.load()

    splitter = get_splitter()
    chunks = splitter.split_documents(docs)

    create_vectorstore(chunks)

    # Return the actual number of chunks we fed to creating the vectorstore
    # The Vectorstore creation filters some tiny chunks out.
    valid_chunks = [c for c in chunks if len(c.page_content.strip()) > 30]
    return len(valid_chunks)

def answer_question(query: str) -> Dict[str, Any]:
    """Retrieves relevant context & formats response using Groq."""
    vectorstore = load_vectorstore()
    docs = vectorstore.similarity_search(query, k=6)

    context = format_docs(docs)

    messages = rag_prompt.format(
        context=context,
        question=query
    )

    response = llm.invoke(messages)

    return {
        "answer": response.content,
        "sources": [d.page_content for d in docs]
    }
