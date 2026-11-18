#!/usr/bin/env python3
"""Sync Antigravity (agy) session title to cmux tab and workspace titles."""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys

DB_PATH = os.path.expanduser("~/.gemini/antigravity-cli/conversation_summaries.db")
DEFAULT_CMUX_CLI = "/Applications/cmux.app/Contents/Resources/bin/cmux"
DEFAULT_CMUX_SOCK = os.path.expanduser("~/.local/state/cmux/cmux.sock")
MAX_TITLE_LEN = 50
MIN_UPDATE_PROMPT_LEN = 12


def normalize_title(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= MAX_TITLE_LEN:
        return text
    cut = text[:MAX_TITLE_LEN].rsplit(" ", 1)[0]
    return (cut or text[:MAX_TITLE_LEN]).rstrip(" .,:;-—") + "…"


def fallback_title(prompt: str) -> str:
    line = next((l.strip() for l in prompt.splitlines() if l.strip()), "")
    line = re.sub(r"[`*_#>\[\]]+", " ", line)
    return normalize_title(line.strip(" .,:;-—!?"))


def read_db_title(conversation_id: str) -> str:
    if not conversation_id or not os.path.exists(DB_PATH):
        return ""
    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=1.0)
        try:
            row = conn.execute(
                "SELECT title FROM conversation_summaries WHERE conversation_id = ?",
                (conversation_id,),
            ).fetchone()
            return (row[0] or "").strip() if row else ""
        finally:
            conn.close()
    except Exception:
        return ""


def find_cmux_cli() -> str | None:
    for candidate in (
        os.environ.get("CMUX_BUNDLED_CLI_PATH"),
        DEFAULT_CMUX_CLI,
        shutil.which("cmux"),
    ):
        if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def run_cmux(cli: str, sock: str, args: list[str]) -> None:
    cmd = [cli]
    if sock:
        cmd.extend(["--socket", sock])
    cmd.extend(args)
    env = os.environ.copy()
    env.setdefault("CMUXTERM_CLI_RESPONSE_TIMEOUT_SEC", "0.5")
    subprocess.run(
        cmd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=2,
        check=False,
    )


def load_state(path: str) -> dict[str, str]:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    return {}


def save_state(path: str, state: dict[str, str]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
    except Exception:
        pass


def main() -> None:
    surface_id = os.environ.get("CMUX_SURFACE_ID", "").strip()
    workspace_id = os.environ.get("CMUX_WORKSPACE_ID", "").strip()
    if not surface_id and not workspace_id:
        print("{}")
        return

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    conversation_id = (
        data.get("conversationId")
        or data.get("conversation_id")
        or ""
    ).strip()
    prompt = (data.get("lastUserInput") or data.get("prompt") or "").strip()

    cache_key = surface_id or workspace_id
    state_file = f"/tmp/cmux-agy-title-{cache_key}.json"
    state = load_state(state_file)
    if state.get("conversation_id") != conversation_id:
        state = {"conversation_id": conversation_id}

    db_title = read_db_title(conversation_id)
    prev_title = state.get("title", "")
    prev_db_title = state.get("db_title", "")

    title = ""
    if prompt:
        candidate = fallback_title(prompt)
        if candidate and (not prev_title or len(prompt) >= MIN_UPDATE_PROMPT_LEN):
            title = candidate
    elif db_title and db_title != prev_db_title:
        title = normalize_title(db_title)
    elif not prev_title and db_title:
        title = normalize_title(db_title)

    if db_title:
        state["db_title"] = db_title

    if not title or title == prev_title:
        save_state(state_file, state)
        print("{}")
        return

    cli = find_cmux_cli()
    if cli:
        sock = os.environ.get("CMUX_SOCKET_PATH", "").strip() or DEFAULT_CMUX_SOCK
        if not os.path.exists(sock):
            sock = ""
        if surface_id:
            run_cmux(cli, sock, ["rename-tab", "--surface", surface_id, "--title", title])
        if workspace_id:
            run_cmux(cli, sock, ["rename-workspace", "--workspace", workspace_id, "--", title])
        state["title"] = title
        save_state(state_file, state)

    print("{}")


if __name__ == "__main__":
    main()
