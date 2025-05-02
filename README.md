# Agentic Salmonella Research Analysis

A framework for analyzing relationships between salmonella outbreaks, socioeconomic factors, and geographic data using a multi-agent LLM approach.

## Project Overview

This project employs a structured, agentic approach to analyze salmonella outbreak data in relation to socioeconomic and geographic factors. It uses specialized LLM agents for different aspects of the research workflow:

- **Planner**: Creates structured analysis plans with specific steps
- **Explorer**: Examines data characteristics and relationships
- **Analyzer**: Performs statistical analysis on datasets
- **Executor**: Implements the analysis steps
- **Aggregator**: Combines results into coherent findings

## Features

- Multi-agent LLM approach for comprehensive analysis
- Structured output using Pydantic models
- Support for multiple LLM backends (OpenRouter, Ollama)
- Organized data management for multiple datasets
- Standardized analysis workflow

## Data Sources

The framework is designed to work with several datasets:
- Salmonella outbreak data
- Social Vulnerability Index (SVI)
- Census demographic data
- Food insecurity data

Note: Some datasets like PulseNet have limited usage rights and must be manually downloaded.

## Getting Started

### Prerequisites

- Python 3.8+
- Required packages listed in `requirements.txt`

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/research-agentic_salmonella.git
cd research-agentic_salmonella

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file to include your API keys
```

### Usage

```bash
# Run the planner with OpenRouter backend
python planner.py --openrouter

# Use a specific model
python planner.py --openrouter --model meta-llama/llama-4-maverick:free

# Run with local Ollama model
python planner.py --ollama

# Use test query
python planner.py --openrouter --test
```

## Project Structure

- `main.py`: Application entry point
- `planner.py`: Creates structured analysis plans
- `config.py`: Manages project configuration and directories
- `utils/`: Utility functions for data loading
- `sys_messages/`: System prompts for LLM agents
- `responses/`: Saved LLM responses
- `data/`: Data storage (not included in repository)

## Current Status

This project is a work in progress, with the planner component fully implemented and other components (explorer, analyzer, executor, aggregator) in development.

## License

[License information]

## Acknowledgements

[Any acknowledgements]