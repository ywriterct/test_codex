from pydantic import BaseModel, Field


class RouteSuggestion(BaseModel):
    route_id: str = Field(..., description="GTFS route identifier")
    vehicle_count: int = Field(..., ge=0, description="Active vehicles observed in feed")
    quiet_score: float = Field(..., ge=0, le=1, description="Higher is quieter")
    rationale: str = Field(..., description="Explanation for the score")


class QuietRouteResponse(BaseModel):
    origin: str
    destination: str
    data_timestamp: str | None
    warnings: list[str]
    suggestions: list[RouteSuggestion]
