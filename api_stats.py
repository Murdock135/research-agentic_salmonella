class api_stats:
    def __init__(self):
        self.total_api_calls = 0
        self.planner_api_calls = 0
        self.explorer_api_calls = 0
        self.analyzer_api_calls = 0
        self.executor_api_calls = 0
        self.aggregator_api_calls = 0
        
        self.total_tokens_used = 0