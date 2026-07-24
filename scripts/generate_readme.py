#!/usr/bin/env python3
"""Generate the GitHub profile README from public, verifiable data."""

from __future__ import annotations

import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

USERNAME = "floze-the-genius"
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.md"

EXCLUDED_OWNERS = {
    "edgegift",
    "floze-the-genius",
    "kazi4kk",
    "kishvpn-org",
    "maksdavydovpr",
    "tehniki-dev",
    "vladikaccelerator",
}

MAINTAINED_REPOSITORIES = [
    "floze-the-genius/opencode-multi-auth-codex",
    "floze-the-genius/opencode-tps-meter",
    "floze-the-genius/opencode-status-signals",
]

PROJECT_DESCRIPTIONS = {
    "floze-the-genius/opencode-multi-auth-codex": (
        "Account routing, session controls, dashboard, and reliability tooling "
        "for Codex OAuth in OpenCode."
    ),
    "floze-the-genius/opencode-tps-meter": (
        "Live streaming and final output-token throughput for the OpenCode TUI."
    ),
    "floze-the-genius/opencode-status-signals": (
        "Session-state feedback through OpenCode's native theme system."
    ),
}

CARD_CANDIDATES = {
    "PROFILE_CARD_URL": [
        (
            "https://github-profile-summary-cards.vercel.app/api/cards/"
            f"profile-details?username={USERNAME}&theme=github_dark"
        ),
        (
            "https://github-readme-activity-graph.vercel.app/graph"
            f"?username={USERNAME}&theme=github-compact&hide_border=true&area=true"
        ),
    ],
    "STREAK_CARD_URL": [
        (
            "https://streak-stats.demolab.com/"
            f"?user={USERNAME}&theme=github-dark-blue&hide_border=true"
        ),
        (
            "https://github-profile-summary-cards.vercel.app/api/cards/stats"
            f"?username={USERNAME}&theme=github_dark"
        ),
    ],
    "LANGUAGES_CARD_URL": [
        (
            "https://github-profile-summary-cards.vercel.app/api/cards/"
            f"repos-per-language?username={USERNAME}&theme=github_dark"
        ),
        (
            "https://github-readme-stats-one-bice.vercel.app/api/top-langs/"
            f"?username={USERNAME}&layout=compact&theme=github_dark&hide_border=true"
        ),
    ],
    "ACTIVITY_CARD_URL": [
        (
            "https://github-readme-activity-graph.vercel.app/graph"
            f"?username={USERNAME}&theme=github-compact&hide_border=true&area=true"
        ),
        (
            "https://github-profile-summary-cards.vercel.app/api/cards/"
            f"profile-details?username={USERNAME}&theme=github_dark"
        ),
    ],
}

MAX_SEARCH_PAGES = 10
RECENT_MERGE_LIMIT = 6


def github_token() -> str | None:
    for name in ("GITHUB_TOKEN", "GH_TOKEN", "GH_PAT"):
        if os.environ.get(name):
            return os.environ[name]
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"],
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


TOKEN = github_token()


def request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(
            req,
            context=ssl.create_default_context(),
            timeout=45,
        ) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API returned {exc.code} for {url}: {detail[:400]}"
        ) from exc


def graphql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    response = request_json(
        "https://api.github.com/graphql",
        method="POST",
        payload={"query": query, "variables": variables or {}},
    )
    if response.get("errors"):
        raise RuntimeError(f"GraphQL errors: {response['errors']}")
    return response["data"]


def fetch_public_year_contributions() -> int:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=365)
    data = graphql(
        """
        query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
              contributionCalendar { totalContributions }
              restrictedContributionsCount
            }
          }
        }
        """,
        {
            "login": USERNAME,
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": end.isoformat().replace("+00:00", "Z"),
        },
    )
    collection = data["user"]["contributionsCollection"]
    total = int(collection["contributionCalendar"]["totalContributions"])
    restricted = int(collection["restrictedContributionsCount"])
    return max(0, total - restricted)


def fetch_merged_pull_requests() -> list[dict[str, Any]]:
    """Fetch public authored merges via GitHub Search.

    The user.pullRequests GraphQL connection omits some older authored PRs whose
    fork metadata changed after merge. Search is the same source used by the
    live OSS audit and still returns those verifiable public merges.
    """
    merged: list[dict[str, Any]] = []
    query = f"is:pr author:{USERNAME} is:merged is:public"
    for page in range(1, MAX_SEARCH_PAGES + 1):
        params = urllib.parse.urlencode(
            {
                "q": query,
                "sort": "updated",
                "order": "desc",
                "per_page": 100,
                "page": page,
            }
        )
        data = request_json(f"https://api.github.com/search/issues?{params}")
        items = data.get("items") or []
        for item in items:
            repository_url = item.get("repository_url") or ""
            marker = "/repos/"
            if marker not in repository_url:
                continue
            full_name = repository_url.split(marker, 1)[1]
            owner = full_name.split("/", 1)[0]
            pull_request = item.get("pull_request") or {}
            merged_at = pull_request.get("merged_at") or item.get("closed_at")
            merged.append(
                {
                    "title": item.get("title") or "",
                    "number": item["number"],
                    "url": item["html_url"],
                    "mergedAt": merged_at,
                    "repository": {
                        "nameWithOwner": full_name,
                        "isPrivate": False,
                        "owner": {"login": owner},
                    },
                }
            )
        if len(items) < 100:
            break
    return merged


