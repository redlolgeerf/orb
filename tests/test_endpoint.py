import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from orb.main import app, get_messages_client, get_reports_client
from orb.types import CurrentPeriodReport, MessageCost, ReportCost, UsageResponse, Usage


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def current_period_report():
    return CurrentPeriodReport(
        messages=[
            MessageCost(
                id=123, text="foo", timestamp="2024-04-29T10:22:13.926Z", report_id=None
            ),
            MessageCost(
                id=124, text="bar", timestamp="2024-04-29T14:33:22.741Z", report_id=1
            ),
        ]
    )


@pytest.fixture
def report_cost() -> ReportCost:
    return ReportCost(
        id=1,
        name="report",
        credit_cost=10,
    )


@pytest.fixture
def messages_client(current_period_report):
    client = AsyncMock()
    client.get_current_period_messages = AsyncMock(return_value=current_period_report)
    return client


@pytest.fixture
def reports_client(report_cost):
    client = AsyncMock()
    client.get_report_cost = AsyncMock(return_value=report_cost)
    return client


@pytest.fixture
def override_get_messages_client(messages_client):
    async def get_client():
        return messages_client

    app.dependency_overrides[get_messages_client] = get_client
    yield
    app.dependency_overrides.pop(get_messages_client, None)


@pytest.fixture
def override_get_reports_client(reports_client):
    async def get_client():
        return reports_client

    app.dependency_overrides[get_reports_client] = get_client
    yield
    app.dependency_overrides.pop(get_reports_client, None)


@pytest.fixture
def expected_usage() -> UsageResponse:
    return UsageResponse(
        usage=[
            Usage(
                message_id=123,
                report_name=None,
                timestamp="2024-04-29T10:22:13.926Z",
                credits_used=1,
            ),
            Usage(
                message_id=124,
                report_name="report",
                timestamp="2024-04-29T14:33:22.741Z",
                credits_used=10,
            ),
        ]
    )


@pytest.mark.usefixtures("override_get_messages_client", "override_get_reports_client")
def test__get_usage(client: TestClient, expected_usage):
    response = client.get("/usage")
    assert response.status_code == 200
    assert response.json() == expected_usage.model_dump()
