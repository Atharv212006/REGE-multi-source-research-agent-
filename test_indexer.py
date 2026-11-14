
from ingestion.indexer import build_vectorstore

folder_path = "data/uploads"

vectorstore = build_vectorstore(folder_path)

print("\nFAISS indexing completed!")

# Test similarity search
results = vectorstore.similarity_search(
    "What is the main topic of this document?",
    k=3
)

print("\n--- SEARCH RESULTS ---")

for result in results:

    print("\nSource:", result.metadata.get("source"))

    print("Content:")
    print(result.page_content[:300])

    print("-" * 50)
