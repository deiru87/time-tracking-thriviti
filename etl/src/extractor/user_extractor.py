import requests
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.user_transformer import UserTransformerHandler
from util.row_data_processor import RowDataProcessor
from configuration.env import URL_BASE_API, API_KEY_HEADER, API_KEY

logger = log.get_logger("user-extractor-component")


class UserExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = UserTransformerHandler()

    @staticmethod
    def extract(workspace) -> dict:
        url = URL_BASE_API + "workspaces/" + workspace["id"] + "/users"
        headers = {API_KEY_HEADER: API_KEY}
        data = requests.get(url, headers=headers).json()
        return data

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of users in thriviti time-tracking')
        users_data = []
        for workspace in RowDataProcessor.workspaces_data:
            users_data.extend(self.extract(workspace))
        super().set_next(self.handler)
        super().handle(users_data)

