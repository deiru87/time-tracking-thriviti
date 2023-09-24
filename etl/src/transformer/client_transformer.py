import pandas as pd
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.client_loader import ClientLoaderHandler

logger = log.get_logger("client-transformer-component")


class ClientTransformerHandler(AbstractHandler):

    def __init__(self):
        self.handler = ClientLoaderHandler()

    @staticmethod
    def transform(clients) -> Any:
        final_clients = []
        for client in clients:
            tmp_client = {"id": client["id"], "name": client["name"],
                          "email": client["email"],
                          "workspace_id": client["workspaceId"],
                          "archived": client["archived"],
                          "address": client["address"],
                          "note": client["note"]}
            final_clients.append(tmp_client)
        return pd.DataFrame.from_records(final_clients)

    def handle(self, request: Any) -> None:
        clients = self.transform(request)
        super().set_next(self.handler)
        super().handle(clients)
