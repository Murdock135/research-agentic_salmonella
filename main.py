from load_env import load_env_vars
from config import Config
import utils

def get_llms(llm_config: dict):
    pass

if __name__=="__main__":
    load_env_vars()
    config = Config()
    
    llm_config_path = config.LLM_CONFIG_PATH
    llm_config = utils.load_llm_config(llm_config_path)
    
    # Get Chat Models (Language models)
    planner_config = llm_config['planner']
    planner_llm = utils.get_llm(planner_config['model'], planner_config['provider'])
    
    
