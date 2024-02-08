"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_tap_test_class, SuiteConfig

from tap_toggl.tap import TapToggl

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "api_token": os.environ["TAP_TOGGL_API_TOKEN"],
}

TEST_SUITE_CONFIG = SuiteConfig(
    ignore_no_records_for_streams=["projects", "tasks", "time_entries"]
)

TestTapToggl = get_tap_test_class(
    tap_class=TapToggl,
    config=SAMPLE_CONFIG,
    suite_config=TEST_SUITE_CONFIG,
)

# TODO: Create additional tests as appropriate for your tap.
