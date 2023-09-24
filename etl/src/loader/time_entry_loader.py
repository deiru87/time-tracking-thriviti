
import common.logs.logger as log
from pandas import DataFrame
from typing import Any
from sqlalchemy import create_engine
from handler.abstract_handler import AbstractHandler
from loader.consolidate_loader import ConsolidateLoaderHandler
from configuration.env import NAME_DB, PASS_DB, USER_DB, IP_SERVER, INSTANCE_UNIX_SOCKET

logger = log.get_logger("time-entry-loader-component")


class TimeEntryLoaderHandler(AbstractHandler):

    def __init__(self):
        self.handler = ConsolidateLoaderHandler()

    @staticmethod
    def loader(workspaces: DataFrame) -> None:
        logger.info('saving TimeEntries data in database')
        url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB
        try:
            if INSTANCE_UNIX_SOCKET:
                url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB + "?host=" + INSTANCE_UNIX_SOCKET
            engine = create_engine(url_db)
            final_df = workspaces.drop_duplicates(keep='first')
            with engine.connect() as conn:
                final_df.to_sql(con=conn, index=False, name='time_entry', if_exists='replace')
        except Exception as error:
            logger.error(error)

    def handle(self, request: Any) -> None:
        self.loader(request)
        logger.info("finish persistence of time entries in DB")
        super().set_next(self.handler)
        super().handle(request)
