
import logging

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state 

from google.adk import Agent
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from ...config import MODEL


answer_agent = Agent(
    name="answer_agent",
    model=MODEL, 
    description="Answer user questions based on provided context like a tutor", 
    instruction="""
    If in the user {intent?} list there is no 'ask', don't respond anything with this agent.
    Base on the user {query?} and provided {context?}, you should provide a comprehensive and detailed answer.
    If the answer is not in the provided context, use Wikipedia tool to find the answer.
    The answer should be well-structured and easy to understand in a json format with the following structure:
    (
        "answer": "Your detailed answer here"
    )
    
    Use the 'append_to_state' tool to store to the 'answer' state key.
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[
        LangchainTool(tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())),
        append_to_state, 
           ],
)