def is_external_public(pr: dict[str, Any]) -> bool:
    repository = pr.get("repository") or {}
    owner = ((repository.get("owner") or {}).get("login") or "").lower()
    return bool(
        pr.get("mergedAt")
        and not repository.get("isPrivate")
        and owner
        and owner not in EXCLUDED_OWNERS
    )


def fetch_repository(full_name: str) -> dict[str, Any]:
    return request_json(f"https://api.github.com/repos/{full_name}")


def format_maintained_projects(
    repositories: list[dict[str, Any]],
) -> tuple[str, int]:
    cells: list[str] = []
    stars = 0
    for repository in repositories:
        full_name = repository["full_name"]
        name = repository["name"]
        stars += int(repository["stargazers_count"])
        description = PROJECT_DESCRIPTIONS[full_name]
        cells.append(
            f"""    <td width="33%" valign="top">
      <h3><a href="{repository["html_url"]}">{name}</a></h3>
      <p>{description}</p>
      <p>
        <img src="https://img.shields.io/github/stars/{full_name}?style=flat-square&label=stars" alt="Stars" />
        <img src="https://img.shields.io/github/forks/{full_name}?style=flat-square&label=forks" alt="Forks" />
      </p>
    </td>"""
        )
    return "<table>\n  <tr>\n" + "\n".join(cells) + "\n  </tr>\n</table>", stars


def clean_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip()).replace("|", "\\|")


def format_recent_merges(merged: list[dict[str, Any]]) -> str:
    external = sorted(
        (pr for pr in merged if is_external_public(pr)),
        key=lambda pr: pr["mergedAt"],
        reverse=True,
    )
    chosen: list[dict[str, Any]] = []
    repositories: set[str] = set()
    for pr in external:
        full_name = pr["repository"]["nameWithOwner"]
        if full_name.lower() in repositories:
            continue
        repositories.add(full_name.lower())
        chosen.append(pr)
        if len(chosen) == RECENT_MERGE_LIMIT:
            break

    if not chosen:
        return "_No public upstream merges found._"

    lines = []
    for pr in chosen:
        full_name = pr["repository"]["nameWithOwner"]
        merged_date = pr["mergedAt"][:10]
        lines.append(
            f"- **[{full_name}#{pr['number']}]({pr['url']})** - "
            f"{clean_title(pr['title'])} ({merged_date})"
        )
    return "\n".join(lines)


def looks_like_svg(body: bytes, content_type: str) -> bool:
    head = body.lstrip()[:250].lower()
    return (
        len(body) >= 300
        and (b"<svg" in head or "image/svg" in content_type.lower())
        and b"<html" not in head
        and b"deployment_paused" not in head
    )


def choose_card_url(candidates: list[str]) -> str:
    for url in candidates:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "image/svg+xml,image/*,*/*",
                "User-Agent": f"{USERNAME}-profile-card-probe",
            },
        )
        try:
            with urllib.request.urlopen(
                req,
                context=ssl.create_default_context(),
                timeout=10,
            ) as response:
                body = response.read(64_000)
                content_type = response.headers.get("Content-Type", "")
                if response.status == 200 and looks_like_svg(body, content_type):
                    return url
        except Exception:
            continue
    return candidates[0]


def render() -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    template = re.sub(
        r"^<!--.*?-->\n",
        "<!-- AUTO-GENERATED from README.template.md; edit the template, not this file. -->\n",
        template,
        count=1,
        flags=re.DOTALL,
    )

    merged = fetch_merged_pull_requests()
    external_merged = [pr for pr in merged if is_external_public(pr)]
    contributions = fetch_public_year_contributions()
    repositories = [fetch_repository(name) for name in MAINTAINED_REPOSITORIES]
    projects, maintained_stars = format_maintained_projects(repositories)

    replacements = {
        "UPSTREAM_MERGED": str(len(external_merged)),
        "PUBLIC_YEAR_CONTRIBUTIONS": str(contributions),
        "MAINTAINED_STARS": str(maintained_stars),
        "MAINTAINED_PROJECTS": projects,
        "RECENT_MERGES": format_recent_merges(merged),
    }
    for key, candidates in CARD_CANDIDATES.items():
        replacements[key] = choose_card_url(candidates)

    content = template
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", value)

    leftovers = re.findall(r"\{\{[A-Z0-9_]+\}\}", content)
    if leftovers:
        raise RuntimeError(f"Unreplaced placeholders: {leftovers}")
    return content


def main() -> int:
    try:
        OUTPUT.write_text(render(), encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Generated {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
