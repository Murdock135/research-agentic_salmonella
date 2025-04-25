import os
import datetime

class Config:
    def __init__(self):
        # Set the base directory to the directory of this file
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Set the data directories relative to the base directory
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.RAW_DATA_DIR = os.path.join(self.DATA_DIR, 'raw')
        self.PROCESSED_DATA_DIR = os.path.join(self.DATA_DIR, 'processed')
        self.SQL_DATA_DIR = os.path.join(self.DATA_DIR, 'SQL version')

        # Data directories
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.RAW_DATA_DIR = os.path.join(self.DATA_DIR, 'raw')
        self.PROCESSED_DATA_DIR = os.path.join(self.DATA_DIR, 'processed')
        self.SQL_DATA_DIR = os.path.join(self.DATA_DIR, 'SQL version')

        # Specific Data directories
        self.MMG_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'mmg')
        self.PN_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'pulsenet')
        self.SVI_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'social_vulnerability_index')
        self.RAW_POULTRY_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'raw_poultry')
        self.CENSUS_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'census')
        self.NORS_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'nors')
        self.FOODNET_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'foodnet')
        self.SOCIOECONO_SALMONELLA_DIR = os.path.join(self.PROCESSED_DATA_DIR, 'salmonella_population')

        # Selected data directories
        self.SELECTED_DATA_DIR = os.path.join(self.RAW_DATA_DIR, 'selected_data')
        self.SELECTED_MMG_DIR = os.path.join(self.SELECTED_DATA_DIR, 'mmg')
        self.SELECTED_NORS_DIR = os.path.join(self.SELECTED_DATA_DIR, 'nors')
        self.SELECTED_SVI_DIR = os.path.join(self.SELECTED_DATA_DIR, 'svi')
        self.SELECTED_SOCIOECONO_SALMONELLA = os.path.join(self.SELECTED_DATA_DIR, 'sense-d_socioecono_salmonella_MO_2020.csv')

        # Set the output directories relative to the base directory
        self.OUTPUT_DIR = os.path.join(self.BASE_DIR, 'output')

        # Create output directory for a specific run
        self.create_output_directory_for_run()
    
    def get_selected_data_paths(self):
        return {
            'mmg': self.SELECTED_MMG_DIR,
            'nors': self.SELECTED_NORS_DIR,
            'svi': self.SELECTED_SVI_DIR,
            'socioecono_salmonella': self.SELECTED_SOCIOECONO_SALMONELLA
        }
    
    def get_prompt_paths(self):
        prompts_dir = os.path.join(self.BASE_DIR, 'sys_messages')

        return {
            "planner_prompt_path" : os.path.join(prompts_dir, 'planner_message.txt')
        }

    def create_output_directory_for_run(self):
        format = "%d-%m-%Y_%H-%M-%S"
        now = datetime.datetime.now()
        now_str = now.strftime(format)
        self.RUN_OUTPUT_DIR = os.path.join(self.OUTPUT_DIR, now_str)
        os.makedirs(self.RUN_OUTPUT_DIR, exist_ok=True)

        directory_names = ['explorer', 'analyzer', 'planner', 'executor', 'aggregator'] 
        for dir_name in directory_names:
            os.makedirs(os.path.join(self.RUN_OUTPUT_DIR, dir_name), exist_ok=True)






