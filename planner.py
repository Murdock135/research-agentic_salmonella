import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import sys
from typing import List
from config import Config
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import load_prompt, ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel, Field

from utils import (
    get_llm, 
    get_user_query, 
    parse_args,
    get_data_paths_bash_tree,
    get_df_heads
)

MODEL = "meta-llama/llama-4-maverick:free"
PROVIDER = "openrouter"

# Define desired output structure
class Step(BaseModel):
    """Information about a step"""
    step_description: str = Field(..., description="Description of the analytical step")
    datasets: List[str] = Field(..., description="List of dataset names used")
    rationale: str = Field(..., description="Why this step is necessary")
    task_type: List[str] = Field(..., description="The type of computation required e.g. data_retrieval, correlation, visualization")
    
class Plan(BaseModel):
    """Information about the the steps in a plan to answer the user query"""
    steps: List[Step]

    def pretty_print(self):
        for i, step in enumerate(self.steps):
            print(f"Step {i}")
            print(f"Description: {step.step_description}")
            print(f"Datasets: {step.datasets}")
            print(f"Rationale: {step.rationale}")
            print(f"Tast Type: {step.task_type}")
            print()
       
def get_plan(llm, prompt, user_query, parser):
    chain = prompt | llm | parser

    # get response
    response = chain.invoke({"user_query": user_query})  
    return chain, response

def generate_plan(llm, prompt_text, user_query, data_path):
    parser = PydanticOutputParser(pydantic_object=Plan)
    
    # Format instructions
    try:
        format_instructions = parser.get_format_instructions()
    except Exception as e:
        print("Couldn't get formatting instructions. Exception: ", e)
        
    tree = get_data_paths_bash_tree(data_path)
    df_heads = get_df_heads(data_path)
    
    prompt = ChatPromptTemplate.from_messages(
        [ 
            ("system", prompt_text),
            ("human", "{user_query}")
        ]).partial(
            tree=tree,
            df_heads=df_heads, 
            format_instructions=format_instructions)

    chain, plan = get_plan(llm, prompt, user_query, parser)
    
    return chain, plan
        

# Use for testing generate_plan()
if __name__ == "__main__":
    load_dotenv()
    args = parse_args()
    model = MODEL
    provider = PROVIDER
    
    config = Config()
    llm = get_llm(model, provider)
    prompts: dict[str, str] = config.load_prompts()
    data_path = config.SELECTED_DATA_DIR
    user_query = get_user_query(args)
    
    # Generate plan
    prompt_text = prompts['planner_prompt']
    chain, plan = generate_plan(llm, prompt_text, user_query, data_path)

    # print(plan)
    plan.pretty_print()
    

