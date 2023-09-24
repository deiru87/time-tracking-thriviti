import uvicorn
from fastapi import FastAPI, Query

from commons.schema import ResponseSchema
from configuration.config import db
from repository.time_entry import TimeEntryRepository
from repository.consolidated import ConsolidatedRepository
from repository.consolidated_history import ConsolidatedHistoryRepository


def init_app():
    db.init()
    app = FastAPI(
        title="Thriviti time tracking",
        description="Api to get information about time entries and consolidated data",
        version="1"
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app


app = init_app()


@app.get("/time-entry", response_model=ResponseSchema)
async def get_all_time_entry(
        page: int = 1,
        limit: int = 50,
        columns: str = Query(None, alias="columns"),
        filter: str = Query(None, alias="filter")
):
    result = await TimeEntryRepository.get_all(page, limit, columns, filter)
    return ResponseSchema(detail="Successfully fetch time entries data!", result=result)


@app.get("/consolidated", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_consolidated(
        page: int = 1,
        limit: int = 50,
        columns: str = Query(None, alias="columns"),
        filter: str = Query(None, alias="filter")
):
    result = await ConsolidatedRepository.get_all(page, limit, columns, filter)
    return ResponseSchema(detail="Successfully fetch consolidated data!", result=result)


@app.get("/consolidated_history", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_consolidated_history(
        page: int = 1,
        limit: int = 50,
        columns: str = Query(None, alias="columns"),
        filter: str = Query(None, alias="filter")
):
    result = await ConsolidatedHistoryRepository.get_all(page, limit, columns, filter)
    return ResponseSchema(detail="Successfully fetch consolidated history data!", result=result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
