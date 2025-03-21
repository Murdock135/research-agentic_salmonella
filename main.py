import os
import pandas as pd
import sys
from typing import List
from config import Config
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import load_prompt, ChatPromptTemplate
from pydantic import BaseModel, Field

# Define desired output structure
class Step(BaseModel):
    step_description: str = Field(..., description="Description of the analytical step")
    datasets: List[str] = Field(..., description="List of dataset names used")
    rationale: str = Field(..., description="Why this step is necessary")
    task_type: str = Field(..., description="The type of computation required e.g. data_retrieval, correlation, visualization")
    
class Plan(BaseModel):
    steps: List[Step]

# Obtain formatting instructions
parser = PydanticOutputParser(pydantic_object=Plan)
format_instructions = parser.get_format_instructions()
print("Format instructions:\n", format_instructions)

if __name__=="__main__":
    config = Config()
    data_path = config.SELECTED_DATA_DIR

    # For testing, use a hardcoded query if one is provided as argument
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        user_query = "What is the correlation between social vulnerability and salmonella rates in Missouri?"
        print("Using test query: ", user_query)
    else:
        # get user query
        user_query = input("Enter your query: \n")
    
    print("User Has asked: \n", user_query)

    # Load prompts
    planner_prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sys_messages', 'message_planner.txt')
    if os.path.exists(planner_prompt_path):
        with open(planner_prompt_path, 'r') as file:
            planner_prompt_text = file.read()
    else:
        raise Exception("path to the system message file not found")

    # create the prompt template using format_instructions
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", planner_prompt_text),
        ("human", "{user_query}")
    ])

    # Inject the formatting instructions
    prompt_template = prompt_template.partial(format_instructions = format_instructions)
    
    # Test if prompt is properly templated
    inputs = {
            "data_path": data_path,
            "user_query": user_query
            }

    print("Prompt:\n", prompt_template.invoke(inputs).to_string())

    # llm parameters
    #    temperature = 0
    #    max_tokens = 200

    llm=ChatOllama(model="llama3.2:latest", temperature=0)
    
    # get response
