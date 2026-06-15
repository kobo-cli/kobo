# Kovo CLI

**Free security scanning for your code, from the command line.**

Kovo scans your project for real vulnerabilities — SQL injection, XSS, command
injection, SSRF, path traversal, insecure deserialization, and more — and gives
you a clear report you (or your AI coding agent) can act on immediately.

This repo is the **command-line client only**. It zips your project, sends it to
the Kovo API over HTTPS, and prints the result. It's open source so you can verify
exactly what it does.

---

## Install

```bash
pip install kovo-cli      # installs the `kovo` command
```

Requires Python 3.10+.

## Getting started (3 steps)

```bash
# 1. Sign up — Kovo emails you a 6-digit code
kovo register --email you@gmail.com

# 2. Enter the code to activate your account
kovo verify 123456

# 3. Scan your project (you'll accept the terms once, the first time)
kovo scan --path .
```

That's it. Example output:

```
Security Grade: B
Findings: 7  (critical 0 · high 2 · medium 3 · low 2)
Full report: kovo report --last --format json
```

## Use with an AI agent

Get the full machine-readable report and feed it to your assistant to auto-fix:

```bash
kovo scan --path . --format json      # findings as JSON
kovo report --last --format json      # re-fetch the latest report
```

Each finding includes the file, line, severity, CWE, and a short message.

## All commands

| Command | Description |
| --- | --- |
| `kovo register --email <email>` | Request a verification code |
| `kovo verify <code>` | Verify and store your API key |
| `kovo scan --path <dir>` | Scan a project (`--format text\|json`) |
| `kovo report --last` | Fetch your most recent report |
| `kovo history` | List your past scans |
| `kovo whoami` | Show your account |
| `kovo logout` | Remove stored credentials |
| `kovo config --server <url>` | Point at a different API endpoint |

Your API key is stored locally in `~/.kovo/` (readable only by you).

## Free tier

Unlimited use for individual developers and small teams, with a light rate limit
(a few scans per 5-hour window). No payment, no card, no quotas to manage.

## Privacy

Running a scan **uploads your source code** to the Kovo service, where it is stored
and used to operate and improve the product. **Remove secrets and credentials
before scanning.** Full details: [TERMS.md](TERMS.md). The CLI asks you to accept
these terms once before your first scan.

## License

The Kovo CLI is licensed under the **GNU AGPL-3.0-or-later** ([LICENSE](LICENSE)).
You may use, modify, and redistribute it freely; any derivative — including a
modified version run as a network service — must stay open under the same license.
The Kovo backend service is separate and governed by [TERMS.md](TERMS.md).
