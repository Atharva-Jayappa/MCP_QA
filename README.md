# MCP\_QnA 🚀

Welcome to MCP_QnA ! This repository integrates an Large Language Model (Google Gemini) with a MCP server to answer context specific questions.

Currently I have added two modules: one based on a vector database for context search and another using fuzzy search for quick matching. 
Enjoy exploring the project! 😃

## Repository Structure

- **LLM\+VectorDB**  
  Contains code to query a vector database and get context from research papers.
  - `client.py`: Implements a client using Server-Sent Events (SSE) to interact with the MCP server.
  - `embed_documents.py`: Embeds documents from research papers (or any other document of you choice).
  - `fetch_chunks.py`: Splits or fetches document chunks for processing.
  - `server.py`: Implements the server side for handling vector database requests.
  

- **LLM\+FuzzySearch**  
  Supports fuzzy searching within the available context data.
  - `client.py`: Implements a client for fuzzy searching.
  - `context.json`: Holds context data used for fuzzy search.
  - `server.py`: Provides the server logic for fuzzy searches.

## Key Features ✨

- **Client-Server Communication**: Uses Server-Sent Events (SSE) for real-time communication (Easily upgradable to streamable-http based server). 
- **Tool Integration**: The client in `client.py` demonstrates how to list tools and make context-based requests.

## Getting Started 🔧

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Atharva-Jayappa/MCP_QnA.git
   cd MCP_QnA

2. **Install Dependencies**
   Make sure Python is installed and then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
    Store your API keys securely. For example:
    ```bash
    set GENAI_API_KEY=your_api_key_here
    ```
   
4. **Run the Application**
    For the clien script in the vector database module, run:
    ```bash
    cd LLM+VectorDB
    python client.py
    ```
   For the server script in the vector database module, run:
   ```bash
    cd LLM+VectorDB
    python server.py
    ```
   Same for the fuzzy search module:


## Usage 💡

- **Vector Database Query**: The client in `LLM+VectorDB/client.py` connects to the MCP server via SSE, lists available tools, and sends user queries to fetch embedded document context in the form of chunks.
- **Fuzzy Search Query**: The client in `LLM+FuzzySearch/client.py` allows users to perform fuzzy searches on the context data stored in `context.json`.
- **Server-Sent Events (SSE)**: The server in `server.py` handles SSE connections, allowing real-time updates and responses to client requests.
   
