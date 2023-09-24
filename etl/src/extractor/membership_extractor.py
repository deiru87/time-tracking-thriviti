import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.membership_transformer import MembershipTransformerHandler
from util.row_data_processor import RowDataProcessor


logger = log.get_logger("membership-extractor-component")


class MembershipExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = MembershipTransformerHandler()

    @staticmethod
    def extract(workspace) -> dict:
        return workspace["memberships"]

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of memberships in thriviti time-tracking')
        membership_data = []
        for workspace in RowDataProcessor.workspaces_data:
            membership_data.extend(self.extract(workspace))
        RowDataProcessor.membership_data = membership_data
        super().set_next(self.handler)
        super().handle(membership_data)

