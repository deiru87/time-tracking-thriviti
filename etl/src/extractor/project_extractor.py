import requests
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.project_transformer import ProjectTransformerHandler
from util.row_data_processor import RowDataProcessor
from configuration.env import URL_BASE_API, API_KEY_HEADER, API_KEY, NAME_PARAM_PAGE_SIZE, PAGE_SIZE

logger = log.get_logger("client-extractor-component")


class ProjectExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = ProjectTransformerHandler()

    @staticmethod
    def extract(workspace) -> dict:
        url = URL_BASE_API + "workspaces/" + workspace["id"] + "/projects"
        headers = {API_KEY_HEADER: API_KEY}
        params = {NAME_PARAM_PAGE_SIZE: PAGE_SIZE}
        data = requests.get(url, headers=headers, params=params).json()
        return data

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of projects in thriviti time-tracking')
        projects_data = []
        for workspace in RowDataProcessor.workspaces_data:
            projects_data.extend(self.extract(workspace))
        RowDataProcessor.projects_data = projects_data
        super().set_next(self.handler)
        super().handle(projects_data)

