"""REST client handling, including TogglStream base class."""

from __future__ import annotations

import sys
from base64 import b64encode
from datetime import datetime
from typing import Any, Callable

import requests
from singer_sdk.pagination import BasePageNumberPaginator, BaseAPIPaginator
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


class TogglStream(RESTStream):
    """Toggl stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.track.toggl.com"

    records_jsonpath = "$[*]"

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        auth_str = bytes(f"{self.config.get('api_token')}:api_token", "utf-8")
        encoded_token = b64encode(auth_str).decode("ascii")
        headers = {"content-type": "application/json"}
        if "api_token" in self.config:
            headers["Authorization"] = f"Basic {encoded_token}"
        else:
            self.logger.error("No API token provided")
        return headers

    def start_time_to_epoch(self, start_time: str) -> int:
        """Convert a start time to an epoch time.

        Args:
            start_time: The start time.

        Returns:
            The epoch time.
        """
        utc_time = datetime.strptime(start_time, "%Y-%m-%d")
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
        return int(epoch_time)


class TogglPaginationStream(TogglStream):
    """Toggl stream class with pagination variation."""

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Get a fresh paginator for this API endpoint.

        Returns:
            A paginator instance.
        """
        return BasePageNumberPaginator(1)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if self.config.get("start_date") and self.name != "projects":
            params["since"] = self.start_time_to_epoch(self.config.get("start_date"))
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort_order"] = "asc"
            params["sort_field"] = self.replication_key
        return params
