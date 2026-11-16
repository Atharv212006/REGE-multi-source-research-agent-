
from agents.research_agent import agent

question = input("Enter your research question: ")

print("\n========== RESEARCH ANSWER ==========\n")

response = agent.invoke({
    "messages": [
        {"role": "user", "content": question}
    ]
})

# Display all agent messages
for message in response["messages"]:
    print("\nMessage Type:", message.type)

    # Check whether the agent called a tool
    if message.type == "tool":
        print("Tool Used:", message.name)
        print("Tool Output:", message.content[:500])

    elif message.type == "ai":
        if message.content:
            print("AI Response:", message.content)
        
        if message.tool_calls:
            print("Tools Requested:")
            for tool_call in message.tool_calls:
                print("-", tool_call["name"])
