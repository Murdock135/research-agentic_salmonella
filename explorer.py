from dotenv import load_dotenv
from config import Config
from utils import load_dataset, get_llm, load_text, get_df_heads, get_data_paths_bash_tree
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langchain_experimental.utilities import PythonREPL
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
import os
import pandas as pd
import tools as mytools

TOOLS = [
    'read_file',
    'copy_file',
    'file_search',
    'list_directory',
]

TEST_QUERIES = [
    "",
    "How many counties are there in each dataset?",
    "Explore the data"
    ]
  
if __name__ == "__main__":
    # load_dotenv()
    config = Config()
    prompts = config.load_prompts()
    user_messages = config.load_user_messages()
    explorer_prompt = prompts['explorer_prompt']
    user_message = user_messages['explorer_user_message']
        
    # Use LLM to get dataset file names
    working_dir = config.SELECTED_DATA_DIR
    print("Working Directory: ", working_dir)
    tree = get_data_paths_bash_tree(working_dir)
    print(tree)
    df_heads = get_df_heads(working_dir)
        
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", explorer_prompt),
            ("human", "{user_query}"),
            ("placeholder", "{agent_scratchpad}")
        ]
    ).partial(
        tree=tree,
        df_heads=df_heads
    )   
    
    llm = init_chat_model("o3-mini", model_provider="openai")
    python_repl = PythonREPL()
    pythonREPLtool = Tool(
        name="python_repl",
        func=python_repl.run,
        description="A Python REPL that can execute Python code. Use this to run Python code and get the result.",
    )
    
    tools = [mytools.load_dataset, mytools.get_sheet_names, pythonREPLtool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(name='Explorer', agent=agent, tools=tools, verbose=True, return_intermediate_steps=False)
    
    for step in agent_executor.stream({"user_query": user_message}):
        print(step)   
    
    # response = agent_executor.invoke({"user_query":user_message})
    # print(response)
    
    







