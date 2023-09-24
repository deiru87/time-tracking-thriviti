import requests
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.workspace_transformer import WorkspaceTransformerHandler
from util.row_data_processor import RowDataProcessor
from configuration.env import URL_BASE_API, API_KEY_HEADER, API_KEY

logger = log.get_logger("workspace-extractor-component")


class WorkspaceExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = WorkspaceTransformerHandler()

    @staticmethod
    def extract() -> dict:
        url = URL_BASE_API + "workspaces"
        headers = {API_KEY_HEADER: API_KEY}
        data = requests.get(url, headers=headers).json()
        return data

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of workspaces in thriviti time-tracking')
        workspace_data = self.extract()
        RowDataProcessor.workspaces_data = workspace_data
        super().set_next(self.handler)
        super().handle(workspace_data)


