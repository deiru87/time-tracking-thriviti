from typing import Any
from extractor.workspace_extractor import WorkspaceExtractorHandler
from extractor.user_extractor import UserExtractorHandler
from extractor.client_extractor import ClientExtractorHandler
from extractor.membership_extractor import MembershipExtractorHandler
from extractor.project_extractor import ProjectExtractorHandler
from extractor.task_extractor import TaskExtractorHandler
from extractor.time_entry_extractor import TimeEntryExtractorHandler
from handler.handler import Handler


def execute(handler: Handler, request: Any):
    handler.handle(request)


if __name__ == "__main__":
    workspace_extractor = WorkspaceExtractorHandler()
    user_extractor = UserExtractorHandler()
    client_extractor = ClientExtractorHandler()
    membership_extractor = MembershipExtractorHandler()
    project_extractor = ProjectExtractorHandler()
    task_extractor = TaskExtractorHandler()
    time_entry_extractor = TimeEntryExtractorHandler()
    execute(workspace_extractor, None)
    execute(user_extractor, None)
    execute(client_extractor, None)
    execute(membership_extractor, None)
    execute(project_extractor, None)
    execute(task_extractor, None)
    execute(time_entry_extractor, None)




