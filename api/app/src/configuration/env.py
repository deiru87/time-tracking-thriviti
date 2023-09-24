import os


USER_DB = os.getenv("USER_DB", "postgres")
PASS_DB = os.getenv("PASS_DB", "Deimer87")
IP_SERVER = os.getenv("IP_SERVER", "localhost:5434")
NAME_DB = os.getenv("NAME_DB", "thriviti")
START_DATE_RANGE = os.getenv("START_DATE_RANGE", "2020-01-01T00:00:00Z")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", None)
