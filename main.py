import os
import pandas as pd

from config import Config
from langchain_ollama import ChatOllama
from langchain_core.prompts import load_prompt, ChatPromptTemplate

if __name__=="__main__":
    config = Config()
    data_path = config.SELECTED_DATA_DIR

    # Load prompts
    try:
        planner_prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sys_messages', 'message_planner.txt')
        if os.path.exists(planner_prompt_path):
            with open(planner_prompt_path, 'r') as file:
                planner_prompt_text = file.read()
            prompt_template = ChatPromptTemplate.from_template(planner_prompt_text)
            planner_prompt = prompt_template.format_messages(data_path)
        else:
            raise Exception("path to the system message file not found")
    except Exception as e:
        print("The system prompt for the planner LLM not found")

    breakpoint()

    # llm parameters
    #    temperature = 0
    #    max_tokens = 200

    llm=ChatOllama(model="llama3.2:latest")

    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to Malay. Translate the user's sentence"
        ),
        ("human", "I love programming."),
    ]

    ai_msg = llm.invoke(messages)
    print(ai_msg)


