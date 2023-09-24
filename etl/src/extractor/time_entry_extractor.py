import requests
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from transformer.time_entry_transformer import TimeEntryTransformerHandler
from util.row_data_processor import RowDataProcessor
from datetime import datetime
from zoneinfo import ZoneInfo
from configuration.env import URL_REPORT_API, API_KEY_HEADER, API_KEY, START_DATE_RANGE

logger = log.get_logger("time-entry-extractor-component")


class TimeEntryExtractorHandler(AbstractHandler):

    def __init__(self):
        self.handler = TimeEntryTransformerHandler()

    @staticmethod
    def extract(workspace) -> list[dict]:
        url = URL_REPORT_API + "workspaces/" + workspace["id"] + "/reports/detailed"
        headers = {API_KEY_HEADER: API_KEY, "Content-Type": "application/json"}
        page = 0
        results = True
        data = []
        request = {
            "dateRangeEnd": datetime.now(tz=ZoneInfo("UTC")).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "dateRangeStart": START_DATE_RANGE,
            "amounts": [
                "EARNED", "COST", "PROFIT"
            ],
            "detailedFilter": {
                "page": page,
                "pageSize": 100
            }
        }

        while results:
            results = requests.post(url, headers=headers, json=request).json()
            results = results["timeentries"]
            if results:
                data.extend(results)
            page += 1
            request["detailedFilter"]["page"] = page
        return data

    def handle(self, request: Any) -> None:
        logger.info('handle request to extract data of time-entries in thriviti time-tracking')
        time_entries_data = []
        for workspace in RowDataProcessor.workspaces_data:
            time_entries_data.extend(self.extract(workspace))
        super().set_next(self.handler)
        super().handle(time_entries_data)

