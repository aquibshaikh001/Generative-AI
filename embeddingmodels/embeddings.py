from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    dimensions=64
)

text = [ 
        "Hello this is Aquib Shaikh",
        "Hello your name is Youtube",
        "And you are all beautiful"
        ]

vectors = embeddings.embed_documents(text)

print(vectors)