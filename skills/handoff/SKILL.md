---
name: handoff
description: Сводка текущего разговора в handoff-документ для продолжения в новой сессии.
argument-hint: "На чём сфокусироваться в следующей сессии?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Inside a workspace, save to `.scratch/<topic>/handoff.md` (globally gitignored and accessible to sandboxed sessions) and print its absolute path; outside a workspace, fall back to the OS temporary directory (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows).

Include a "suggested skills" section in the document, naming which skills the next agent should read and apply with the tools available in its environment.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
