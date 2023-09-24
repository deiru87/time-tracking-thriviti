import common.logs.logger as log
import pandas as pd
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.workspace_loader import WorkspaceLoaderHandler

logger = log.get_logger("workspace-transformer-component")


class WorkspaceTransformerHandler(AbstractHandler):

    def __init__(self):
        self.workspace_loader = WorkspaceLoaderHandler()

    @staticmethod
    def transform(workspaces: list) -> Any:
        final_workspaces = []
        for workspace in workspaces:
            tmp_workspace = {"id": workspace["id"], "name": workspace["name"],
                             "hourly_rate_amount": workspace["hourlyRate"]["amount"],
                             "hourly_rate_currency": workspace["hourlyRate"]["currency"],
                             "cost_rate_amount": workspace["costRate"]["amount"],
                             "cost_rate_currency": workspace["costRate"]["currency"]}
            final_workspaces.append(tmp_workspace)
        return pd.DataFrame.from_records(final_workspaces)

    def handle(self, request: Any) -> None:
        workspaces = self.transform(request)
        super().set_next(self.workspace_loader)
        super().handle(workspaces)