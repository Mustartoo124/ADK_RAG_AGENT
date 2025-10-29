
import logging

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state 

from google.adk import Agent


from ...config import MODEL


summarize_lesson_agent = Agent(
    name="summarize_lesson_agent",
    model=MODEL, 
    description="Summarize lesson content concisely", 
    instruction="""
    If in the user {intent?} list there is no 'summarize', don't respond anything with this agent.
    Base on the user {query?} and provided {context?}, write a concise summary of the lesson content.
    The summary should capture the key points and essential information from the lesson.
    The summary should be well-structured and easy to understand in a json format with the following structure:
    (
        "summary": "Your concise summary in vietnamese here"
    )
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[
        append_to_state, 
           ],
)