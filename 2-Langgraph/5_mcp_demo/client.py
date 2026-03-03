from langchain_mcp_adapters.client import MultiServerMCPClient
#from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import os

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

import asyncio


async def main():
    client = MultiServerMCPClient(
        {
            "main":{
                "command":"python",
                "args":["D:/python/AI/pynb/2-Langgraph/5_mcp_demo/main.py"],
                "transport":"stdio",
            }
        }
    )

    tools=await client.get_tools()
    model=ChatGroq(model="qwen/qwen3-32b")
    # agent=create_react_agent(
    #     model,tools
    # )

    agent=create_agent(
        model,tools
    )


    resp = await agent.ainvoke(
        {"messages":[{"role":"user", "content":"what customer Name matches the customer id CUST123"}]}
    )

    print(resp["messages"][-1].content)

asyncio.run(main())