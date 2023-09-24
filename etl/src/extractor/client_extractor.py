import requests
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.client_transformer import ClientTransformerHandler
from util.row_data_processor import RowDataProcessor
from configuration.env import URL_BASE_API, API_KEY_HEADER, API_KEY

logger = log.get_logger("client-extractor-component")


class ClientExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = ClientTransformerHandler()

    @staticmethod
    def extract(workspace) -> dict:
        url = URL_BASE_API + "workspaces/" + workspace["id"] + "/clients"
        headers = {API_KEY_HEADER: API_KEY}
        data = requests.get(url, headers=headers).json()
        return data

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of clients in thriviti time-tracking')
        clients_data = []
        for workspace in RowDataProcessor.workspaces_data:
            clients_data.extend(self.extract(workspace))
        RowDataProcessor.client_data = clients_data
        super().set_next(self.handler)
        super().handle(clients_data)

