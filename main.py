from load_env import load_env_vars
from config import Config
import utils



if __name__=="__main__":
    load_env_vars()
    args = utils.parse_args()
    config = Config()
    
    
