# AI Prompts

## Workspace Link

https://excalidraw.com/#json=_3Q0WyTKb0tzFHYWcdL27,1tn20U54hPouTGY2lRS1CA

1. set up a fastapi project in this backend directory

2. gimme an endpoint that takes a .txt file as an input

3. can you generate me a document.txt file for a company policy

4. what other online embedding models are free.

5. the text document is possibly a company policy, a product spec, or a technical guide... since we dont know the doc structure wouldn't it be ideal to split it based on \n and paragraph lining.

6. gimme the format for para-wise and line-wise splitting for recursivechartextsplitter

7. gimme a template for a rag system that answers questions from the uploaded document and answers only from the uploaded document and if the answer is not in the document return "I don't know"

8. i have added and tested a rag implementation in the rag.py file. use it to create endpoints

-/ingest

* takes a .txt file as input
* use the chromadb as db and store the embeddings generated
* return the size of the chunks upon success

-/query

* takes the query as input
* use the retriever as in the rag.py to retrieve the chunks and feed it to llm
* return the answer from the llm and the sources/chunks used to answer the questions

9. i need a chat ui for "AI chat application". use a minimal structure as shown in the image to generate the ui and also use the app.tsx file to build the ui

10. build a docker compose file to run the frontend, backend and the chromadb

11. how to fix the "ignoreDeprecations": "5.0", error in typescript

12. gimme the code for adding the client as a CORS origin in fastapi

13. can you add another endpoint /clear

* output: clears the chromadb so that a new document can be ingested after clearing the context

14. there is a cors issue generated in the docker containers. how can we fix it
