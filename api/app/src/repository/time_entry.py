import math
import traceback
from datetime import datetime

from sqlalchemy import or_, and_, text, func, column, desc
from sqlalchemy.sql import select
from configuration.config import db
from model.time_entry import TimeEntry
from commons.schema import PageResponse


class TimeEntryRepository:

    @staticmethod
    async def get_all(
            page: int = 1,
            limit: int = 10,
            columns: str = None,
            filter: str = None
    ):

        query = select(from_obj=TimeEntry, columns="*")

        # select columns dynamically
        if columns is not None and columns != "all":
            # we need column format data like this --> [column(id),column(name),column(sex)...]

            query = select(from_obj=TimeEntry, columns=convert_columns(columns))

        # select filter dynamically
        if filter is not None and filter != "null":
            # we need filter format data like this  --> {'name': 'an','country':'an'}

            # convert string to dict format
            criteria = dict(x.split("=") for x in filter.split('*'))

            criteria_list = []
            new_criteria_list = []

            # check every key in dict. are there any table attributes that are the same as the dict key ?

            for attr, value in criteria.items():
                _attr = getattr(TimeEntry, attr)

                # filter format
                search = "%{}%".format(value)

                if attr == 'time_interval_start':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    new_criteria_list.append(_attr.__ge__(value))
                elif attr == 'time_interval_end':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    new_criteria_list.append(_attr.__le__(value))
                else:
                    criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))
            query = query.filter(and_(*new_criteria_list))

        # count query
        count_query = select(func.count(1)).select_from(query)
        query = query.order_by(desc(text('time_interval_end')))
        offset_page = page - 1
        # pagination
        query = (query.offset(offset_page * limit).limit(limit))

        # total record
        total_record = (await db.execute(count_query)).scalar() or 0

        # total page
        total_page = math.ceil(total_record / limit)

        # result
        result = (await db.execute(query)).fetchall()

        # Define a function to format datetime values
        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d') if dt else None

        # Create a list to hold the formatted results
        formatted_results = []

        # Iterate through the results and apply formatting
        for row in result:
            formatted_row = {
                column: format_datetime(getattr(row, column)) if isinstance(getattr(row, column),
                                                                            datetime) else getattr(row, column)

                for column in row.keys()
            }
            formatted_results.append(formatted_row)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=formatted_results
        )


def convert_columns(columns):
    """
    # seperate string using split ('-')
    new_columns = columns.split('-')

    # add to list with column format
    column_list = []
    for data in new_columns:
        column_list.append(data)

    # we use lambda function to make code simple

    """

    return list(map(lambda x: column(x), columns.split('-')))
