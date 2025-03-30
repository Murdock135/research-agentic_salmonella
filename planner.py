import os
import pandas as pd
import sys
from typing import List
from config import Config
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import load_prompt, ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# Define desired output structure
class Step(BaseModel):
    step_description: str = Field(..., description="Description of the analytical step")
    datasets: List[str] = Field(..., description="List of dataset names used")
    rationale: str = Field(..., description="Why this step is necessary")
    task_type: str = Field(..., description="The type of computation required e.g. data_retrieval, correlation, visualization")
    
class Plan(BaseModel):
    steps: List[Step]

def get_user_query():
    # For testing, use a hardcoded query if one is provided as argument
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        user_query = "What is the correlation between social vulnerability and salmonella rates in Missouri?"
        print("Using test query: ", user_query)
    else:
        # get user query
        user_query = input("Enter your query: \n")

    return user_query
    
def load_prompts(prompt_paths_dict):
    planner_prompt_path = prompt_paths_dict['planner_prompt_path'] 
    # code for other prompt paths here

    # complete the dict later
    prompt_dict = {
            'planner_prompt': None,
            }

    with open(planner_prompt_path, 'r') as f:
        prompt_dict['planner_prompt'] = f.read()

    return prompt_dict 

def get_plan(config: Config):
    prompt_paths = config.get_prompt_paths() # load system prompts
    prompts :dict[str, str] = load_prompts(prompt_paths) # load prompts. store in a dictionary
    data_path = config.SELECTED_DATA_DIR # set path to data
    user_query = get_user_query() # user query

    # Create prompt template
#    prompt_template = PromptTemplate.from_template(prompts['planner_prompt'])
    prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompts['planner_prompt']),
                ("human", "{user_query}")
            ]).partial(data_path=data_path)
       
    # llm parameters
    #    temperature = 0
    #    max_tokens = 200
    breakpoint()

    llm=ChatOllama(model="llama3.2:latest", temperature=0) # instantiate language model
    # structured_llm = llm.with_structured_output(Plan, include_raw=True) 
    chain = prompt | llm

    # get response
    response = chain.invoke({"user_query": user_query})  
    return response

if __name__ == "__main__":
    config = Config()
    plan = get_plan(config)

    print(plan)
