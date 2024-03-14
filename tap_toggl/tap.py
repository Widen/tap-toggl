"""Toggl tap class."""

from __future__ import annotations

from datetime import datetime

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_toggl import streams


class TapToggl(Tap):
    """Toggl tap class."""

    name = "tap-toggl"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_token",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the Toggl API",
        ),
        th.Property(
            "detailed_report_trailing_days",
            th.IntegerType,
            required=False,
            default=1,
            description="Provided for backwards compatibility. Does nothing.",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=False,
            default=datetime.now().strftime("%Y-%m-%d"),
            description="The earliest record date to sync. In the format YYYY-MM-DD.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.TogglStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.ClientsStream(self),
            streams.GroupsStream(self),
            streams.OrganizationsStream(self),
            streams.ProjectsStream(self),
            streams.TasksStream(self),
            streams.TagsStream(self),
            streams.TimeEntriesStream(self),
            streams.UsersStream(self),
            streams.WorkspacesStream(self),
        ]


if __name__ == "__main__":
    TapToggl.cli()
