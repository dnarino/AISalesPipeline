import warnings
warnings.filterwarnings('ignore')

import os
import yaml
#loading crewai Library
from crewai import Agent, Task, Crew, LLM
#load environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv()

#Add Nvidia Deepseek model
llm =LLM(
    #model="openai/gpt-4o-mini",
    #api_key=os.getenv("OPENAI_API_KEY")
    model="openai/deepseek-ai/deepseek-v4-pro",
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)
