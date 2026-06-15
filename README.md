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

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?logo=openjdk&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?logo=go&logoColor=white)
![Ruby](https://img.shields.io/badge/Ruby-CC342D?logo=ruby&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-777BB4?logo=php&logoColor=white)
![C#](https://img.shields.io/badge/C%23-512BD4?logo=dotnet&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?logo=kotlin&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?logo=rust&logoColor=white)
![Scala](https://img.shields.io/badge/Scala-DC322F?logo=scala&logoColor=white)
![Swift](https://img.shields.io/badge/Swift-F05138?logo=swift&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?logo=c&logoColor=black)
![C++](https://img.shields.io/badge/C++-00599C?logo=cplusplus&logoColor=white)
![Dart](https://img.shields.io/badge/Dart-0175C2?logo=dart&logoColor=white)

> 🔌 **Embedded & firmware, first-class.** STM32 and other C/C++ targets are detected
> and scanned **automatically** — no setup — with a dedicated **STM32 / ARM Cortex-M
> HAL** ruleset for the peripheral-misuse and memory-safety bugs that bite firmware.

> 🎯 **Not just code — your running stack too.** Point Kobo at a live web app, an API,
> a container image, or a database **you own** and it scans those as well. See
> [Scan live targets you own](#-scan-live-targets-you-own).

---

## 🤖 Built for your AI coding agent

Kobo is made to be **run by your AI agent** — Claude Code, Cursor, Copilot,
Windsurf — so vulnerabilities are caught and fixed *while* the code is written,
not in a security review three weeks later. **Set it up once, then it runs itself.**

**1. Set it up once** (so the agent never touches your credentials):

```bash
pip install kobo-scan && kobo register --email you@gmail.com && kobo verify <code>
```

**2. Paste this rule into your AI tool — then forget about it** (or run `kobo agent` to print it):

> **Security gate — always enforce.** Before you mark any coding task complete, run
> `kobo scan --path . --format json` and parse `findings`. For each finding, open
> `file` at `line`, understand the `message`, and fix the **root cause** —
> parameterize the query, validate or encode the input, drop the unsafe call — never
> suppress, comment out, or ignore it. Then **re-scan** and repeat until **zero
> `critical` and zero `high`** findings remain (target grade **A**). Do not introduce
> new `critical`/`high` issues, and never tell me a task is done while one is open.
> For any other capability (CI gating, or scanning a live URL / API / container /
> database), run `kobo --help` or read the README at https://github.com/kobo-cli/kobo
> before telling me it can't be done. Every so often, run `pip install -U kobo-scan`
> first so you're on the latest scanner.

| Your AI tool | Paste the rule into |
|---|---|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Any other agent / API | the system prompt |

From now on, every time the agent touches code it scans, reads the machine-readable
findings, fixes the real cause, and re-scans — on its own. **Security that keeps pace
with AI-speed development. Zero glue code.**

---

## ⚖️ Why a scanner — not "just ask the AI to review"

Letting your agent security-review every change **costs tokens** and is
**non-deterministic** — it reasons differently each run and silently skips whole
classes of bugs. Kobo is the opposite: deterministic, repeatable **SAST** (static
analysis), **dependency & secret** scanning, and **IaC** config checks. Same code
in → same findings out, in seconds, for free.

**Honest scope.** Kobo catches concrete, detectable vulnerabilities — injection,
leaked secrets, unsafe deserialization, weak crypto, insecure infrastructure config.
It does **not** reason about *business logic*: broken access rules, pricing or quota
abuse, "should this user be allowed to do this?" No scanner catches those reliably —
that's where your own review and your agent's judgment still earn their keep. Run
Kobo for the deterministic security floor; keep a human in the loop for intent.

---

## 📦 Install

Requires **Python 3.10+**.

```bash
pip install kobo-scan        # installs the `kobo` command
pip install -U kobo-scan     # upgrade to the latest (run this now and then)
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

## 🎯 Scan live targets you own

Beyond source code, Kobo can scan things you've **deployed** — but only after you
**prove you control them**, so it can never be aimed at someone else's systems:

```bash
kobo verify-target myapp.com          # we show you a DNS record / file to add
kobo verify-target myapp.com --check  # we confirm it — once per host
```

Then scan the live target:

```bash
kobo scan --url https://myapp.com                              # a running web app
kobo scan --openapi https://myapp.com/openapi.json --api-url https://myapp.com   # an API
kobo scan --image ghcr.io/you/app:latest                       # a container image
kobo scan --db postgresql://user:pass@db.myapp.com:5432/app    # a database
```

Findings land in the **same report** as code scans (same grade, same fields). You
can only scan hosts you've verified — internal and unverified addresses are refused.
*(Container-image scanning inspects the image, so it needs no ownership check.)*

---

## 🧰 Commands

| Command | What it does |
|---|---|
| `kobo register --email <e>` | sign up — get a verification code by email |
| `kobo verify <code>` | activate your account + store your key |
| `kobo login --key <key>` | log in on a new machine with an existing key |
| `kobo scan --path <dir>` | scan a project — `--format text\|json` |
| `kobo scan --url\|--image\|--db\|--api-url` | scan a live target you own (see above) |
| `kobo verify-target <host>` | prove you own a host so you can scan it live (`--check` to confirm) |
| `kobo report --last` | re-fetch your latest report (`--format json`) |
| `kobo history` | list your past scans |
| `kobo whoami` / `kobo logout` | show account / forget credentials |
| `kobo agent` | print the rule to paste into an AI tool (`CLAUDE.md`, `.cursorrules`…) |
| `kobo config --server <url>` | point at a different API endpoint |
| `kobo version` | print the version |

> 💡 **The CLI is self-documenting.** Run `kobo` (or `kobo --help`, `kobo scan --help`)
> for the full guide — quickstart, live-target usage, and the AI-agent workflow + JSON
> shape are built right in, so an agent can learn the whole tool with no README.

---

## 📊 The report

Every finding is **`file · line · severity · message`**, plus one **A–F grade**
so you know at a glance whether it's safe to ship.

`--format json` gives clean, machine-readable output for your AI agent or CI:

```json
{
  "grade": "B",
  "summary": { "total": 7, "critical": 0, "high": 2, "medium": 3, "low": 2 },
  "findings": [
    { "file": "app.py", "line": 42, "severity": "high",
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

Free for individual developers and small teams. Light rate limits keep it fair:

| Scan type | Limit |
|---|---|
| 📦 **Code scans** (`--path`) | 5 per 5-hour window |
| 🎯 **Live-target scans** (`--url` / `--api-url` / `--db` / `--image`) | 10 per hour |

**No payment, no credit card, no quotas to manage.**

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
