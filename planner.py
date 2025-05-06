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
import argparse

from utils import get_llm

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

def parse_args():
    parser = argparse.ArgumentParser(description="Run planner with LLM backend")
    parser.add_argument('--test', action="store_true", help="Use a test query")
    parser.add_argument('--ollama', action="store_true", help="Use ollama backend")
    parser.add_argument('--openrouter', action="store_true", help="Use openrouter backend")
    parser.add_argument("--model", type=str, help="Model name")
    return parser.parse_args()

def get_user_query(args):
    if args.test:
        user_query = "What is the correlation between social vulnerability and salmonella rates?"
        print("Using test query: ", user_query)
    else:
        while True:
            user_query = input("Enter your query:\n")

    return user_query
       
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
    
    prompt = ChatPromptTemplate.from_messages(
        [ 
            ("system", prompt_text),
            ("human", "{user_query}")
        ]).partial(data_path=data_path, format_instructions=format_instructions)

    chain, plan = get_plan(llm, prompt, user_query, parser)
    
    return chain, plan
        

if __name__ == "__main__":
    args = parse_args()
    load_dotenv()
    config = Config()
    llm = get_llm(args)
    prompts: dict[str, str] = config.load_prompts()
    data_path = config.SELECTED_DATA_DIR
    user_query = get_user_query(args)
    
    # Generate plan
    prompt_text = prompts['planner_prompt']
    chain, plan = generate_plan(llm, prompt_text, user_query, data_path)

    # print(plan)
    plan.pretty_print()
    
    # Save response
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(config.PLANNER_OUTPUT_DIR, f"p_response_{timestamp}.txt")

    with open(filename, 'w') as f:
        f.write(str(plan))
