
import common.logs.logger as log
from pandas import DataFrame
from typing import Any
from sqlalchemy import create_engine
from handler.abstract_handler import AbstractHandler
from configuration.env import NAME_DB, PASS_DB, USER_DB, IP_SERVER, INSTANCE_UNIX_SOCKET

logger = log.get_logger("task-loader-component")


class TaskLoaderHandler(AbstractHandler):

    @staticmethod
    def loader(workspaces: DataFrame) -> None:
        logger.info('saving Tasks data in database')
        url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB
        try:
            if INSTANCE_UNIX_SOCKET:
                url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB  + "?host=" + INSTANCE_UNIX_SOCKET
            engine = create_engine(url_db)
            with engine.connect() as conn:
                workspaces.to_sql(con=conn, index=False, name='task', if_exists='replace')
        except Exception as error:
            logger.error(error)

    def handle(self, request: Any) -> None:
        self.loader(request)
        logger.info("finish persistence of tasks in DB")
