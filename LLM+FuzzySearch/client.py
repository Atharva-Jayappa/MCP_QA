import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import Optional, Any
from google import genai
import os

client = genai.Client(api_key="")  # Unlike myself, use an .env file to store your API key securely.


class MCPClient:

    """
    A client for interacting with the OpenAI MCP server using Server-Sent Events (SSE).
    """

    def __init__(self):
        """
        Initialize the OpenAI MCP client.
        """
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.write_stream: Optional[Any] = None
        self.read_stream: Optional[Any] = None

    async def initialize(self, user_query: str, server_path: str = "http://127.0.0.1:8050/sse") -> None:
        """
        Initialize the MCP client, connect to the server, and list available tools.
        This method will also send a user query to the server and print the response.
        :param user_query: the user's query to be sent to the MCP server.
        :param server_path: path to the MCP server's SSE endpoint.
        :return: generates a response using gemini api based on the user query using the MCP server's tools.
        """
        async with sse_client(server_path) as (self.read_stream, self.write_stream):
            async with ClientSession(self.read_stream, self.write_stream) as self.session:
                await self.session.initialize()

                tools_result = await self.session.list_tools()

                print("Available tools:")
                for tool in tools_result.tools:
                    print(f"- {tool.name}: {tool.description}")

                prompt = f"""You are a helpful assistant that can answer questions about user queries
                
                You have a tool called `fetch_context` that can be used to answer questions. 
                
                this will fuzzy search its internal QA pairs and return the best match.
                 so that you can answer the user's question specifically and accurately.
                 
                The user query is: "{user_query}"
                
                Use the tool if you the question seems specific, else if its just a general question, you can answer it directly.
                
                """

                # Send request to the model with MCP function declarations
                response = await client.aio.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.125,
                        tools=[self.session],  # uses the session, will automatically call the tool
                        # Uncomment if you **don't** want the SDK to automatically call the tool
                        # automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(
                        #     disable=True
                        # ),
                    ),
                )
                print(response.text)


async def main():
    mcpclient = MCPClient()
    await mcpclient.initialize(user_query="<Context Specific Question Here>",)


if __name__ == "__main__":
    asyncio.run(main())
