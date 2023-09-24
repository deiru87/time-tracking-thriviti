import os

# MODEL PATH
URL_REPORT_API = os.getenv("URL_REPORT_API", "https://reports.api.clockify.me/v1/")
URL_BASE_API = os.getenv("URL_BASE_API", "https://api.clockify.me/api/v1/")
API_KEY = os.getenv("API_KEY", "OTIzYWJjOTUtYmUyMy00ZDgzLTlkMmItNGI4NjRjNjllMmQz")
API_KEY_HEADER = os.getenv("API_KEY_HEADER", "X-Api-Key")
USER_DB = os.getenv("USER_DB", "postgres")
PASS_DB = os.getenv("PASS_DB", "Deimer87")
IP_SERVER = os.getenv("IP_SERVER", "localhost:5434")
NAME_DB = os.getenv("NAME_DB", "thriviti")
START_DATE_RANGE = os.getenv("START_DATE_RANGE", "2020-01-01T00:00:00Z")
INSTANCE_UNIX_SOCKET = os.getenv("INSTANCE_UNIX_SOCKET", None)
NAME_PARAM_PAGE_SIZE = os.getenv("NAME_PARAM_PAGE_SIZE", "page-size")
PAGE_SIZE = os.getenv("PAGE_SIZE", 1000)
