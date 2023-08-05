import os

from typing import Any, Dict
from enum import Enum

from mixpanel import Mixpanel, MixpanelException


MIXPANEL_ALLOWED_ENVS = ["dev", "staging", "production"]


class TrackingSource(Enum):
    API = 0
    CLI = 1


class UserTrackingException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)


def _as_string(src: TrackingSource) -> str:
    return {TrackingSource.API: "api", TrackingSource.CLI: "cli"}[src]


def log_event(
    source: TrackingSource, user_name: str, customer: str, event_name: str, event_data: Dict[str, Any]
) -> None:
    if os.environ.get("MIXPANEL_ENV") not in MIXPANEL_ALLOWED_ENVS:
        return

    tracker = Mixpanel("971745954800ddbc7ca6ad5ff049c935")
    event_data["source"] = _as_string(source)
    try:
        tracker.track(f"{user_name}@{customer}", event_name, event_data)
    except MixpanelException as mxe:
        raise UserTrackingException(str(mxe))
