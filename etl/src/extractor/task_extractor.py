import requests
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.task_transformer import TaskTransformerHandler
from util.row_data_processor import RowDataProcessor
from configuration.env import URL_BASE_API, API_KEY_HEADER, API_KEY

logger = log.get_logger("task-extractor-component")


class TaskExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = TaskTransformerHandler()

    @staticmethod
    def extract(workspace, project) -> dict:
        url = URL_BASE_API + "workspaces/" + workspace["id"] + "/projects/" + project["id"] + "/tasks"
        headers = {API_KEY_HEADER: API_KEY}
        data = requests.get(url, headers=headers).json()
        return data

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of tasks in thriviti time-tracking')
        tasks_data = []
        for workspace in RowDataProcessor.workspaces_data:
            for project in RowDataProcessor.projects_data:
                tasks_data.extend(self.extract(workspace, project))
        super().set_next(self.handler)
        super().handle(tasks_data)

