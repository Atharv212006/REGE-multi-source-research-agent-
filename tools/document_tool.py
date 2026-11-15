
from langchain_core.tools import tool
from ingestion.indexer import load_vectorstore


@tool
def search_documents(query: str) -> str:
    """
    Search uploaded PDF, DOCX and TXT documents.

    Use this tool to find information from
    documents uploaded by the user.
    """

    try:

        # Load FAISS database
        vectorstore = load_vectorstore()

        # Find relevant text chunks
        results = vectorstore.similarity_search(
            query,
            k=4
        )

        if not results:
            return "No relevant information found."

        # Prepare search results
        output = []

        for i, doc in enumerate(results, start=1):

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")

            result = f"""
Result {i}
Source: {source}
Page: {page}

Content:
{doc.page_content}
"""

            output.append(result)

        return "\n\n".join(output)

    except Exception as error:

        return f"Document search failed: {str(error)}"
