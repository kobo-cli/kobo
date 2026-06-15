# Kobo CLI

**Free security scanning for your code, from the command line.**

Kobo scans your project for real vulnerabilities — SQL injection, XSS, command
injection, SSRF, path traversal, insecure deserialization, and more — and gives
you a clear report you (or your AI coding agent) can act on immediately.

This repo is the **command-line client only**. It zips your project, sends it to
the Kobo API over HTTPS, and prints the result. It's open source so you can verify
exactly what it does.

---

## Install

```bash
pip install kobo-cli      # installs the `kobo` command
```

Requires Python 3.10+.

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

## All commands

| Command | Description |
| --- | --- |
| `kobo register --email <email>` | Request a verification code |
| `kobo verify <code>` | Verify and store your API key |
| `kobo scan --path <dir>` | Scan a project (`--format text\|json`) |
| `kobo report --last` | Fetch your most recent report |
| `kobo history` | List your past scans |
| `kobo whoami` | Show your account |
| `kobo logout` | Remove stored credentials |
| `kobo config --server <url>` | Point at a different API endpoint |

Your API key is stored locally in `~/.kobo/` (readable only by you).

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
