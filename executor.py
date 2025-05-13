from config import Config
from load_env import load_env_vars
import utils
import tools

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

def execute(llm, user_message, system_prompt, config_obj: Config):
    working_dir = config_obj.SELECTED_DATA_DIR
    tree = utils.get_data_paths_bash_tree(working_dir)
    df_heads = utils.get_df_heads(working_dir)
    
    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", "{user_query}"),
            ("placeholder", "{agent_scratchpad}")
        ]
    ).partial(
        tree=tree,
        df_heads=df_heads
    )
    
    pythonREPLtool = tools.getpythonrepltool()
    fs_tools = ['read_file', 'list_directory', 'file_search']
    _tools = [pythonREPLtool, tools.load_dataset] + tools.filesystemtools(working_dir, fs_tools)
    agent = create_tool_calling_agent(llm, _tools, prompt)
    agent_executor = AgentExecutor(name="Executor", agent=agent, tools=_tools, verbose=True)

    for step in agent_executor.stream({"user_query": user_message}):
        print(step)

# For testing
if __name__ == "__main__":
    load_env_vars()
    config = Config()
    args = utils.parse_args()
    
    system_prompts = config.load_prompts()
    system_prompt = system_prompts['executor_prompt']

    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", "{user_query}"),
            ("placeholder", "{agent_scratchpad}")
        ]
    )
    
    # Get llm and create agent
    llm_config = config.load_llm_config()
    executor_config = llm_config['executor']
    llm = utils.get_llm(model=executor_config['model'], provider=executor_config['provider'])
    
    if args.test:
        user_message = "Code up a binary search tree in python. Then test on sample data"
        print(f"Using test query: '{user_message}'")
        args.test = False
    else:
        user_message = utils.get_user_query()
        print(f"Using query: '{user_message}'")
        
    execute(llm, user_message, system_prompt)        
    
    
    