"""Synthetic GitHub tracker snapshots for two-comment fixtures."""

from __future__ import annotations

import copy
from typing import Any


REPOSITORY_ID = "R_SYNTHETIC_REPOSITORY_001"
REPORT_ID = "I_SYNTHETIC_REPORT_001"
WRITER_ID = "U_SYNTHETIC_WRITER_001"
OTHER_WRITER_ID = "U_SYNTHETIC_OTHER_001"
DEFAULT_BODY = "# Repository gardening history\n\nRead the latest run-closed comment for the morning report.\n"


def empty_tracker(
    *,
    repository_id: str = REPOSITORY_ID,
    report_issue_id: str = REPORT_ID,
    writer_id: str = WRITER_ID,
    body: str = DEFAULT_BODY,
) -> dict[str, Any]:
    return {
        "schema": "repo-gardener-github-tracker-snapshot",
        "configured_repository_id": repository_id,
        "configured_report_issue_id": report_issue_id,
        "configured_writer_id": writer_id,
        "issue": {
            "id": 4242,
            "node_id": report_issue_id,
            "body": body,
            "state": "open",
            "comments": 0,
        },
        "comment_pages_complete": True,
        "comment_pages": [[]],
    }


def _next_comment_id(comments: list[dict[str, Any]]) -> int:
    return max((item["id"] for item in comments), default=0) + 1


def apply_prepared(snapshot: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(snapshot)
    comments = [item for page in result["comment_pages"] for item in page]
    numeric_id = _next_comment_id(comments)
    result["comment_pages"][-1].append(
        {
            "id": numeric_id,
            "node_id": f"IC_RUN_RECORD_{numeric_id:03d}",
            "user": {"node_id": prepared["writer_id"], "login": "synthetic-writer"},
            "body": prepared["comment"],
        }
    )
    result["issue"]["comments"] = len(comments) + 1
    return result


def add_ordinary_comment(
    snapshot: dict[str, Any],
    *,
    author_id: str = OTHER_WRITER_ID,
    body: str = "A marker-free owner note.",
) -> dict[str, Any]:
    result = copy.deepcopy(snapshot)
    comments = [item for page in result["comment_pages"] for item in page]
    numeric_id = _next_comment_id(comments)
    result["comment_pages"][-1].append(
        {
            "id": numeric_id,
            "node_id": f"IC_ORDINARY_{numeric_id:03d}",
            "user": {"node_id": author_id, "login": "synthetic-owner"},
            "body": body,
        }
    )
    result["issue"]["comments"] = len(comments) + 1
    return result


def split_comment_pages(snapshot: dict[str, Any], page_sizes: list[int]) -> dict[str, Any]:
    result = copy.deepcopy(snapshot)
    comments = [item for page in result["comment_pages"] for item in page]
    pages: list[list[dict[str, Any]]] = []
    index = 0
    for size in page_sizes:
        pages.append(comments[index : index + size])
        index += size
    if index != len(comments):
        raise ValueError("page sizes do not cover every comment")
    result["comment_pages"] = pages or [[]]
    result["issue"]["comments"] = len(comments)
    return result
