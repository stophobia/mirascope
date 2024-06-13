"""
Extracting structured information with retries
"""
import os
from typing import Literal, Type

from pydantic import BaseModel

from mirascope.openai import OpenAIExtractor

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"


class TaskDetails(BaseModel):
    description: str
    due_date: str
    priority: Literal["low", "normal", "high"]


class TaskExtractor(OpenAIExtractor[TaskDetails]):
    extract_schema: Type[TaskDetails] = TaskDetails
    prompt_template = """
	Extract the task details from the following task:
	{task}
	"""

    task: str


task = "Submit quarterly report by next Friday. Task is high priority."
task_details = TaskExtractor(task=task).extract(retries=3)
assert isinstance(task_details, TaskDetails)
print(task_details)
# > description='Submit quarterly report' due_date='next Friday' priority='high'
