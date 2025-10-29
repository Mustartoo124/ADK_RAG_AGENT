
import logging

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state 

from google.adk import Agent

from ...config import MODEL


quiz_generator_agent = Agent(
    name="quiz_generator_agent",
    model=MODEL, 
    description="Answer user questions based on provided context like a tutor", 
    instruction="""
    If in the user {intent?} list there is no 'create_quiz', don't respond anything with this agent. 
    Base on the user {query?} and provided {context?}, you should generate {quiz_number?} quiz questions with 4 options each and indicate the correct answer.
    If the quiz is not in the provided context, you should inform the user that you cannot create the quiz based on the given context. 
    1. Each question should be clear and concise.
    2. Each question should have 4 options, labeled A, B, C, and D.
    3. Indicate the correct answer for each question.
    4. The questions should cover different aspects of the provided context to ensure a comprehensive assessment.
    5. Your output should be in Vietnamese.
    6. Format the output as a JSON array of objects, where each object represents a quiz question with the following structure:
    (
        "quizzes":
        (
            "question": "Question text",
            "options": (
                "A": "Option A text",
                "B": "Option B text",
                "C": "Option C text",
                "D": "Option D text"
            ),
            "correct_answer": "A" // or B, C, D
        ), 
        
        (
            "question": "Question text",
            "options": (
                "A": "Option A text",
                "B": "Option B text",
                "C": "Option C text",
                "D": "Option D text"
            ),
            "correct_answer": "A" // or B, C, D
        ), 
        
    )
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[
        append_to_state, 
           ],
)