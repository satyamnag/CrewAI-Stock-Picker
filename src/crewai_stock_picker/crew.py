import os
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool

class TrendingCompany(BaseModel):
    """A company that is in the news and attracting attention."""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """List of multiple trending companies that are in the news."""
    companies: List[TrendingCompany] = Field(
        description="List of companies trending in the news"
    )

class TrendingCompanyResearch(BaseModel):
    """Detailed research on a company."""
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """A list of detailed research on all the companies."""
    research_list: List[TrendingCompanyResearch] = Field(
        description="Comprehensive research on all trending companies"
    )

@CrewBase
class CrewaiStockPicker():
    """CrewaiStockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        try:
            return Agent(
                config=self.agents_config["trending_company_finder"],
                tools=[SerperDevTool()],
                memory=True
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create agent 'trending_company_finder': {e}")

    @agent
    def financial_researcher(self) -> Agent:
        try:
            return Agent(
                config=self.agents_config["financial_researcher"],
                tools=[SerperDevTool()],
            )
        except KeyError:
            raise RuntimeError("Missing agent config: 'financial_researcher'")
        except Exception as e:
            raise RuntimeError(f"Error creating 'financial_researcher': {e}")

    @agent
    def stock_picker(self) -> Agent:
        try:
            return Agent(
                config=self.agents_config["stock_picker"],
                tools=[PushNotificationTool()],
                memory=True
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create agent 'stock_picker': {e}")

    @task
    def find_trending_companies(self) -> Task:
        try:
            return Task(
                config=self.tasks_config["find_trending_companies"],
                output_pydantic=TrendingCompanyList,
            )
        except KeyError:
            raise RuntimeError("Task config missing: 'find_trending_companies'")
        except Exception as e:
            raise RuntimeError(f"Error creating task 'find_trending_companies': {e}")

    @task
    def research_trending_companies(self) -> Task:
        try:
            return Task(
                config=self.tasks_config["research_trending_companies"],
                output_pydantic=TrendingCompanyResearchList,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create task 'research_trending_companies': {e}")

    @task
    def pick_best_company(self) -> Task:
        try:
            return Task(
                config=self.tasks_config["pick_best_company"],
            )
        except Exception as e:
            raise RuntimeError(f"Error creating task 'pick_best_company': {e}")

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiStockPicker crew with memory and error handling."""
        try:
            manager = Agent(
                config = self.agents_config["manager"],
                allow_delegation=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize manager agent: {e}")

        try:
            long_term_memory = LongTermMemory(
                storage = LTMSQLiteStorage(
                    db_path = "./memory/long_term_memory_storage.db"
                )
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize long-term memory: {e}")

        try:
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                    embedder_config = {
                        "provider": "openai",
                        "config": {
                            "model_name": "text-embedding-3-small",
                            "api_key": os.getenv("OPENAI_API_KEY"),
                        }
                    },
                    type = "short_term",
                    path = "./memory/",
                )
            )
        except Exception as e:
            raise RuntimeError(f"Failed to set up RAG short-term memory: {e}")
        
        try:
            entity_memory = EntityMemory(
                storage = RAGStorage(
                    embedder_config = {
                        "provider": "openai",
                        "config": {
                            "model_name": "text-embedding-3-small",
                            "api_key": os.getenv("OPENAI_API_KEY")
                        }
                    },
                    type = "short_term",
                    path = "./memory/"
                )
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize entity memory: {e}")

        try:
            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.hierarchical,
                verbose=True,
                manager_agent=manager,
                memory=True,
                long_term_memory=long_term_memory,
                short_term_memory=short_term_memory,
                entity_memory=entity_memory,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create StockPicker crew: {e}")