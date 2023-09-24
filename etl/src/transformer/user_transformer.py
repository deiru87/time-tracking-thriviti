import pandas as pd
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.user_loader import UserLoaderHandler

logger = log.get_logger("user-transformer-component")


class UserTransformerHandler(AbstractHandler):

    def __init__(self):
        self.handler = UserLoaderHandler()

    @staticmethod
    def transform(users) -> Any:
        final_users = []
        for user in users:
            tmp_user = {"id": user["id"], "name": user["name"],
                        "email": user["email"],
                        "active_workspace": user["activeWorkspace"],
                        "default_workspace": user["defaultWorkspace"],
                        "setting_week_start": user["settings"]["weekStart"]
                        if user["settings"] is not None and user["settings"]["weekStart"] is not None else "",
                        "setting_week_time_zone": user["settings"]["timeZone"]
                        if user["settings"] is not None and user["settings"]["timeZone"] is not None else "",
                        "setting_start_day": user["settings"]["myStartOfDay"]
                        if user["settings"] is not None and user["settings"]["myStartOfDay"] is not None else "",
                        "status": user["status"]}
            final_users.append(tmp_user)
        return pd.DataFrame.from_records(final_users)

    def handle(self, request: Any) -> None:
        users = self.transform(request)
        super().set_next(self.handler)
        super().handle(users)
