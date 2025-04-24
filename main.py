
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

def get_llm(args):
    model = args.model or "meta-llama/llama-4-maverick:free"

    if args.openrouter and args.ollama:
        raise ValueError("Please specify only one backend: --openrouter or --ollama. Not both.")

    if args.openrouter:
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL")
        return ChatOpenAI(
                openai_api_key=api_key,
                openai_api_base=base_url,
                model_name=str(model)
                )

    elif args.ollama:
        return ChatOllama(model="gemma3:12b")    

def pretty_print_llms(llm_dict):
    for llm_name, llm_obj in llm_dict.items():
        print(f"{llm_name}: {llm_obj}")
        print()

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

if __name__=="__main__":
    load_dotenv()
    args = parse_args()
    
    llm_names = ['explorer', 'analyzer', 'planner']
    llms: dict = {llm_name: get_llm(args) for llm_name in llm_names}

    pretty_print_llms(llms)
