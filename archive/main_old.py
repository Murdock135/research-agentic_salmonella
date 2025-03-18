import pandas as pd
import os
from config import Config

from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv, find_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI


# Load data
state = 'MO'
year = '2020'

# TODO: MAKE A DATA DIR AND CHANGE THIS
data_path = os.path.join(Config.SOCIOECONO_SALMONELLA_DIR, f'sense-d_socioecono_salmonella_{state}_{year}.csv')
df = pd.read_csv(data_path)

# Convert dataframe to SQL table
table_name = "socio_econo_salmonella"
db_name = f'{Config.SQL_DATA_DIR}/{table_name}'
engine = create_engine(f"sqlite:///{db_name}.db")

inspector = inspect(engine)
if table_name in inspector.get_table_names():
    print(f"Table {table_name} already exists. Data not written to database.")
else:
    # Write to SQL database only if table doesn't exist
    try:
        df.to_sql(table_name, engine, index=False)
        print("Data written to the database.")
    except Exception as e:
        print(f"Error writing to database: {e}")

# Load database
db = SQLDatabase(engine)
print(db.dialect)
print("Available tables: ", db.get_usable_table_names())

# Create SQL agent
model = ChatOpenAI(model="gpt-3.5-turbo")
agent_executor = create_sql_agent(model, db=db, agent_type="openai-tools", verbose=True)

# Invoke agent
response = agent_executor.invoke({"input": "which county has the highest salmonella rate?"})
print(response)

if __name__=="__main__":
    _ = load_dotenv(find_dotenv())
    breakpoint()
