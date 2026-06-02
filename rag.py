import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq

load_dotenv()

DOC_PATH = "./document.txt"
PERSIST_DIR = "./chroma_db"

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

llm = ChatGroq(
    model="groq/compound-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a strict enterprise document assistant.

RULES:
- Answer ONLY using the provided context.
- If the answer is not in the context, say:
  "I don't know based on the provided document."
- Do not guess.
- Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
""")
#load doc
def load_document():
    loader = TextLoader(DOC_PATH)
    return loader.load()
    
def get_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=[
            "\n\n",      # paragraphs (highest priority)
            "\n",        # line breaks
            ". ",        # sentences
            " ",         # fallback
            ""           # last resort
        ]
    )

def build_vectorstore():
    docs = load_document()

    splitter = get_splitter()
    chunks = splitter.split_documents(docs)

    # filter tiny noise chunks
    chunks = [c for c in chunks if len(c.page_content.strip()) > 30]

    print(f"\nLoaded document → {len(chunks)} chunks")

    # rebuild fresh DB always for correctness
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    return vectorstore

def load_vectorstore():
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

def format_docs(docs):
    return "\n\n---\n\n".join(d.page_content for d in docs)

def main():

    if os.path.exists(PERSIST_DIR):
        print("Loading existing vector DB...")
        vectorstore = load_vectorstore()
    else:
        print("Building vector DB...")
        vectorstore = build_vectorstore()

    print("\nMini Contextual AI Assistant Ready\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            break
            
        docs = vectorstore.similarity_search(query, k=6)

        print("\n--- Retrieved Chunks ---")
        for i, d in enumerate(docs):
            print(f"\n[Chunk {i}]")
            print(d.page_content[:300])

        context = format_docs(docs)
        
        messages = prompt.format(
            context=context,
            question=query
        )

        response = llm.invoke(messages)

        print("\nAssistant:", response.content, "\n")


if __name__ == "__main__":
    main()
