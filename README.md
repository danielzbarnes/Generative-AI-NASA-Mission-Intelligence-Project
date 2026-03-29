# Generative AI-NASA Mission Intelligence Project

This project is to build a Q&A system that can answer questions about some of NASA's most historic space missions. This will process and work with actual mission transcripts and technical documents from Apollo 11, Apollo 13, and the Challenger missions.

The high-level view of the project:

- The Embedding Pipeline, first processes the raw NASA text files and chunks them into manageable sizes. The chunks are then converted into numerical representations—or embeddings and store them in ChromaDB.
- The RAG Client, this is the core of the retrieval system. This is the logic that takes a user's question, searches the ChromaDB database to find the most relevant document chunks, and then formats that information neatly to be used as context.
- The LLM Client, this connect to the OpenAI API. This component will take the user's question and the context from your RAG client and generate a helpful, human-readable answer.
- The RAGAS Evaluator, checks how well the RAG system worked.
- The Chat Application, the interactive chat interface using Streamlit that brings the application together.

### Installation

1. **Navigate to the project folder**:
   ```bash
   cd project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"


 ### **Implementation**

1. **Run the complete pipeline**:
   ```bash
   # Process documents
   python embedding_pipeline.py --openai-key YOUR_KEY --data-path ./data
   
   # Launch chat interface
   streamlit run chat.py
   ```
