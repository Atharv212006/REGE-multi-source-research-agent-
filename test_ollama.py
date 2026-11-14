from langchain_ollama import ChatOllama, OllamaEmbeddings

# Test Llama
llm = ChatOllama(model="llama3.2")

response = llm.invoke("What is artificial intelligence?")

print("LLM Response:")
print(response.content)

# Test Embedding
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector = embeddings.embed_query("AI Research Agent")

print("\nEmbedding dimensions:", len(vector))