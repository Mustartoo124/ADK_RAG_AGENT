
import logging

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state 

from google.adk import Agent

from ...config import MODEL


context_adapter_agent = Agent(
    name="context_adapter_agent",
    model=MODEL, 
    description="Translate Vietnamese to English", 
    instruction="""
    You are a translate assistant that translates
    user input to English if the input is in Vietnamese. 
    If the input is already in English, you just return it without any change.
    When they respond, use the 'append_to_state' tool to store the user's response
    in the 'query' state key and transfer to 'user_context_agent'.
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[append_to_state],
)