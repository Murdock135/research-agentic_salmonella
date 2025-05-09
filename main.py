
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

from utils import get_llm, parse_args

 

def pretty_print_llms(llm_dict):
    for llm_name, llm_obj in llm_dict.items():
        print(f"{llm_name}: {llm_obj}")
        print()

def load_prompts(prompt_paths_dict):
    planner_prompt_path = prompt_paths_dict['planner_prompt_path'] 
    # code for other prompt paths here

    # complete the dict later
    prompt_dict = {
        'explorer_prompt': None,
        'analyzer_prompt': None,
        'planner_prompt': None,
        'executor_prompt': None,
        'aggregator_prompt': None
            }

    with open(planner_prompt_path, 'r') as f:
        prompt_dict['planner_prompt'] = f.read()

    return prompt_dict 



if __name__=="__main__":
    load_dotenv()
    args = parse_args()
    config = Config()
    
    llm_names = ['explorer', 'analyzer', 'planner', 'executor', 'aggregator']
    llms: dict = {llm_name: get_llm(args) for llm_name in llm_names}

    pretty_print_llms(llms)
