class RowDataProcessor(object):
    instance = None
    workspaces_data = None
    projects_data = None
    membership_data = None
    client_data = None
    custom_fields_data = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RowDataProcessor, cls).__new__(cls)
        return cls.instance

    def get_workspaces_data(self):
        return self.workspaces_data

    def get_projects_data(self):
        return self.projects_data

    def get_memberships_data(self):
        return self.membership_data

    def get_client_data(self):
        return self.client_data

    def get_custom_fields_data(self):
        return self.custom_fields_data
