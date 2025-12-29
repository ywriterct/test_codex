from urllib.parse import urlencode

from fastapi import FastAPI, Query

from app.config import settings
from app.models import QuietRouteResponse, RouteSuggestion
from app.services.mta import MtaRealtimeClient, summarize_vehicle_counts

app = FastAPI(title="Quiet Routes Navigator")


@app.get("/quiet-routes", response_model=QuietRouteResponse)
def quiet_routes(
    origin: str = Query(..., description="Human-readable origin description"),
    destination: str = Query(..., description="Human-readable destination description"),
    max_routes: int = Query(5, ge=1, le=20),
) -> QuietRouteResponse:
    warnings: list[str] = []
    trip_planner_url = "https://new.mta.info/plan?{}".format(
        urlencode({"from": origin, "to": destination})
    )
    client = MtaRealtimeClient(settings.mta_api_key, settings.mta_feed_url)
    feed = client.fetch_feed()
    if feed is None:
        warnings.append(
            "MTA_API_KEY is not set; returning empty suggestions. "
            "Provide a valid MTA API key to enable live route scoring."
        )
        return QuietRouteResponse(
            origin=origin,
            destination=destination,
            data_timestamp=None,
            warnings=warnings,
            suggestions=[],
        )

    vehicle_counts, timestamp = summarize_vehicle_counts(feed)
    if not vehicle_counts:
        warnings.append(
            "No vehicle positions were found in the realtime feed. "
            "Route scoring may be unavailable for this feed."
        )
    warnings.append(
        "Directions are provided via the MTA trip planner link. "
        "This API does not compute stop-by-stop routing yet."
    )

    suggestions: list[RouteSuggestion] = []
    for route_id, count in vehicle_counts.most_common():
        quiet_score = round(1 / (count + 1), 3)
        suggestions.append(
            RouteSuggestion(
                route_id=route_id,
                vehicle_count=count,
                quiet_score=quiet_score,
                rationale=(
                    "Lower active vehicle counts typically indicate fewer trains "
                    "and potentially quieter conditions."
                ),
                trip_planner_url=trip_planner_url,
            )
        )
    suggestions = sorted(suggestions, key=lambda item: item.quiet_score, reverse=True)[
        :max_routes
    ]

    return QuietRouteResponse(
        origin=origin,
        destination=destination,
        data_timestamp=timestamp,
        warnings=warnings,
        suggestions=suggestions,
    )
