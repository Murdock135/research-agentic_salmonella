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
    system_prompts_dict = config.get_prompt_paths()
    breakpoint()

    # Create prompt template
    prompt_template = PromptTemplate.from_template(planner_prompt_text)
    
    # Test if prompt is properly templated
    inputs = {
            "data_path": data_path,
            "user_query": user_query
            }

    print("Prompt:\n", prompt_template.invoke(inputs).to_string())
    prompt = prompt_template.format(data_path=data_path,
                                    user_query=user_query)
    # llm parameters
    #    temperature = 0
    #    max_tokens = 200

    llm=ChatOllama(model="llama3.2:latest", temperature=0)
    structured_llm = llm.with_structured_output(Plan, include_raw=True)    

    # get response
    response = structured_llm.invoke(prompt) 
    print(response)
