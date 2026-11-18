#!/usr/bin/env python3
"""Set Herdr tab title from agent session prompts or OpenCode titles."""

from __future__ import annotations
import json
import os
import re
import subprocess
import sys
import urllib.request

HC_BIN = "/Users/ym/.local/bin/hc"
HERDR_APP_BIN = "/Users/ym/.local/bin/herdr-app"


def get_tab_id(terminal_id: str) -> str | None:
    try:
        out = subprocess.check_output(
            [HC_BIN, "get", terminal_id, "--json"],
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=3,
        )
        data = json.loads(out)
        return (data.get("labels") or {}).get("herdr.tab")
    except Exception:
        return None


def set_tab_title(terminal_id: str, title: str) -> None:
    title = re.sub(r"\s+", " ", title).strip()
    if not title:
        return
    tab_id = get_tab_id(terminal_id)
    if not tab_id:
        return
    subprocess.run(
        [HERDR_APP_BIN, "do", "tab.rename", "--id", tab_id, "--name", title[:60]],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=3,
        check=False,
    )


def fallback_title(prompt: str) -> str:
    line = next((l.strip() for l in prompt.splitlines() if l.strip()), "")
    line = re.sub(r"[`*_#>\[\]]+", " ", line)
    line = re.sub(r"\s+", " ", line).strip(" .,:;-—!?")
    if len(line) <= 44:
        return line
    cut = line[:44].rsplit(" ", 1)[0]
    return (cut or line[:44]).rstrip(" .,:;-—") + "…"


def generate_llm_title(prompt: str) -> str | None:
    snippet = prompt.strip()[:600]
    if not snippet:
        return None

    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps({
                "model": "gpt-4.1-mini",
                "messages": [{
                    "role": "user",
                    "content": f"Short 3-5 word title for this coding task, same language as prompt, no quotes:\n{snippet}",
                }],
                "max_tokens": 24,
            }).encode(),
            headers={
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                text = json.loads(resp.read())["choices"][0]["message"]["content"]
                return text.strip().strip("\"'`")
        except Exception:
            pass

    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={gemini_key}"
        req = urllib.request.Request(
            url,
            data=json.dumps({
                "contents": [{
                    "parts": [{
                        "text": f"Short 3-5 word title for this coding task, same language as prompt, no quotes:\n{snippet}",
                    }],
                }],
            }).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read())
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip().strip("\"'`")
        except Exception:
            pass

    return None


def main() -> None:
    terminal_id = os.environ.get("HC_TERMINAL_ID")
    is_agy = "--agy" in sys.argv

    if not terminal_id:
        if is_agy:
            print("{}")
        return

    if "--set" in sys.argv:
        idx = sys.argv.index("--set")
        if idx + 1 < len(sys.argv):
            set_tab_title(terminal_id, sys.argv[idx + 1])
        return

    if "--worker" in sys.argv:
        prompt = sys.stdin.read().strip()
        if prompt:
            title = generate_llm_title(prompt) or fallback_title(prompt)
            set_tab_title(terminal_id, title)
        return

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    agent = "agy" if is_agy else "codex"
    session_id = data.get("conversationId") or data.get("thread_id") or data.get("session_id") or terminal_id
    prompt = (data.get("lastUserInput") or data.get("prompt") or "").strip()

    marker = f"/tmp/herdr-title-{agent}-{session_id}"
    if prompt and not os.path.exists(marker):
        try:
            with open(marker, "w") as f:
                f.write(terminal_id)
        except Exception:
            pass
        proc = subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), "--worker"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        if proc.stdin:
            proc.stdin.write(prompt.encode("utf-8", errors="replace"))
            proc.stdin.close()

    if is_agy:
        print("{}")


if __name__ == "__main__":
    main()
