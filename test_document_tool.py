
from tools.document_tool import search_documents

question = "What is the main topic of this document?"

result = search_documents.invoke({
    "query": question
})

print("\n========== DOCUMENT SEARCH ==========")

print(result)

print("\n========== TEST COMPLETED ==========")
