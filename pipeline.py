from planner import generate_plan

def pipeline(
    user_query: str,
    llms: dict,
    prompts: dict,
    data_path: str,
    
):
    """
    Run the entire pipeline for the Agentic system.
    
    Args:
        user_query (str): The user's query.
        planner_llm: The LLM for planning.
        explorer_llm: The LLM for exploration.
        executor_llm: The LLM for execution.
        analyzer_llm: The LLM for analysis.
        aggregator_llm: The LLM for aggregation.
        prompts (dict): A dictionary containing prompt templates.
        data_path (str): Path to the data directory.
        
    Returns:
        None
    """
    
    # Generate plan
    planner_prompt: str = prompts['planner_prompt']
    chain, plan = generate_plan(llms['planner_llm'], planner_prompt, user_query, data_path)
    
    # Print the plan
    plan.pretty_print()