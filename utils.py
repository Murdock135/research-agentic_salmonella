# utils.py
import pandas as pd
import os
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

def load_text(file_path):
    """Loads text from a file."""
    with open(file_path, 'r') as f:
        text = f.read()

    return text

def load_dataset(file_path, sheet_name=None):
    """
    Loads a dataset from either a CSV or an Excel sheet.
    Args:
        file_path (str): Path to the dataset file.
        sheet_name (str, optional): Name of the Excel sheet to load. Defaults to None.
    Returns:
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') and sheet_name:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format or missing sheet name for Excel file.")
    
def get_llm(args):
    model = args.model or "meta-llama/llama-4-maverick:free"

    if args.openrouter and args.ollama:
        raise ValueError("Please specify only one backend: --openrouter or --ollama. Not both.")

    elif args.ollama:
        return ChatOllama(model="gemma3:12b")   
    
    else:
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL")
        return ChatOpenAI(
                openai_api_key=api_key,
                openai_api_base=base_url,
                model_name=str(model)
                )


# Tests
if __name__ == "__main__":
    from config import Config
    
    config = Config()
    data_paths = config.get_selected_data_paths()
    mmg_dir = data_paths['mmg']
    mmg_data_path = os.path.join(mmg_dir, 'MMG2022_2020-2019Data_ToShare.xlsx')
    
    df = load_dataset(mmg_data_path, sheet_name='County')
    print(df.head().to_markdown())
    print("Data loaded successfully.")