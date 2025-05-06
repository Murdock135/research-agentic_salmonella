from dotenv import load_dotenv
from config import Config
from utils import load_dataset
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit

tools = [
    'read_file',
    'copy_file',
    'file_search',
    'list_directory',
]

if __name__ == "__main__":
    load_dotenv()
    config = Config()
    prompts = config.load_prompts()
    
    explorer_prompt = prompts['explorer_prompt']
    print("Explorer Prompt:")
    print(explorer_prompt)
    
    working_dir = config.SELECTED_DATA_DIR
    print("Working Directory: ", working_dir)
    
    toolkit = FileManagementToolkit(
        root_dir=working_dir,
        selected_tools=tools
    )
    toolkit.get_tools()
    
    print("Available Tools:")
    for tool in toolkit.get_tools():
        print(tool.name)
    
    
    
    
    
    
    