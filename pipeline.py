from planner import generate_plan
from executor import execute
from config import Config

def pipeline(
    user_query: str,
    llms: dict,
    prompts: dict,
    data_path: str,
    config_obj: Config
    
):  
    # Prompts
    planner_prompt: str = prompts['planner_prompt']
    executor_prompt = prompts['executor_prompt']
    
    chain, plan = generate_plan(llms['planner_llm'], planner_prompt, user_query, data_path)
    
    # Print the plan
    plan.pretty_print()
    
    # Pass plan to executor
    executor_llm = llms['executor_llm']
    steps = plan.steps
    print("="*50)
    for i, step in enumerate(steps):
        print("-"*50)
        print(f"Step {i} of plan. [Step: {step.step_description}]")
        print("-"*50)
        
        execute(
            llm=executor_llm,
            user_message=step.step_description,
            system_prompt=executor_prompt,
            config_obj=config_obj
        )
        
        
        
    