import os

class Config:
    # Project root directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    

    # Data directories
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    SQL_DATA_DIR = os.path.join(DATA_DIR, 'SQL version')

    # Specific data directories
    MMG_DATA_DIR = os.path.join(RAW_DATA_DIR, 'mmg')
    PN_DATA_DIR = os.path.join(RAW_DATA_DIR, 'pulsenet')
    SVI_DATA_DIR = os.path.join(RAW_DATA_DIR, 'social_vulnerability_index')
    RAW_POULTRY_DATA_DIR = os.path.join(RAW_DATA_DIR, 'raw_poultry')
    CENSUS_DATA_DIR = os.path.join(RAW_DATA_DIR, 'census')
    NORS_DATA_DIR = os.path.join(RAW_DATA_DIR, 'nors')
    FOODNET_DATA_DIR = os.path.join(RAW_DATA_DIR, 'foodnet')
    SOCIOECONO_SALMONELLA_DIR = os.path.join(PROCESSED_DATA_DIR, 'salmonella_population')

    # Output directories
    RESPONSES_DIR = os.path.join(BASE_DIR, 'responses')
    PLANNER_RESPONSES_DIR = os.path.join(RESPONSES_DIR, 'planner')
    EXECUTOR_RESPONSES_DIR = os.path.join(RESPONSES_DIR, 'executor')
    AGGREGATOR_RESPONSES_DIR = os.path.join(RESPONSES_DIR, 'aggregator')
    # FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
    # REPORTS_DIR = os.path.join(RESULTS_DIR, 'reports')

    # Selected data directory
    SELECTED_DATA_DIR = os.path.join(BASE_DIR, 'selected_data')
    
    # Selected dataset paths
    SELECTED_MMG_DIR = os.path.join(SELECTED_DATA_DIR, 'mmg')
    SELECTED_NORS_DIR = os.path.join(SELECTED_DATA_DIR, 'nors')
    SELECTED_SVI_DIR = os.path.join(SELECTED_DATA_DIR, 'svi')
    SELECTED_SOCIOECONO_SALMONELLA = os.path.join(SELECTED_DATA_DIR, 'sense-d_socioecono_salmonella_MO_2020.csv')
    
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
