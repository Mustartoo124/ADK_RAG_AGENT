
import logging

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state 

from google.adk import Agent

from ...config import MODEL


user_context_agent = Agent(
    name="user_context_agent",
    model=MODEL, 
    description="Define user intent from user input", 
    instruction="""
    You are a user context assistant that extract user intents from user input you get from {query?}.
    There are three type of user intents: 
    - ask: The user is asking a question to you. With this instance, you should use the 'append_to_state' tool to store 
    the user intent into the 'intent' state, this case is 'ask'. For example, if the user input is "What is the capital of France?",
    you should use the 'append_to_state' tool to store 'ask' into the 'intent' state.
    - create_quiz: The user is asking you to create quizzes. With this instance, you should use the 'append_to_state' tool to store
    the user intent into the 'intent' state, this case is 'create_quiz'. For example, if the user input is "Create a quiz about
    history", you should use the 'append_to_state' tool to store 'create_quiz' into the 'intent' state. More over, if user ask for a specific
    number of quiz questions, you should also use the 'append_to_state' tool to store that number into the 'quiz_number' state. If there is no 
    specific number, you should store the default value 5 into the 'quiz_number' state.
    - summarize: The user is asking you to summarize the current lesson. With this instance, you should use the 'append_to_state' tool to store
    the user intent into the 'intent' state, this case is 'summarize'. For example, if the user input is "Summarize this lesson for me",
    you should use the 'append_to_state' tool to store 'summarize' into the 'intent' state.
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[append_to_state],
)