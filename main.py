from load_env import load_env_vars
from config import Config
import utils

from pipeline import pipeline

def get_llms(llm_config: dict):
    explorer_config = llm_config['explorer']
    planner_config = llm_config['planner']
    analyzer_config = llm_config['analyzer']
    executor_config = llm_config['executor']
    aggregator_config = llm_config['aggregator']
    
    get_llm = utils.get_llm
    
    return {
        'explorer_llm': get_llm(model=explorer_config['model'], provider=explorer_config['provider']),
        'planner_llm': get_llm(model=planner_config['model'], provider=planner_config['provider']),
        'analyzer_llm': get_llm(model=analyzer_config['model'], provider=analyzer_config['provider']),
        'executor_llm': get_llm(model=executor_config['model'], provider=executor_config['provider']),
        'aggregator_llm': get_llm(model=aggregator_config['model'], provider=aggregator_config['provider'])
    }
    

if __name__=="__main__":
    load_env_vars()
    args = utils.parse_args()
    config = Config()
    
    llm_config = config.load_llm_config()
    llms: dict = get_llms(llm_config)
    
    user_query = utils.get_user_query(args)
    data_path = config.SELECTED_DATA_DIR
    prompts = config.load_prompts()
    
    pipeline(
        user_query=user_query,
        llms=llms,
        prompts=prompts,
        data_path=data_path
    )
    
    
    
    
    
    
