from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# Define desired output structure
class Step(BaseModel):
    step_description: str = Field(..., description="Description of the analytical step")
    datasets: List[str] = Field(..., description="List of dataset names used")
    rationale: str = Field(..., description="Why this step is necessary") 
    task_type: str = Field(..., description="The type of computation required e.g. data_retrieval, correlation, visualization")
    
class Plan(BaseModel):
    steps: List[Step]

# Obtain formatting instructions
parser = PydanticOutputParser(pydantic_object=Plan)
format_instructions = parser.get_format_instructions()

print(format_instructions)

# Test with a sample output
test_json = '''
{
  "steps": [
    {
      "step_description": "Retrieve social vulnerability index data for Missouri counties",
      "datasets": ["svi/SVI_2020_US_county.csv"],
      "rationale": "To analyze correlation with salmonella rates, we first need the SVI data by county",
      "task_type": "data_retrieval"
    },
    {
      "step_description": "Retrieve salmonella incidence data for Missouri counties",
      "datasets": ["sense-d_socioecono_salmonella_MO_2020.csv"],
      "rationale": "We need salmonella rates by county to analyze correlation with SVI",
      "task_type": "data_retrieval"
    },
    {
      "step_description": "Calculate correlation between SVI components and salmonella rates",
      "datasets": ["svi/SVI_2020_US_county.csv", "sense-d_socioecono_salmonella_MO_2020.csv"],
      "rationale": "To identify which social vulnerability factors correlate with salmonella incidence",
      "task_type": "correlation"
    }
  ]
}
'''

try:
    result = parser.parse(test_json)
    print("\nParsed successfully:")
    print(result)
except Exception as e:
    print("\nParser failed with error:")
    print(e)