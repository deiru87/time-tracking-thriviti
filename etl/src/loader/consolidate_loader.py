
import common.logs.logger as log
import pandas as pd
from typing import Any
from sqlalchemy import create_engine, inspect, text
from handler.abstract_handler import AbstractHandler
from loader.consolidate_hist_loader import ConsolidateHistLoaderHandler
from configuration.env import NAME_DB, PASS_DB, USER_DB, IP_SERVER, INSTANCE_UNIX_SOCKET

logger = log.get_logger("consolidate-loader-component")


class ConsolidateLoaderHandler(AbstractHandler):
    
    def __init__(self):
        self.handler = ConsolidateHistLoaderHandler()
        
    @staticmethod
    def loader() -> None:
        logger.info('saving consolidated of data in database')
        df_db = pd.DataFrame()
        url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB
        try:
            if INSTANCE_UNIX_SOCKET:
                url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB + "?host=" + INSTANCE_UNIX_SOCKET
            engine = create_engine(url_db)
            with engine.connect() as conn:
                query = "select " \
                        "t.project_id," \
                        "(select name from project where id = t.project_id) as project_name," \
                        "(select name from client where id = t.client_id) as client_name," \
                        "date_trunc('DAY', t.time_interval_end at time zone '00') as date," \
                        "cast(SUM(CASE WHEN t.billable = true THEN t.time_interval_duration ELSE 0 END) as float ) AS "\
                        "hours_billable,"\
                        "cast(SUM(CASE WHEN t.billable = false THEN t.time_interval_duration ELSE 0 END) as float ) " \
                        "AS hours_unbillable,"\
                        "(select time_estimate from project where id = t.project_id) as budgeted_time," \
                        "(select duration from project where id = t.project_id) as current_spent_time," \
                        "sum(t.amount) as amount, " \
                        "sum(t.cost) as cost, " \
                        "sum(t.profit) as profit, " \
                        "max(t.amount_rate) as amount_rate, " \
                        "max(t.cost_rate) as cost_rate " \
                        "from time_entry t " \
                        "group by t.project_id, t.client_id, date_trunc('DAY', t.time_interval_end at time zone '00')" \
                        "order by date desc"
                if inspect(conn).has_table('time_entry'):
                    df_db = pd.read_sql_query(sql=text(query), con=conn)

                with engine.connect() as new_conn:
                    df_db.to_sql(con=new_conn, index=False, name='consolidated', if_exists='replace')

        except Exception as error:
            logger.error(error)

    def handle(self, request: Any) -> None:
        self.loader()
        logger.info("finish persistence of consolidated data in DB")
        super().set_next(self.handler)
        super().handle(request)
