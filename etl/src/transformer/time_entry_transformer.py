import math

import pandas as pd

import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.time_entry_loader import TimeEntryLoaderHandler
from util.row_data_processor import RowDataProcessor

logger = log.get_logger("time-entry-transformer-component")


def get_first_client(clients, client_id):
    if client_id is None:
        return None
    matches = [c for c in clients if c["id"] == client_id]
    if matches:
        return matches[0]
    return None


def get_first_project(projects, project_id):
    matches = [p for p in projects if p["id"] == project_id]
    if matches:
        return matches[0]
    return None


def get_first_custom_field(custom_fields, custom_field_id):
    matches = [c for c in custom_fields if c["customFieldId"] == custom_field_id]
    if matches:
        return matches[0]
    return None


class TimeEntryTransformerHandler(AbstractHandler):

    def __init__(self):
        self.handler = TimeEntryLoaderHandler()

    @staticmethod
    def transform(time_entries) -> Any:
        final_time_entries = []
        cost_rate_amount = 0
        non_billing_value = ""
        subject_matter_value = ""
        for time_entry in time_entries:

            for member in RowDataProcessor.membership_data:
                if member["userId"] == time_entry["userId"]:
                    tmp_cost_rate = member["costRate"]["amount"] if member["costRate"] is not None else 0
                    cost_rate_amount = tmp_cost_rate / 100
                    break

            client_id = time_entry["clientId"] if "clientId" in time_entry else ""
            tmp_client = get_first_client(RowDataProcessor.client_data, client_id)
            tmp_project = get_first_project(RowDataProcessor.projects_data, time_entry["projectId"])
            custom_fields = time_entry["customFields"] if "customFields" in time_entry else []
            custom_field_client_call = get_first_custom_field(custom_fields, '64026290264092281bfacf2c')
            custom_field_subject_matter = get_first_custom_field(custom_fields, '6402662e21b9ba7d2f28df9d')
            custom_field_qbo_invoice = get_first_custom_field(custom_fields, '640fd413fb46041015eed4c2')
            custom_field_non_billing = get_first_custom_field(custom_fields, '64ab158389058175da6365d4')
            if custom_field_non_billing is not None and custom_field_non_billing["value"] is not None:
                non_billing_value = ''.join([str(elem) for elem in custom_field_non_billing["value"]])
            if custom_field_subject_matter is not None and custom_field_subject_matter["value"] is not None:
                subject_matter_value = ''.join([str(elem) for elem in custom_field_subject_matter["value"]])
            client_name = tmp_client["name"] if tmp_client is not None else ""
            amount = time_entry["amount"] / 100
            duration = time_entry["timeInterval"]["duration"] / 60 / 60
            cost = duration * cost_rate_amount
            datetime_start = pd.to_datetime(time_entry["timeInterval"]["start"]).tz_convert('America/Bogota')
            datetime_end = pd.to_datetime(time_entry["timeInterval"]["end"]).tz_convert('America/Bogota')
            tmp_time_entry = {"id": time_entry["_id"], "description": time_entry["description"],
                              "user_id": time_entry["userId"],
                              "user_name": time_entry["userName"],
                              "project_id": time_entry["projectId"],
                              "project_name": tmp_project["name"] if tmp_project is not None else "",
                              "client_id": client_id,
                              "client_name": client_name if client_name is not None else "",
                              "activity": time_entry["taskName"] if "taskName" in time_entry else "",
                              "quickbooks_invoice": custom_field_qbo_invoice["value"]
                              if custom_field_qbo_invoice is not None else "",
                              "client_call": custom_field_client_call["value"]
                              if custom_field_client_call is not None else "",
                              "non_billing_reason": non_billing_value,
                              "subject_matter": subject_matter_value,
                              "time_interval_start": datetime_start,
                              "time_interval_end": datetime_end,
                              "start_date": datetime_start.date(),
                              "start_time": datetime_start.time(),
                              "end_date": datetime_end.date(),
                              "end_time": datetime_end.time(),
                              "time_interval_duration": duration,
                              "billable": time_entry["billable"],
                              "amount": amount,
                              "cost": cost,
                              "profit": amount - cost,
                              "amount_rate": time_entry["rate"] / 100,
                              "cost_rate": cost_rate_amount}
            final_time_entries.append(tmp_time_entry)
        return pd.DataFrame.from_records(final_time_entries)

    def handle(self, request: Any) -> None:
        entries = self.transform(request)
        super().set_next(self.handler)
        super().handle(entries)
