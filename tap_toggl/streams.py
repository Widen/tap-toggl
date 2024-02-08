"""Stream type classes for tap-toggl."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th

from tap_toggl.client import TogglStream, TogglPaginationStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


class ClientsStream(TogglStream):
    """Define custom stream."""

    name = "clients"
    path = "/me/clients"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("archived", th.BooleanType),
        th.Property("at", th.DateTimeType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("server_deleted_at", th.DateTimeType),
        th.Property("wid", th.IntegerType),
    ).to_dict()


class OrganizationsStream(TogglStream):
    """Define custom stream."""

    name = "organizations"
    path = "/me/organizations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("admin", th.BooleanType),
        th.Property("at", th.DateTimeType),
        th.Property("created_at", th.DateTimeType),
        th.Property("id", th.IntegerType),
        th.Property("is_multi_workspace_enabled", th.BooleanType),
        th.Property("is_unified", th.BooleanType),
        th.Property("max_data_retention_days", th.IntegerType),
        th.Property("max_workspaces", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("owner", th.BooleanType),
        # th.Property("payment_methods", th.ArrayType(th.ObjectType())),
        th.Property("permissions", th.StringType),
        th.Property("pricing_plan_id", th.IntegerType),
        th.Property("server_deleted_at", th.DateTimeType),
        th.Property("suspended_at", th.DateTimeType),
        th.Property("trial_info", th.ObjectType(
            th.Property("last_pricing_plan_id", th.IntegerType),
            th.Property("next_payment_date", th.DateTimeType),
            th.Property("trial", th.BooleanType),
            th.Property("trial_available", th.BooleanType),
            th.Property("trial_end_date", th.DateTimeType),
        )),
        th.Property("user_count", th.IntegerType),
    ).to_dict()

    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "organization_id": record["id"],
        }


class GroupsStream(TogglStream):
    """Define custom stream."""

    parent_stream_type = OrganizationsStream
    name = "groups"
    path = "/organizations/{organization_id}/groups"
    primary_keys: t.ClassVar[list[str]] = ["group_id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("at", th.DateTimeType),
        th.Property("group_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("permissions", th.StringType),
        th.Property("organization_id", th.IntegerType),
        th.Property("users", th.ArrayType(th.ObjectType(
            th.Property("avatar_url", th.StringType),
            th.Property("joined", th.BooleanType),
            th.Property("name", th.StringType),
            th.Property("user_id", th.IntegerType),
        ))),
        th.Property("workspaces", th.ArrayType(th.IntegerType)),
    ).to_dict()


class UsersStream(TogglPaginationStream):
    """Define custom stream."""

    parent_stream_type = OrganizationsStream
    name = "users"
    path = "/organizations/{organization_id}/users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("admin", th.BooleanType),
        th.Property("avatar_url", th.StringType),
        th.Property("can_edit_email", th.BooleanType),
        th.Property("email", th.StringType),
        th.Property("groups", th.ArrayType(th.ObjectType(
            th.Property("group_id", th.IntegerType),
            th.Property("name", th.StringType),
        ))),
        th.Property("id", th.IntegerType),
        th.Property("inactive", th.BooleanType),
        th.Property("invitation_code", th.StringType),
        th.Property("joined", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("owner", th.BooleanType),
        th.Property("organization_id", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("workspaces", th.ArrayType(th.ObjectType(
            th.Property("admin", th.BooleanType),
            th.Property("inactive", th.BooleanType),
            th.Property("name", th.StringType),
            th.Property("role", th.StringType),
            th.Property("workspace_id", th.IntegerType),
        ))),
    ).to_dict()

    def get_url_params(
            self,
            context: dict | None,  # noqa: ARG002
            next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
            params["sort_dir"] = "asc"
        return params


class WorkspacesStream(TogglStream):
    """Define custom stream."""

    # parent_stream_type = OrganizationsStream
    name = "workspaces"
    path = "/me/workspaces"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("admin", th.BooleanType),
        th.Property("at", th.DateTimeType),
        th.Property("business_ws", th.BooleanType),
        th.Property("csv_upload", th.ArrayType(th.ObjectType())),
        th.Property("default_currency", th.StringType),
        th.Property("default_hourly_rate", th.NumberType),
        th.Property("hide_start_end_times", th.BooleanType),
        th.Property("ical_enabled", th.BooleanType),
        th.Property("ical_url", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("last_modified", th.DateTimeType),
        th.Property("logo_url", th.StringType),
        th.Property("max_data_retention_days", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("only_admins_may_create_projects", th.BooleanType),
        th.Property("only_admins_may_create_tags", th.BooleanType),
        th.Property("only_admins_see_billable_rates", th.BooleanType),
        th.Property("only_admins_see_team_dashboard", th.BooleanType),
        th.Property("organization_id", th.IntegerType),
        th.Property("permissions", th.StringType),
        th.Property("premium", th.BooleanType),
        th.Property("profile", th.IntegerType),
        th.Property("projects_billable_by_default", th.BooleanType),
        th.Property("projects_private_by_default", th.BooleanType),
        th.Property("rate_last_updated", th.DateTimeType),
        th.Property("reports_collapse", th.BooleanType),
        th.Property("role", th.StringType),
        th.Property("rounding", th.IntegerType),
        th.Property("rounding_minutes", th.IntegerType),
        th.Property("server_deleted_at", th.DateTimeType),
        th.Property("suspended_at", th.DateTimeType),
        th.Property("te_constraints", th.ObjectType(
            th.Property("description_present", th.BooleanType),
            th.Property("project_present", th.BooleanType),
            th.Property("tag_present", th.BooleanType),
            th.Property("task_present", th.BooleanType),
            th.Property("time_entry_constraints_enabled", th.BooleanType),
        )),
        th.Property("working_hours_in_minutes", th.IntegerType),
    ).to_dict()

    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "workspace_id": record["id"],
        }


class ProjectsStream(TogglPaginationStream):
    """Define custom stream."""

    parent_stream_type = WorkspacesStream
    name = "projects"
    path = "/workspaces/{workspace_id}/projects"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("actual_hours", th.IntegerType),
        th.Property("actual_seconds", th.IntegerType),
        th.Property("at", th.DateTimeType),
        th.Property("auto_estimates", th.BooleanType),
        th.Property("billable", th.BooleanType),
        th.Property("cid", th.IntegerType),
        th.Property("client_id", th.IntegerType),
        th.Property("color", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("currency", th.StringType),
        th.Property("current_period", th.ObjectType(
            th.Property("end_date", th.DateTimeType),
            th.Property("start_date", th.DateTimeType),
        )),
        th.Property("end_date", th.DateTimeType),
        th.Property("estimated_hours", th.IntegerType),
        th.Property("estimated_seconds", th.IntegerType),
        th.Property("fixed_fee", th.NumberType),
        th.Property("id", th.IntegerType),
        th.Property("is_private", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("permissions", th.StringType),
        th.Property("rate", th.NumberType),
        th.Property("rate_last_updated", th.DateTimeType),
        th.Property("recurring", th.BooleanType),
        th.Property("recurring_parameters", th.ArrayType(th.ObjectType(
            th.Property("custom_period", th.IntegerType),
            th.Property("estimated_seconds", th.IntegerType),
            th.Property("parameter_end_date", th.DateTimeType),
            th.Property("parameter_start_date", th.DateTimeType),
            th.Property("period", th.StringType),
            th.Property("project_start_date", th.DateTimeType),
        ))),
        th.Property("server_deleted_at", th.DateTimeType),
        th.Property("start_date", th.DateTimeType),
        th.Property("status", th.StringType),
        th.Property("template", th.BooleanType),
        th.Property("template_id", th.IntegerType),
        th.Property("wid", th.IntegerType),
        th.Property("workspace_id", th.IntegerType),
    ).to_dict()


class TasksStream(TogglPaginationStream):
    """Define custom stream."""

    parent_stream_type = WorkspacesStream
    name = "tasks"
    path = "/workspaces/{workspace_id}/tasks"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    records_jsonpath = "$.data[*]"
    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("at", th.DateTimeType),
        th.Property("estimated_seconds", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("project_id", th.IntegerType),
        th.Property("recurring", th.BooleanType),
        th.Property("server_deleted_at", th.DateTimeType),
        th.Property("tracked_seconds", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("workspace_id", th.IntegerType),
    ).to_dict()


class TagsStream(TogglStream):
    """Define custom stream."""

    parent_stream_type = WorkspacesStream
    name = "tags"
    path = "/workspaces/{workspace_id}/tags"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("at", th.DateTimeType),
        th.Property("deleted_at", th.DateTimeType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("workspace_id", th.IntegerType),
    ).to_dict()


class TimeEntriesStream(TogglStream):
    """Define custom stream."""

    name = "time_entries"
    path = "/me/time_entries"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "at"
    schema = th.PropertiesList(
        th.Property("at", th.DateTimeType),
        th.Property("billable", th.BooleanType),
        th.Property("client_name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("duration", th.IntegerType),
        th.Property("duronly", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("pid", th.IntegerType),
        th.Property("project_active", th.BooleanType),
        th.Property("project_color", th.StringType),
        th.Property("project_id", th.IntegerType),
        th.Property("project_name", th.StringType),
        th.Property("server_deleted_at", th.DateTimeType),
        th.Property("start", th.DateTimeType),
        th.Property("stop", th.DateTimeType),
        th.Property("tag_ids", th.ArrayType(th.IntegerType)),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property("task_id", th.IntegerType),
        th.Property("task_name", th.StringType),
        th.Property("tid", th.IntegerType),
        th.Property("uid", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("wid", th.IntegerType),
        th.Property("workspace_id", th.IntegerType),
    ).to_dict()

    def get_url_params(
            self,
            context: dict | None,  # noqa: ARG002
            next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        if self.config.get("start_date"):
            return {"since": self.start_time_to_epoch(self.config.get("start_date"))}
        else:
            return {}
