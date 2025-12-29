from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

import requests
from google.transit import gtfs_realtime_pb2

from app.config import settings


class MtaRealtimeClient:
    def __init__(self, api_key: str, feed_url: str) -> None:
        self.api_key = api_key
        self.feed_url = feed_url

    def fetch_feed(self) -> gtfs_realtime_pb2.FeedMessage | None:
        if not self.api_key:
            return None
        response = requests.get(
            self.feed_url,
            headers={settings.mta_api_key_header: self.api_key},
            timeout=settings.request_timeout_seconds,
        )
        response.raise_for_status()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed


def summarize_vehicle_counts(
    feed: gtfs_realtime_pb2.FeedMessage,
) -> tuple[Counter, str | None]:
    vehicle_counts: Counter[str] = Counter()
    timestamp: str | None = None
    if feed.header.timestamp:
        timestamp = datetime.fromtimestamp(
            feed.header.timestamp, tz=timezone.utc
        ).isoformat()
    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue
        route_id = entity.vehicle.trip.route_id
        if route_id:
            vehicle_counts[route_id] += 1
    return vehicle_counts, timestamp
