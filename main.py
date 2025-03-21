import os
import pandas as pd

from typing import List
from config import Config
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import load_prompt, ChatPromptTemplate
from pydantic import BaseModel, Field

# Define desired output structure
class Step(BaseModel):
    step_description: str = Field(..., description="Description of the analytical step")
    datasets: List = Field(..., description="Datasets used")
    rationale: str = Field(..., description="Why this step is necessary")
    task_type: str = Field(..., description="The type of computation required e.g. data_retrieval, correlation, visualization")
    
class Plan(BaseModel):
    steps: List[Step]

# Obtain formatting instructions
parser = PydanticOutputParser(pydantic_object=Plan)
format_instructions = parser.get_format_instructions()

if __name__=="__main__":
    config = Config()
    data_path = config.SELECTED_DATA_DIR

    # get user query
    user_query = input("Enter your query: \n")
    print("User Has asked: \n", user_query)

    # Load prompts
    try:
        planner_prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sys_messages', 'message_planner.txt')
        if os.path.exists(planner_prompt_path):
            with open(planner_prompt_path, 'r') as file:
                planner_prompt_text = file.read()
            prompt_template = ChatPromptTemplate.from_template(planner_prompt_text)
            prompt_template = prompt_template.partial(format_instructions=format_instructions)
        else:
            raise Exception("path to the system message file not found")
    except Exception as e:
        print("Exception occured: ", e)

    breakpoint()

    # llm parameters
    #    temperature = 0
    #    max_tokens = 200

    llm=ChatOllama(model="llama3.2:latest")
    
    # create chain
    chain = prompt_template | llm | parser
   
    # get response
    inputs = {
           "user_query": user_query,
           "data_path": data_path
           }

    response = chain.invoke(inputs)

    print("Response: \n", response)
