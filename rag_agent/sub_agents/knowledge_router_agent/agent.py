import logging

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state 
from ...tools.rag_query import rag_query

from ..answer_agent import answer_agent
from ..quiz_generator_agent import quiz_generator_agent
from ..summarize_lesson_agent import summarize_lesson_agent  

from google.adk import Agent
from google.adk.agents import ParallelAgent

from ...config import MODEL


knowledge_router_agent = Agent(
    name="knowledge_router_agent",
    model=MODEL, 
    description="Routing task to the right agent based on user intent", 
    instruction="""
    You are a knowledge router assistant that routes to an appropriate agent based on user {intent?} list and {query?}.
    Based on the {query?}, you should retrieve the appropriate information from corpora using the 'rag_query' tool.
    `rag_query`: Query a corpus to answer questions
       - Parameters:
         - corpus_name: The name of the corpus to query (required, but can be empty to use current corpus)
         - query: The text question to ask 
         
    Then, you should use the 'append_to_state' tool to store the retrieved information into the 'context' state.
    With each element in the list {intent?}, you call a specific agent to handle the task.
    Base on corresponding user intent, you should route to the right agent, if there is more than one intent, you should run them in parallel:
    - If the user intent is 'ask', you should route to 'answer_agent'. 
    - If the user intent is 'create_quiz', you should route to 'quiz_generator'.
    - If the user intent is 'summarize', you should route to 'summarize_lesson_agent'.
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[rag_query, append_to_state],
    sub_agents=[answer_agent, quiz_generator_agent, summarize_lesson_agent],
)