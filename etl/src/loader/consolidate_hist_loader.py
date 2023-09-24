import common.logs.logger as log
import pandas as pd
from typing import Any
from sqlalchemy import create_engine, inspect, text, MetaData, Table, Column, String, DATETIME, DECIMAL
from handler.abstract_handler import AbstractHandler
from configuration.env import NAME_DB, PASS_DB, USER_DB, IP_SERVER, INSTANCE_UNIX_SOCKET

logger = log.get_logger("consolidate-hist-loader-component")


def get_connection() -> Any:
    url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB
    if INSTANCE_UNIX_SOCKET:
        url_db = "postgresql+psycopg2://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB + "?host=" + INSTANCE_UNIX_SOCKET
    return create_engine(url_db)


def get_history_table():
    sample_metadata = MetaData()
    consolidated_history = Table(
        'consolidated_history', sample_metadata,
        Column('project_id', String),
        Column('project_name', String),
        Column('client_name', String),
        Column('date', DATETIME),
        Column('hours', DECIMAL),
        Column('budgeted_time', DECIMAL),
        Column('current_spent_time', DECIMAL),
        Column('amount', DECIMAL),
        Column('cost', DECIMAL),
        Column('profit', DECIMAL),
    )
    return consolidated_history


def delete_dummy_records() -> None:
    try:
        engine = get_connection()
        with engine.begin() as conn:
            conn.execute(text('DELETE FROM consolidated_history WHERE date = (select date_trunc(\'DAY\', now() at '
                              'time zone \'America/Bogota\'))'))
    except Exception as error:
        logger.error(error)


class ConsolidateHistLoaderHandler(AbstractHandler):

    @staticmethod
    def loader() -> Any:
        logger.info('saving consolidated history  data in database')
        df_db = pd.DataFrame()
        is_delta = False
        result_data = None
        final_data = None
        try:
            engine = get_connection()
            with engine.connect() as conn:
                query = "select * from consolidated order by date desc"
                if inspect(conn).has_table('consolidated'):
                    df_db = pd.read_sql_query(sql=text(query), con=conn)

                with engine.connect() as new_conn:
                    try:
                        df_db.to_sql(con=new_conn, index=False, name='consolidated_history', if_exists='fail')
                    except:
                        is_delta = True
                        query_target = "select * from consolidated_history order by date desc"
                        df_db_hist = pd.read_sql_query(sql=text(query_target), con=conn)
                    if is_delta:
                        with engine.connect() as tmp_conn:
                            query_delta = "select c.* from consolidated c where not exists "\
                                "(select * from consolidated_history ch where ch.project_id=c.project_id and " \
                                          "ch.date=c.date and ch.hours_billable=c.hours_billable)"
                            last_data = pd.read_sql_query(sql=text(query_delta), con=tmp_conn)
                            result_data = last_data
                            df_db_hist = df_db_hist.drop_duplicates(keep='first')
                            delta_data = pd.concat([df_db_hist, last_data])
                            delta_data = delta_data.sort_values(by=['date', 'hours_billable'], ignore_index=True,
                                                                ascending=False)
                            final_data = delta_data.drop_duplicates(subset=['project_id', 'date'], keep='first')

            if final_data is not None:
                with engine.connect() as def_conn:
                    final_data.to_sql(con=def_conn, index=False, name='consolidated_history', if_exists='replace')

            return result_data

        except Exception as error:
            logger.error(error)

    @staticmethod
    def complete_loader(delta_data) -> None:

        if delta_data is None or delta_data.size <= 0:
            return
        try:
            engine = get_connection()
            with engine.connect() as tmp_conn:
                query = "select p.id as project_id," \
                        "p.name as project_name," \
                        "(select name from client where id = p.client_id) as client_name," \
                        "p.duration as duration," \
                        "p.time_estimate as time_estimate," \
                        "(select date_trunc('DAY', now() at time zone 'America/Bogota') as date)" \
                        "from project p where archived = false"
                df_db = pd.read_sql_query(sql=text(query), con=tmp_conn)

            records = []
            for idx in df_db.index:

                if delta_data.loc[(delta_data['project_id'] == df_db["project_id"][idx]) &
                                  (delta_data['date'] == df_db["date"][idx])].empty is True:
                    records.extend([{"project_id": df_db["project_id"][idx], "project_name": df_db["project_name"][idx],
                                     "client_name": df_db["client_name"][idx], "date": df_db["date"][idx],
                                     "hours_billable": 0,
                                     "hours_unbillable": 0,
                                     "budgeted_time": df_db["time_estimate"][idx],
                                     "current_spent_time": df_db["duration"][idx], "amount": 0, "cost": 0, "profit": 0,
                                     "amount_rate": 0, "cost_rate": 0}])

            ultimate_consolidation = pd.DataFrame(records)
            ultimate_consolidation = ultimate_consolidation.sort_values(by=['date', 'hours_billable'],
                                                                        ignore_index=True, ascending=False)
            ultimate_consolidation = ultimate_consolidation.drop_duplicates(keep='first')

            with engine.connect() as ultimate_conn:
                ultimate_consolidation.to_sql(con=ultimate_conn, index=False, name='consolidated_history',
                                              if_exists='append')
        except Exception as error:
            logger.error(error)

    def handle(self, request: Any) -> None:
        delete_dummy_records()
        delta_data = self.loader()
        self.complete_loader(delta_data)
        logger.info("finish persistence of consolidated history data in DB")
