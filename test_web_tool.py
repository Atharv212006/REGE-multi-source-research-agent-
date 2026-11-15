
from tools.web_tool import web_search

question = "Latest developments in Generative AI"

result = web_search.invoke({
    "query": question
})

print("\n========== WEB SEARCH RESULTS ==========")

print(result)

print("\n========== TEST COMPLETED ==========")
