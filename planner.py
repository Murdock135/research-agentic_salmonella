import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import sys
from typing import List
from config import Config
from langchain_ollama import ChatOllama
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import load_prompt, ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel, Field
import argparse

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

def parse_args():
    parser = argparse.ArgumentParser(description="Run planner with LLM backend")
    parser.add_argument('--test', action="store_true", help="Use a test query")
    parser.add_argument('--ollama', action="store_true", help="Use ollama backend")
    parser.add_argument('--openrouter', action="store_true", help="Use openrouter backend")
    parser.add_argument("--model", type=str, help="Model name")
    return parser.parse_args()

def get_llm(args):
    model = args.model or "meta-llama/llama-4-maverick:free"

    if args.openrouter and args.ollama:
        raise ValueError("Please specify only one backend: --openrouter or --ollama. Not both.")

    if args.openrouter:
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL")
        breakpoint()        
        return ChatOpenAI(
                openai_api_key=api_key,
                openai_api_base=base_url,
                model_name=str(model)
                )

    elif args.ollama:
        return ChatOllama(model="gemma3:12b")    

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
    return response

if __name__ == "__main__":
    args = parse_args()
    load_dotenv()
    config = Config()
    llm = get_llm(args)
    prompt_paths = config.get_prompt_paths()
    prompts: dict[str, str] = load_prompts(prompt_paths)
    data_path = config.SELECTED_DATA_DIR
    user_query = get_user_query(args)
   
    # Parser
    parser = PydanticOutputParser(pydantic_object=Plan)

    # Format instructions
    try:
        format_instructions = parser.get_format_instructions()
    except Exception as e:
        print("Couldn't get formatting instructions. Exception: ", e)

    prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompts['planner_prompt']),
                ("human", "{user_query}")
            ]).partial(data_path=data_path, format_instructions=format_instructions) 

    plan = get_plan(llm, prompt, user_query, parser)

    print(plan)
    
    # Save response
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(config.PLANNER_RESPONSES_DIR, f"p_response_{timestamp}.txt")

    with open(filename, 'w') as f:
        f.write(str(plan))
