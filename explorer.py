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
    messages = [HumanMessage(user_message)]
        
    # Use LLM to get dataset file names
    working_dir = config.SELECTED_DATA_DIR
    print("Working Directory: ", working_dir)
    tree = get_data_paths_bash_tree(working_dir)
    print(tree)
    df_heads = get_df_heads(working_dir)
        
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", explorer_prompt),
            ("human", "{user_query}")
        ]
    ).partial(
        tree=tree,
        df_heads=df_heads
    )   
    
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    python_repl = PythonREPL()
    pythonREPLtool = Tool(
        name="python_repl",
        func=python_repl.run,
        description="A Python REPL that can execute Python code. Use this to run Python code and get the result.",
    )
    
    tools = [mytools.get_sheet_names, mytools.load_dataset, pythonREPLtool]
    llm_with_tools = llm.bind_tools(tools)
    chain = prompt | llm_with_tools 
    
    response = chain.invoke({"user_query": user_message})
    messages.append(response)
    tool_calls = response.tool_calls
    print("Tool Calls:\n", tool_calls)

    tool_mapping = {
        "python_repl": pythonREPLtool,
        "get_sheet_names": mytools.get_sheet_names,
        "load_dataset": mytools.load_dataset
    }

    for tool_call in tool_calls:
        # Use the lower-case version of the tool name for mapping lookup
        selected_tool = tool_mapping.get(tool_call["name"].lower())
        if selected_tool:
            # The example from the docs uses .invoke, so we mimic that interface:
            tool_msg = selected_tool.invoke(tool_call)
            messages.append(tool_msg)
            print(f"Result from {tool_call['name']}:", tool_msg)
        else:
            print(f"Tool {tool_call['name']} is not supported.")

    print("="* 50)
    print("Messages")
    for message in messages:
        print("message:")
        print(message)
    
    # breakpoint()
    # Final output
    response = llm_with_tools.invoke(messages)
    print("="*50)
    print("Response")
    print(response)
    







