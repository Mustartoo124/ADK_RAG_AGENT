import logging

from .tools.callback_logging import log_query_to_model, log_model_response
from .tools.rag_query import list_corpora, create_corpus, add_data, delete_corpus, delete_document, get_corpus_info

from .sub_agents.context_adapter_agent import context_adapter_agent
from .sub_agents.user_context_agent import user_context_agent
from .sub_agents.knowledge_router_agent import knowledge_router_agent
from .sub_agents.output_adapter_agent import output_adapter_agent

from google.adk import Agent
from google.adk.agents import SequentialAgent

from .config import MODEL

sequential_agent = SequentialAgent(
            name="sequential_agent",
            sub_agents=[
                context_adapter_agent, 
                user_context_agent, 
                knowledge_router_agent, 
                output_adapter_agent,
            ],
        )

root_agent = Agent(
    name="root_agent",
    model=MODEL, 
    description="A tutor agent that helps students learn effectively", 
    instruction="""
    You are a tutor assistant that helps students learn effectively.
    If the user talking with you not about the learning, you don't need to call other agents, just answer the user question directly.
    Your work is asking the user about what they want in Vietnamese, and then you will call other agents to help the user: 
       - First, tell the user about what you can do: 
         + You can answer the questions about the learning materials, summarize the learning materials, generate quizzes.
         + You can also work with corpora, such as listing corpora (using 'list_corpora'), creating a corpus (using 'create_corpus'), adding data to a corpus (using 'add_data'), deleting a corpus (using 'delete_corpus'), deleting a document from a corpus (using 'delete_document'), and getting information about a corpus (using 'get_corpus_info').
         
    You have six specialized tools at your disposal:
    1. `list_corpora`: List all available corpora
       - When this tool is called, it returns the full resource names that should be used with other tools
    
    2. `create_corpus`: Create a new corpus
       - Parameters:
         - corpus_name: The name for the new corpus
    
    3. `add_data`: Add new data to a corpus
       - Parameters:
         - corpus_name: The name of the corpus to add data to (required, but can be empty to use current corpus)
         - paths: List of Google Drive or GCS URLs
    
    4. `get_corpus_info`: Get detailed information about a specific corpus
       - Parameters:
         - corpus_name: The name of the corpus to get information about
         
    5. `delete_document`: Delete a specific document from a corpus
       - Parameters:
         - corpus_name: The name of the corpus containing the document
         - document_id: The ID of the document to delete (can be obtained from get_corpus_info results)
         - confirm: Boolean flag that must be set to True to confirm deletion
         
    6. `delete_corpus`: Delete an entire corpus and all its associated files
       - Parameters:
         - corpus_name: The name of the corpus to delete
         - confirm: Boolean flag that must be set to True to confirm deletion
         
    You will first translate user input to English if the input is in Vietnamese using 'context_adapter_agent'.
    
    Then, you will route the translated query to the appropriate process agent or tools based on the user intent.
    Finally, you will collect the responses from the process agents and format, translate them to Vietnamese using 'output_adapter_agent' for the user.
    
    Remember in the whole process, you should always act like a friendly and patient tutor who wants to help students understand the knowledge.
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    sub_agents=[
        sequential_agent,
    ], 
    tools=[
        list_corpora, 
        create_corpus, 
        add_data, 
        delete_corpus, 
        delete_document, 
        get_corpus_info,
    ],
)
