#!/usr/bin/env python3
"""Reject new commits whose GitHub author/committer metadata is not attributable.

The repository's canonical GitHub no-reply address is intentionally written out
rather than derived from shell configuration, so the check behaves identically
locally and in CI. GitHub-generated merge commits are allowed to use GitHub's
own committer address, while the authored change must still be attributable to
this repository owner.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass

CANONICAL_EMAIL = "126043595+Samarssj@users.noreply.github.com"
LEGACY_VERIFIED_EMAILS = {"ssjsamar453@gmail.com"}
GITHUB_COMMITTER_EMAIL = "noreply@github.com"
CANONICAL_RE = re.compile(re.escape(CANONICAL_EMAIL) + r"$", re.IGNORECASE)


@dataclass(frozen=True)
class CommitIdentity:
    sha: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    subject: str


def commits(revision_range: str | None) -> list[CommitIdentity]:
    revisions = revision_range or "HEAD"
    output = subprocess.check_output(
        [
            "git",
            "log",
            "--format=%H%x09%an%x09%ae%x09%cn%x09%ce%x09%s",
            revisions,
        ],
        text=True,
    )
    result: list[CommitIdentity] = []
    for line in output.splitlines():
        sha, author_name, author_email, committer_name, committer_email, subject = line.split("\t", 5)
        result.append(CommitIdentity(sha, author_name, author_email, committer_name, committer_email, subject))
    return result


def author_is_allowed(email: str, strict: bool) -> bool:
    if CANONICAL_RE.fullmatch(email):
        return True
    return not strict and email.lower() in {value.lower() for value in LEGACY_VERIFIED_EMAILS}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--range", dest="revision_range", help="Git revision range to validate")
    parser.add_argument(
        "--historical",
        action="store_true",
        help="Allow the explicitly documented legacy verified email in existing history",
    )
    args = parser.parse_args()

    try:
        identities = commits(args.revision_range)
    except (subprocess.CalledProcessError, ValueError) as exc:
        print(f"Unable to inspect commit identities: {exc}", file=sys.stderr)
        return 2

    violations: list[str] = []
    for commit in identities:
        author_ok = author_is_allowed(commit.author_email, strict=not args.historical)
        committer_ok = CANONICAL_RE.fullmatch(commit.committer_email) or (
            commit.committer_email.lower() == GITHUB_COMMITTER_EMAIL
        )
        if not author_ok or not committer_ok:
            violations.append(
                f"{commit.sha[:12]} {commit.subject!r}: "
                f"author={commit.author_email!r}, committer={commit.committer_email!r}"
            )

    if violations:
        print("Commit identity policy violation(s):", file=sys.stderr)
        print("\n".join(violations), file=sys.stderr)
        print(
            f"Use {CANONICAL_EMAIL} for local commits; GitHub-generated commits may use "
            f"{GITHUB_COMMITTER_EMAIL} as the committer.",
            file=sys.stderr,
        )
        return 1

    print(f"Validated {len(identities)} commit identity record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
