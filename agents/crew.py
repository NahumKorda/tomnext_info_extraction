from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from agents.pdf_reader import PDFReader


@CrewBase
class ExecutiveExtractionCrew:

	@agent
	def pdf_reader(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_reader'],
			tools=[PDFReader()],
			verbose=False,
		)

	@agent
	def executive_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['executive_extractor'],
			verbose=True,
		)

	@agent
	def search_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['search_agent'],
			tools = [SerperDevTool()],
			verbose=True,
		)

	@agent
	def executive_quality_evaluator(self) -> Agent:
		return Agent(
			config=self.agents_config['executive_quality_evaluator'],
			verbose=True,
		)

	@task
	def pdf_extraction(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_extraction'],
		)

	@task
	def executive_extraction(self) -> Task:
		return Task(
			config=self.tasks_config['executive_extraction'],
		)

	@task
	def information_retrieval(self) -> Task:
		return Task(
			config=self.tasks_config['information_retrieval'],
		)

	@task
	def executive_assessment(self) -> Task:
		return Task(
			config=self.tasks_config['executive_assessment'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
