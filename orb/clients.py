"""Http clients for calling other services"""

from httpx import AsyncClient
from orb.types import CurrentPeriodReport, ReportCost


class MessagesClient:
    """
    Client for calling "messages" service.
    """

    def __init__(self, base_url: str, client: AsyncClient):
        self.base_url = base_url
        self.client = client

    async def get_current_period_messages(self) -> CurrentPeriodReport:
        r = await self.client.get(f"{self.base_url}/current-period")
        r.raise_for_status()
        print(type(r.content), r.content)
        return CurrentPeriodReport.model_validate_json(r.content)


class ReportsClient:
    """
    Client for calling "reports" service.
    """

    def __init__(self, base_url: str, client: AsyncClient):
        self.base_url = base_url
        self.client = client

    async def get_report_cost(self, report_id: int) -> ReportCost | None:
        r = await self.client.get(f"{self.base_url}/{report_id}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return ReportCost.model_validate_json(r.content)
