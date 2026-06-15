#!/usr/bin/env python3
# Kobo CLI — Copyright (C) 2026 Kobo
# SPDX-License-Identifier: AGPL-3.0-or-later
# Free software under the GNU Affero General Public License v3 or later; see LICENSE.
"""kobo — free-tier security scanner CLI.

Self-service: registers your account, manages your API key, accepts the terms once
(server-side gate), uploads your code, and prints a lean AI-friendly report. No
wallet/quota/billing — this is the free trial.

  kobo config --server https://kobo-api-712614001328.europe-west1.run.app
  kobo register --email you@gmail.com
  kobo verify 123456
  kobo scan --path .
  kobo report --last --format json
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import zipfile

import httpx

__version__ = "0.1.0"

_HOME = os.environ.get("KOBO_HOME") or os.path.join(os.path.expanduser("~"), ".kobo")
_CONFIG = os.path.join(_HOME, "config.json")
_CREDS = os.path.join(_HOME, "credentials.json")
# Production API. Override locally with: kobo config --server <url>
_DEFAULT_SERVER = os.environ.get("KOBO_SERVER", "https://kobo-api-712614001328.europe-west1.run.app")

# directories never worth uploading
_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
              "build", ".idea", ".pytest_cache", "target", ".mypy_cache"}
_MAX = 50 * 1024 * 1024


# ── local state ───────────────────────────────────────────────────────────────
def _read(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write(path: str, data: dict, *, secret: bool = False) -> None:
    os.makedirs(_HOME, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    if secret:
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass


def _server() -> str:
    return _read(_CONFIG).get("server", _DEFAULT_SERVER)


def make_client() -> httpx.Client:
    """Factory (monkeypatchable in tests) — a client bound to the configured server."""
    return httpx.Client(base_url=_server(), timeout=300)


def _auth_headers() -> dict:
    key = _read(_CREDS).get("api_key")
    if not key:
        _die("not logged in — run `kobo register` then `kobo verify <code>`")
    return {"Authorization": f"Bearer {key}"}


def _die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def _detail(resp: httpx.Response) -> str:
    try:
        return resp.json().get("detail", resp.text)
    except Exception:
        return resp.text


# ── packaging ─────────────────────────────────────────────────────────────────
def pack_path(path: str) -> bytes:
    buf = io.BytesIO()
    total = 0
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
            for fn in files:
                full = os.path.join(root, fn)
                try:
                    total += os.path.getsize(full)
                except OSError:
                    continue
                if total > _MAX:
                    _die("project exceeds the 50 MB free-tier upload limit")
                zf.write(full, os.path.relpath(full, path))
    return buf.getvalue()


# ── commands ──────────────────────────────────────────────────────────────────
def cmd_config(args) -> None:
    cfg = _read(_CONFIG)
    if args.server:
        cfg["server"] = args.server.rstrip("/")
        _write(_CONFIG, cfg)
    print(json.dumps({"server": cfg.get("server", _DEFAULT_SERVER)}, indent=2))


def cmd_register(args) -> None:
    with make_client() as c:
        r = c.post("/register", json={"email": args.email})
    if r.status_code != 200:
        _die(_detail(r))
    _write(_CREDS, {**_read(_CREDS), "email": args.email}, secret=True)
    print(f"verification code sent to {args.email} — run `kobo verify <code>`")


def cmd_verify(args) -> None:
    email = _read(_CREDS).get("email")
    if not email:
        _die("run `kobo register --email ...` first")
    with make_client() as c:
        r = c.post("/verify", json={"email": email, "code": args.code})
    if r.status_code != 200:
        _die(_detail(r))
    _write(_CREDS, {"email": email, "api_key": r.json()["api_key"]}, secret=True)
    print("verified — you're ready to scan with `kobo scan --path .`")


def cmd_login(args) -> None:
    """Authenticate on a new machine with an existing API key."""
    with make_client() as c:
        r = c.get("/whoami", headers={"Authorization": f"Bearer {args.key}"})
    if r.status_code != 200:
        _die("invalid api key")
    email = r.json().get("email", "")
    _write(_CREDS, {"email": email, "api_key": args.key}, secret=True)
    print(f"logged in as {email}")


def cmd_whoami(args) -> None:
    with make_client() as c:
        r = c.get("/whoami", headers=_auth_headers())
    if r.status_code != 200:
        _die(_detail(r))
    print(json.dumps(r.json(), indent=2))


def cmd_logout(args) -> None:
    for p in (_CREDS,):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass
    print("logged out")


def _ensure_terms(c: httpx.Client, headers: dict) -> None:
    who = c.get("/whoami", headers=headers)
    if who.status_code == 200 and who.json().get("terms_accepted"):
        return
    health = c.get("/health").json()
    version, url = health.get("terms_version"), _read(_CONFIG).get("terms_url", health.get("terms_url", ""))
    print(f"\nFirst scan — you must accept the Kobo Terms (v{version}):\n  {url or 'see TERMS.md'}")
    ans = input("Accept? [y/N] ").strip().lower()
    if ans != "y":
        _die("terms not accepted — scan cancelled")
    r = c.post("/terms/accept", json={"version": version}, headers=headers)
    if r.status_code != 200:
        _die(_detail(r))


def cmd_scan(args) -> None:
    headers = _auth_headers()
    payload = pack_path(args.path)
    with make_client() as c:
        _ensure_terms(c, headers)
        r = c.post("/scan", headers=headers, files={"file": ("src.zip", payload, "application/zip")})
    if r.status_code != 200:
        _die(_detail(r), code=2)
    body = r.json()
    if args.format == "json":
        with make_client() as c:
            rep = c.get(f"/scan/{body['scan_id']}", headers=headers).json()
        print(json.dumps(rep["report"], indent=2))
    else:
        s = body["summary"]
        print(f"\nSecurity Grade: {body['grade']}")
        print(f"Findings: {s['total']}  (critical {s['critical']} · high {s['high']} "
              f"· medium {s['medium']} · low {s['low']})")
        print(f"Full report: kobo report --last --format json   (scan #{body['scan_id']})")


def cmd_report(args) -> None:
    headers = _auth_headers()
    with make_client() as c:
        if args.last:
            hist = c.get("/scans", headers=headers).json()
            if not hist:
                _die("no scans yet")
            scan_id = hist[0]["scan_id"]
        else:
            scan_id = args.id
        rep = c.get(f"/scan/{scan_id}", headers=headers)
    if rep.status_code != 200:
        _die(_detail(rep))
    print(json.dumps(rep.json()["report"], indent=2))


def cmd_history(args) -> None:
    with make_client() as c:
        r = c.get("/scans", headers=_auth_headers())
    print(json.dumps(r.json(), indent=2))


def cmd_version(args) -> None:
    print(f"kobo {__version__}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kobo", description="Kobo free-tier security scanner")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("config", help="set the server URL"); s.add_argument("--server"); s.set_defaults(fn=cmd_config)
    s = sub.add_parser("register", help="register an email"); s.add_argument("--email", required=True); s.set_defaults(fn=cmd_register)
    s = sub.add_parser("verify", help="verify the OTP code"); s.add_argument("code"); s.set_defaults(fn=cmd_verify)
    s = sub.add_parser("login", help="log in with an existing API key")
    s.add_argument("--key", required=True); s.set_defaults(fn=cmd_login)
    s = sub.add_parser("whoami", help="show account"); s.set_defaults(fn=cmd_whoami)
    s = sub.add_parser("logout", help="forget credentials"); s.set_defaults(fn=cmd_logout)
    s = sub.add_parser("scan", help="scan a project")
    s.add_argument("--path", default="."); s.add_argument("--format", choices=["text", "json"], default="text")
    s.set_defaults(fn=cmd_scan)
    s = sub.add_parser("report", help="fetch a report")
    s.add_argument("--last", action="store_true"); s.add_argument("--id", type=int); s.add_argument("--format", default="json")
    s.set_defaults(fn=cmd_report)
    s = sub.add_parser("history", help="list scans"); s.set_defaults(fn=cmd_history)
    s = sub.add_parser("version", help="print version"); s.set_defaults(fn=cmd_version)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.fn(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
