from pprint import pprint
import warnings
warnings.filterwarnings('ignore')

import os
import yaml
import pprint
#loading crewai Library
from crewai import Agent, Task, Crew, LLM
#load environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv()
#check load APIS
from helper import check_api_keys
check_api_keys()

#Add Nvidia Deepseek model
llm =LLM(
    #model="openai/gpt-4o-mini",
    #api_key=os.getenv("OPENAI_API_KEY")
    model="openai/deepseek-ai/deepseek-v4-pro",
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

#Define file paths for YAML configurations
files={
    'lead_agents': 'config/lead_qualifications_agents.yaml',
    'lead_tasks': 'config/lead_qualifications_tasks.yaml',
    'email_agents': 'config/email_engagement_agents.yaml',
    'email_tasks': 'config/email_engagement_tasks.yaml'
}

#load configurations

configs={}
for config_type, file_path in files.items():
    with open(file_path,"r") as file:
        configs[config_type] =yaml.safe_load(file)
    
#Assign loaded configurations from YAML files


lead_agents_config= configs["load_agents"] 
lead_tasks_config= configs["lead_tasks"] 
email_agents_config= configs["email_agents"] 
email_tasks_config= configs["email_tasks"] 

#create pydantic models

from pydantic import BaseModel,Field
from typing import Dict, Optional, List, Set, Tuple

class LeadPersonalInfo(BaseModel):
    name:str = Field(..., description="The full name of the Lead")
    job_title:str = Field(..., description="The job title of the lead")
    role_relevance: int =Field(..., description=" score representing how relevant the lead's role is to the decision-making process (0-10)")
    professional_background: Optional[str] = Field(default=None, description="A brief description of the lead's professional background.")

class CompanyInfo(BaseModel):
    name:str= Field(..., description="The name of the company the Lead work for.")
    industry:str = Field(..., description="The industry in wich the company operates")
    company_size:int =Field(..., description="The size of the company in terms of employee count.")
    revenue: Optional[float] = Field(None, description="The annual revenue of the company, if available.")

class LeadScore(BaseModel):
    score: int= Field(..., ge=0, le=100,description="The final score assigned to the lead (0-100).")
    score_criteria: List[str] =Field(..., description="The criteria used to determine the lead's score.")
    validation_notes:Optional[str] =Field(None, description="The criteria used to determine the lead's score.")

class LeadScoringResult(BaseModel):
    personal_info: LeadPersonalInfo =Field(..., description="Personal information about the lead")
    company_info: CompanyInfo =Field(..., description="Information about the lead's company.")
    lead_score: LeadScore = Field(...,description="The calculated score and related information for the lead.")


#Creating Agents
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

lead_data_agent=Agent(
    config=lead_agents_config['lead_data_agent'],
    tools=[SerperDevTool(),ScrapeWebsiteTool]
)

cultural_fit_agent =Agent(
    config= lead_agents_config['cultural_fit_agent'],
    tools=[SerperDevTool(),ScrapeWebsiteTool]
)

scoring_validation_agent = Agent(
    config= lead_agents_config['scoring_validation_agent']
)

#Add Tasks

lead_data_task = Task(
    config= lead_tasks_config['lead_data_collection'],
    agent=lead_data_agent
)

cultural_fit_task =Task(
    config=lead_tasks_config['cultural_fit_analysis'],
    agent=cultural_fit_agent
)

scoring_validation_task = Task(
    config=lead_tasks_config['lead_scoring_and_validation'],
    agent= scoring_validation_agent,
    context=[lead_data_task,cultural_fit_task],
    output_pydantic=LeadScoringResult
)

