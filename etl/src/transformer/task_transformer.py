import pandas as pd
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.task_loader import TaskLoaderHandler

logger = log.get_logger("task-transformer-component")


class TaskTransformerHandler(AbstractHandler):

    def __init__(self):
        self.handler = TaskLoaderHandler()

    @staticmethod
    def transform(tasks) -> Any:
        final_tasks = []
        for task in tasks:
            tmp_task = {"id": task["id"], "name": task["name"],
                        "project_id": task["projectId"],
                        "estimate": task["estimate"],
                        "duration": task["duration"],
                        "billable": task["billable"],
                        "hourly_rate_amount": task["hourlyRate"]["amount"] if task["hourlyRate"] is not None else "",
                        "hourly_rate_currency": task["hourlyRate"]["currency"] if task[
                                                                                      "hourlyRate"] is not None else "",
                        "cost_rate_amount": task["costRate"]["amount"] if task["costRate"] is not None else "",
                        "cost_rate_currency": task["costRate"]["currency"] if task["costRate"] is not None else "", }
            final_tasks.append(tmp_task)
        return pd.DataFrame.from_records(final_tasks)

    def handle(self, request: Any) -> None:
        tasks = self.transform(request)
        super().set_next(self.handler)
        super().handle(tasks)
