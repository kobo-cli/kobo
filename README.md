# Kobo CLI

**AI writes code fast — and ships bugs and vulnerabilities just as fast.** Every
generated function can hide SQL injection, leaked secrets, command injection, or
unsafe deserialization that *looks* perfectly fine. **Kobo is the security gate for
AI-assisted development:** one command scans your code and hands your AI agent
machine-readable findings to fix — before they ever reach production.

*Free security scanning for your code, from the command line.*

Kobo scans your project for real vulnerabilities — SQL injection, XSS, command
injection, SSRF, path traversal, insecure deserialization, and more — and gives
you a clear report you (or your AI coding agent) can act on immediately.

This repo is the **command-line client only**. It zips your project, sends it to
the Kobo API over HTTPS, and prints the result. It's open source so you can verify
exactly what it does.

---

## Install

Requires **Python 3.10+**.

```bash
pip install kobo-scan      # installs the `kobo` command
```

That's it — `pip install kobo-scan` (the package), then use `kobo`.

<details>
<summary>Other ways to install</summary>

```bash
# from GitHub
pip install git+https://github.com/kobo-cli/kobo.git

# or clone / download ZIP, then:
pip install .

# or run the single file directly, no install:
python kobo.py --help
```
</details>

## Let your AI assistant use Kobo automatically

Kobo is built to be **driven by AI coding agents** (Claude, GPT, Cursor, Copilot, …)
so security scanning happens *while* code is written — no manual step.

**1. One-time setup (you do this once):**
```bash
pip install kobo-scan
kobo register --email you@gmail.com
kobo verify <code>        # from your email
```
After this the API key is stored in `~/.kobo/`, so the agent can scan without ever
seeing your credentials.

**2. Give your AI agent this instruction** — paste it into your tool's rules/prompt:

> After you write or modify code, run `kobo scan --path . --format json`.
> Read the JSON `findings`; for each, open `file` at `line` and fix the issue
> described by `cwe` + `message`. Re-run `kobo scan` until there are **no `critical`
> or `high` findings**. Never finish a task with an open critical/high vulnerability.

That's it — now the agent scans, reads machine-readable findings, fixes them, and
re-scans on its own, every time it touches code.

**Where to put the instruction:**

| Tool | File / place |
| --- | --- |
| Claude Code | `CLAUDE.md` in your repo |
| Cursor | `.cursorrules` (or Settings → Rules) |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Custom agent / API | the system prompt |

The report is pure JSON (`file · line · severity · cwe · message`), so any agent can
parse and act on it with **zero glue code** — fully hands-off security as you build.

## Getting started (3 steps)

```bash
# 1. Sign up — Kobo emails you a 6-digit code
kobo register --email you@gmail.com

# 2. Enter the code to activate your account
kobo verify 123456

# 3. Scan your project (you'll accept the terms once, the first time)
kobo scan --path .
```

That's it. Example output:

```
Security Grade: B
Findings: 7  (critical 0 · high 2 · medium 3 · low 2)
Full report: kobo report --last --format json
```

## Use with an AI agent

Get the full machine-readable report and feed it to your assistant to auto-fix:

```bash
kobo scan --path . --format json      # findings as JSON
kobo report --last --format json      # re-fetch the latest report
```

Each finding includes the file, line, severity, CWE, and a short message.

## Examples

**Scan the current project:**
```bash
kobo scan --path .
```
```
Security Grade: B
Findings: 7  (critical 0 · high 2 · medium 3 · low 2)
Full report: kobo report --last --format json
```

**Scan a specific folder:**
```bash
kobo scan --path ./services/api
```

**Get the machine-readable report** (file · line · severity · CWE · message — ready for an AI agent to fix):
```bash
kobo scan --path . --format json
```
```json
{
  "grade": "B",
  "summary": { "total": 7, "critical": 0, "high": 2, "medium": 3, "low": 2 },
  "findings": [
    { "file": "app.py", "line": 42, "severity": "high",
      "cwe": "CWE-89", "title": "SQL Injection",
      "message": "Untrusted input flows into a SQL query" }
  ]
}
```

**Pipe findings into your AI coding agent** to auto-fix:
```bash
kobo scan --path . --format json > findings.json
# then: "Fix every finding in findings.json"
```

**Re-fetch your latest report / list history:**
```bash
kobo report --last --format json
kobo history
```

**Use in CI** (fail the build on a bad grade — example with `jq`):
```bash
GRADE=$(kobo scan --path . --format json | jq -r .grade)
[ "$GRADE" = "F" ] && { echo "Security grade F — failing build"; exit 1; }
```

**Returning on a new machine** (log in with your existing key instead of re-verifying):
```bash
kobo login --key kobo_xxxxxxxxxxxxxxxx
kobo scan --path .
```

## All commands

| Command | Description |
| --- | --- |
| `kobo register --email <email>` | Request a verification code |
| `kobo verify <code>` | Verify and store your API key |
| `kobo login --key <api-key>` | Log in on a new machine with an existing API key |
| `kobo scan --path <dir>` | Scan a project (`--format text\|json`) |
| `kobo report --last` | Fetch your most recent report (`--format json`) |
| `kobo history` | List your past scans |
| `kobo whoami` | Show your account |
| `kobo logout` | Remove stored credentials |
| `kobo config --server <url>` | Point at a different API endpoint |
| `kobo version` | Print the CLI version |

Your API key is stored locally in `~/.kobo/` (readable only by you).

### Already have an account? (new machine)

`register`/`verify` is a one-time signup. On another machine, don't re-verify
(that rotates your key) — just log in with your existing key:

```bash
kobo login --key kobo_xxxxxxxxxxxxxxxx
```

## Free tier

Unlimited use for individual developers and small teams, with a light rate limit
(a few scans per 5-hour window). No payment, no card, no quotas to manage.

## Privacy

Running a scan **uploads your source code** to the Kobo service, where it is stored
and used to operate and improve the product. **Remove secrets and credentials
before scanning.** Full details: [TERMS.md](TERMS.md). The CLI asks you to accept
these terms once before your first scan.

## License

The Kobo CLI is licensed under the **GNU AGPL-3.0-or-later** ([LICENSE](LICENSE)).
You may use, modify, and redistribute it freely; any derivative — including a
modified version run as a network service — must stay open under the same license.
The Kobo backend service is separate and governed by [TERMS.md](TERMS.md).
