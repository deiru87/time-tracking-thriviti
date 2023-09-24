import pandas as pd
import common.logs.logger as log
from typing import Any
from handler.abstract_handler import AbstractHandler
from loader.project_loader import ProjectLoaderHandler

logger = log.get_logger("client-transformer-component")


class ProjectTransformerHandler(AbstractHandler):

    def __init__(self):
        self.handler = ProjectLoaderHandler()

    @staticmethod
    def transform(projects) -> Any:
        final_projects = []
        for project in projects:
            idx_pt = project["duration"].find("PT")
            idx_hour = project["duration"].find("H")
            idx_min = project["duration"].find("M")
            idx_sec = project["duration"].find("S")
            duration_h = float(project["duration"][idx_pt + len("PT"): idx_hour]) if idx_pt > -1 and idx_hour > -1 else 0
            duration_m = float(int(project["duration"][idx_hour + len("H"): idx_min]) / 60) if idx_hour > -1 and idx_min > -1 else 0
            duration_s = float(int(project["duration"][idx_min + len("M"): idx_sec]) / 3600) if idx_min > -1 and idx_sec > -1 else 0
            duration = duration_h + duration_m + duration_s

            idx_pt = project["timeEstimate"]["estimate"].find("PT")
            idx_hour = project["timeEstimate"]["estimate"].find("H")
            idx_min = project["timeEstimate"]["estimate"].find("M")
            idx_sec = project["timeEstimate"]["estimate"].find("S")
            t_estimate_h = float(project["timeEstimate"]["estimate"][idx_pt + len("PT"): idx_hour]) if idx_pt > -1 and idx_hour > -1 else 0
            t_estimate_m = float(int(project["timeEstimate"]["estimate"][idx_hour + len("H"): idx_min]) / 60) if idx_hour > -1 and idx_min > -1 else 0
            t_estimate_s = float(int(project["timeEstimate"]["estimate"][idx_min + len("M"): idx_sec]) / 3600) if idx_min > -1 and idx_sec > -1 else 0
            time_estimate = t_estimate_h + t_estimate_m + t_estimate_s

            tmp_project = {"id": project["id"], "name": project["name"],
                           "hourly_rate_amount": project["hourlyRate"]["amount"]
                           if project["hourlyRate"] is not None else "",
                           "hourly_rate_currency": project["hourlyRate"]["currency"]
                           if project["hourlyRate"] is not None else "",
                           "client_id": project["clientId"],
                           "workspace_id": project["workspaceId"],
                           "duration": duration,
                           "time_estimate": time_estimate,
                           "time_estimate_type": project["timeEstimate"]["type"],
                           "time_estimate_active": project["timeEstimate"]["active"],
                           "billable": project["billable"],
                           "archived": project["archived"],
                           "public": project["public"]}
            final_projects.append(tmp_project)
        return pd.DataFrame.from_records(final_projects)

    def handle(self, request: Any) -> None:
        projects = self.transform(request)
        super().set_next(self.handler)
        super().handle(projects)
