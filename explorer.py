from dotenv import load_dotenv
from config import Config
from utils import load_dataset, get_llm
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
import os

TOOLS = [
    'read_file',
    'copy_file',
    'file_search',
    'list_directory',
]

# TODO
def generate_df_head(df, n=5, working_dir=None):
    """
    Use LLM to generate a head of the dataframe
    """
    pass

def _get_dataset_file_names(root_dir, tools=TOOLS):
    """
    Get names of files and directories in a given directory
    Args:
        root_dir (str): Path to the directory
        tools (list): List of tools to use e.g. ['read_file', 'copy_file', 'file_search', 'list_directory']
    Returns:
        contents (str): Names of files and directories in the given directory separated by new lines
    """
    toolkit = FileManagementToolkit(
        root_dir=root_dir,
        selected_tools=tools
    )
    tools = toolkit.get_tools()
    
    # print("Available Tools:")
    # for tool in tools:
    #     print(tool.name)    
    
    # print(f"Files/Directories in {root_dir}:")
    contents = tools[-1].invoke({})
    
    return contents

def recursive_file_search(func, root_dir):
    """
    Recursively search for files in a directory
    """
    iter = 4
    for i in range(iter):
        pass
    
def get_data_paths(root):
    for dirpath, dirnames, filenames in os.walk(root):
        print("Directory:", dirpath)
        print("Subdirectories:", dirnames)
        print("Files:", filenames)
        
    
    
if __name__ == "__main__":
    # load_dotenv()
    config = Config()
    prompts = config.load_prompts()
    
    # Use LLM to get dataset file names
    working_dir = config.SELECTED_DATA_DIR
    print("Working Directory: ", working_dir)

    toolkit = FileManagementToolkit(
    root_dir=working_dir,
    selected_tools=TOOLS
    )
    tools = toolkit.get_tools()
    print("Available Tools:")
    for tool in tools:
        print(tool.name)
        
    # llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    
    agent = create_tool_calling_agent(
        llm=ChatOpenAI(model="gpt-4o"),
        tools=tools,
        prompt=prompt,
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    user_message = "List all files in the directory"
    response = agent_executor.invoke({"input": user_message})
    print("Response: ", response)
    

        
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", explorer_prompt),
    #         ("human", "{user_query}")
    #     ]
    # ).partial(
    #     df_heads=
    
    # explorer_prompt = prompts['explorer_prompt']
    # print("Explorer Prompt:")
    # print(explorer_prompt)
    

    
    
    
    
    
    
    