# Contributing to NewsPilot

## Commit identity

GitHub uses the commit author and committer metadata when it renders the commit timeline. Configure local commits with the repository owner's canonical GitHub no-reply address so each commit resolves to one account and one avatar:

```bash
git config user.name "Samarssj"
git config user.email "126043595+Samarssj@users.noreply.github.com"
```

Do not copy an email address displayed in scientific notation. It is malformed metadata and will not resolve consistently on GitHub.

GitHub-generated commits may use `noreply@github.com` as their committer address; the authored change must still use the canonical address above.

## Before opening a pull request

Run the same checks used by CI:

```bash
python -m compileall -q .
python scripts/smoke_test.py
python scripts/check_commit_identities.py --range HEAD
```

Pull requests and pushes to `main` run the repository validation workflow. Changes that fail the identity, syntax, runtime, or icon-wall checks should be corrected before deployment.
