# 🛡️ Kobo

**AI writes code fast — and ships vulnerabilities just as fast.** Every generated
function can hide SQL injection, a leaked API key, or unsafe deserialization that
*looks* perfectly fine. **Kobo is the security gate for AI-assisted development:**
one command scans your code and hands back findings your AI agent can fix — before
they reach production.

Free. One command. Built to be run by your AI coding agent.

```bash
pip install kobo-scan
kobo scan --path .
```

> This repository is the **open-source command-line client**. It packages your
> project, sends it to the Kobo API over HTTPS, and prints the result — so you can
> read exactly what it does.

---

## 🔍 What it catches

The bugs that actually get apps hacked — the ones that pass code review and slip
straight out of an AI prompt:

| | |
|---|---|
| 💉 **Injection** | SQL, NoSQL, OS-command, code/`eval`, LDAP, XPath |
| 🌐 **Web attacks** | XSS, SSRF, open redirects, request/header smuggling |
| 📂 **Files & data** | path traversal, unsafe deserialization, XXE, template injection |
| 🔑 **Leaked secrets** | hardcoded API keys, tokens, passwords |
| 📦 **Risky dependencies** | imported packages with known security holes |
| ⚙️ **Misconfiguration** | insecure infra config, weak crypto |

…across the **15 languages you actually ship in**:

> **Python · JavaScript · TypeScript · Java · Go · Ruby · PHP · C# ·
> Kotlin · Rust · Scala · Swift · C · C++ · Dart**

---

## 📦 Install

Requires **Python 3.10+**.

```bash
pip install kobo-scan        # installs the `kobo` command
```

<details><summary>Other ways to install</summary>

```bash
pip install git+https://github.com/kobo-cli/kobo.git   # from source
python kobo.py --help                                  # run the single file, no install
```
</details>

---

## 🚀 Quick start

```bash
kobo register --email you@gmail.com   # we email you a 6-digit code
kobo verify 123456                    # activates your account
kobo scan --path .                    # accept the terms once, then scan
```

```text
Security Grade: B
Findings: 7  (critical 0 · high 2 · medium 3 · low 2)
Full report: kobo report --last --format json
```

Your API key is saved in `~/.kobo/` (readable only by you). On another machine,
skip re-verifying — just `kobo login --key <your-key>`.

---

## 🤖 Let your AI agent run it (no manual step)

Kobo is designed to be **driven by AI coding agents** — Claude, GPT, Cursor,
Copilot — so scanning and fixing happen *while* code is written.

**1. You set it up once** (so the agent never touches your credentials):

```bash
pip install kobo-scan && kobo register --email you@gmail.com && kobo verify <code>
```

**2. Drop this instruction into your AI tool:**

> After writing or changing code, run `kobo scan --path . --format json`. Read the
> JSON `findings`; for each, open `file` at `line` and fix the issue described by
> `cwe` + `message`. Re-run until there are **no `critical` or `high`** findings.
> Never finish a task with an open critical/high vulnerability.

| Tool | Where it goes |
|---|---|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Custom agent / API | the system prompt |

Now the agent scans, reads machine-readable findings, fixes them, and re-scans on
its own — every time it touches code. Zero glue code.

---

## 🧰 Commands

| Command | What it does |
|---|---|
| `kobo register --email <e>` | sign up — get a verification code by email |
| `kobo verify <code>` | activate your account + store your key |
| `kobo login --key <key>` | log in on a new machine with an existing key |
| `kobo scan --path <dir>` | scan a project — `--format text\|json` |
| `kobo report --last` | re-fetch your latest report (`--format json`) |
| `kobo history` | list your past scans |
| `kobo whoami` / `kobo logout` | show account / forget credentials |
| `kobo config --server <url>` | point at a different API endpoint |
| `kobo version` | print the version |

---

## 📊 The report

Every finding is **`file · line · severity · CWE · message`**, plus one **A–F grade**
so you know at a glance whether it's safe to ship.

`--format json` gives clean, machine-readable output for your AI agent or CI:

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

**Fail a CI build on a bad grade** (example with `jq`):

```bash
GRADE=$(kobo scan --path . --format json | jq -r .grade)
[ "$GRADE" = "F" ] && { echo "Security grade F — failing build"; exit 1; } || true
```

---

## 🆓 Free tier

Unlimited use for individual developers and small teams, with a light rate limit
(a few scans per 5-hour window). **No payment, no credit card, no quotas to manage.**

---

## 🔒 Privacy

Running a scan **uploads your source code** to the Kobo service, where it's stored
and used to operate and improve the product. **Remove secrets and credentials
before scanning.** You accept the [terms](TERMS.md) once before your first scan.
Full details: [TERMS.md](TERMS.md).

---

## 📄 License

The Kobo CLI is licensed under the **GNU AGPL-3.0-or-later** ([LICENSE](LICENSE)) —
use, modify, and redistribute freely; derivatives (including a modified version run
as a service) must stay open under the same license. The Kobo backend service is
separate and governed by [TERMS.md](TERMS.md).
