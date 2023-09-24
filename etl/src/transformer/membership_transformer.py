import pandas as pd
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.membership_loader import MembershipLoaderHandler

logger = log.get_logger("membership-transformer-component")


class MembershipTransformerHandler(AbstractHandler):

    def __init__(self):
        self.handler = MembershipLoaderHandler()

    @staticmethod
    def transform(memberships) -> Any:
        final_clients = []
        for membership in memberships:
            tmp_client = {
                          "hourly_rate_amount": membership["hourlyRate"]["amount"]
                          if membership["hourlyRate"] is not None else "",
                          "hourly_rate_currency": membership["hourlyRate"]["currency"]
                          if membership["hourlyRate"] is not None else "",
                          "cost_rate_amount": membership["costRate"]["amount"]
                          if membership["costRate"] is not None else "",
                          "cost_rate_currency": membership["costRate"]["currency"]
                          if membership["costRate"] is not None else "",
                          "status": True if membership["membershipStatus"] == 'ACTIVE' else False,
                          "membership_type": membership["membershipType"],
                          "user_id": membership["userId"],
                          "workspace_id": membership["targetId"]}
            final_clients.append(tmp_client)
        return pd.DataFrame.from_records(final_clients)

    def handle(self, request: Any) -> None:
        memberships = self.transform(request)
        super().set_next(self.handler)
        super().handle(memberships)
