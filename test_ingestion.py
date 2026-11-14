from ingestion.loaders import load_documents

documents = load_documents("data/uploads")

print("Total documents/pages loaded:", len(documents))

for document in documents:

    print("\nSource:", document.metadata["source"])

    print("Content:")
    print(document.page_content[:300])

    print("-" * 50)