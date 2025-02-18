"""
Representation of different data structures used.
"""

from pydantic import BaseModel


class ReportCost(BaseModel):
    """Response of /reports endpoint"""

    # report id
    id: int
    # report name
    name: str
    # report cost in credits
    credit_cost: int


class MessageCost(BaseModel):
    """Representation of a message"""

    # message id
    id: int
    # message text
    text: str
    #
    timestamp: str
    # report id
    report_id: int | None = None


class CurrentPeriodReport(BaseModel):
    """Response of /current-preriod endpoint"""

    messages: list[MessageCost]


class Usage(BaseModel):
    """Representation of a usage cost per message"""

    # message id
    message_id: int
    timestamp: str
    # report name
    report_name: str | None
    # usage cost in credits
    credits_used: float


class UsageResponse(BaseModel):
    """Response of our /usage endpoint"""

    usage: list[Usage]
