from collections.abc import AsyncGenerator
from typing import Annotated
from httpx import AsyncClient, Limits
from fastapi import Depends
from fastapi import FastAPI
import asyncio
from orb.clients import MessagesClient, ReportsClient
from orb.utils import calculate_message_cost
from orb.types import Usage, UsageResponse
from orb.settings import SETTINGS

app = FastAPI()


async def get_async_http_client() -> AsyncGenerator[AsyncClient]:
    """
    Create a http client.

    It is used as context manager, so that connection pool is reused. If this
    service is heavily used, it would make more sense to change lifespan of
    this to be bigger than one request, so that we don't have to reestablish
    connection every time.
    """
    # because we don't want to accidentally overwhelm reports service with our
    # requests, put a limit on the number of concurrent requests
    limits = Limits(max_keepalive_connections=5, max_connections=10)
    async with AsyncClient(limits=limits) as client:
        yield client


async def get_messages_client(
    http_client: Annotated[AsyncClient, Depends(get_async_http_client)],
) -> MessagesClient:
    return MessagesClient(SETTINGS.messages_service_url, http_client)


async def get_reports_client(
    http_client: Annotated[AsyncClient, Depends(get_async_http_client)],
) -> AsyncGenerator[ReportsClient]:
    reports_client = ReportsClient(SETTINGS.reports_service_url, http_client)
    yield reports_client


@app.get("/usage")
async def get_usage(
    messages_client: Annotated[MessagesClient, Depends(get_messages_client)],
    reports_client: Annotated[ReportsClient, Depends(get_reports_client)],
) -> UsageResponse:
    """Return usage information for all messages in current billing period."""
    messages = (await messages_client.get_current_period_messages()).messages
    report_ids = (message.report_id for message in messages if message.report_id)
    tasks = [reports_client.get_report_cost(report_id) for report_id in report_ids]
    reports = await asyncio.gather(*tasks)
    reports_map = {report.id: report for report in reports if report}
    usages = []
    for message in messages:
        report = reports_map.get(message.report_id, None)
        usages.append(
            Usage(
                message_id=message.id,
                timestamp=message.timestamp,
                report_name=report.name if report else None,
                # I would rather return it as Decimal not to deal with
                # prescision, but the schema is already "number"
                credits_used=float(calculate_message_cost(message, report)),
            )
        )
    return UsageResponse(usage=usages)
