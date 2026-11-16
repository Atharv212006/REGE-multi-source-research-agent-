
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL
from tools.document_tool import search_documents
from tools.web_tool import web_search


# 1. Initialize the LLM
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)


# 2. Register available tools
tools = [
    search_documents,
    web_search
]


# 3. Define the Research Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    You are an intelligent multi-source research assistant.

    You have access to two tools:

    1. search_documents:
       Use this tool to search information in uploaded documents.

    2. web_search:
       Use this tool to search the internet for current information.

    Instructions:
    - Understand the user's question before choosing a tool.
    - Use document search for questions about uploaded files.
    - Use web search for current or external information.
    - Use both tools when the question requires information from
      both uploaded documents and the internet.
    - Never invent search results or document content.
    - Provide clear, detailed and well-structured answers.
    - If the available information is insufficient, say so.
    """
)


# 4. Function to run the Research Agent
def run_research_agent(question: str) -> str:

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    return response["messages"][-1].content
