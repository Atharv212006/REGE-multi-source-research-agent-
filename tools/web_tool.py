
from langchain_core.tools import tool
from tavily import TavilyClient

from config.settings import TAVILY_API_KEY


@tool
def web_search(query: str) -> str:
    """
    Search the internet for current information.

    Use this tool when the user asks about:
    latest news, recent developments, current events,
    or information that requires internet research.
    """

    try:

        if not TAVILY_API_KEY:
            return "Tavily API key is missing. Check your .env file."

        # Initialize Tavily client
        client = TavilyClient(
            api_key=TAVILY_API_KEY
        )

        # Search the internet
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5
        )

        results = response.get("results", [])

        if not results:
            return "No relevant web results found."

        # Format search results
        output = []

        for i, result in enumerate(results, start=1):

            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "No content")

            formatted_result = f"""
Result {i}

Title: {title}

URL: {url}

Content:
{content}
"""

            output.append(formatted_result)

        return "\n\n".join(output)

    except Exception as error:

        return f"Web search failed: {str(error)}"
