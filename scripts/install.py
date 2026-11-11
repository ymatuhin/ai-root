#!/usr/bin/env python3
"""Link shared agent instructions and skills, backing up existing destinations."""

from datetime import datetime
from pathlib import Path
import os
import shutil


ROOT = Path(__file__).resolve().parent.parent
HOME_DIR = Path.home()
BACKUP = HOME_DIR / '.local/state/ai-root/backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')


def backup(path):
    destination = BACKUP / (path.relative_to(HOME_DIR) if path.is_relative_to(HOME_DIR) else Path('external') / path.relative_to(path.anchor))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(destination))
    print(f'Backup: {path} -> {destination}')


def link(source, destination):
    if destination.is_symlink() and destination.resolve() == source.resolve():
        return
    if destination.exists() or destination.is_symlink():
        backup(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(source, target_is_directory=source.is_dir())
    print(f'Link: {destination} -> {source}')


def main():
    skills = sorted(path.parent for path in (ROOT / 'skills').glob('*/SKILL.md'))
    if not skills or not (ROOT / 'AGENTS.md').is_file():
        raise SystemExit('Missing shared skills or AGENTS.md')

    claude_skills = HOME_DIR / '.claude/skills'
    # Preserve the old repository, including its history and uncommitted files.
    if (claude_skills / '.git').exists():
        backup(claude_skills)

    codex_dir = Path(os.environ.get('CODEX_HOME', HOME_DIR / '.codex')).expanduser()
    opencode_dir = Path(os.environ.get('XDG_CONFIG_HOME', HOME_DIR / '.config')).expanduser() / 'opencode'
    for destination in [HOME_DIR / '.claude/CLAUDE.md', codex_dir / 'AGENTS.md', opencode_dir / 'AGENTS.md']:
        link(ROOT / 'AGENTS.md', destination)

    for skill in skills:
        # Codex uses the common user directory; remove legacy copies to avoid duplicates.
        legacy = codex_dir / 'skills' / skill.name
        if legacy.exists() or legacy.is_symlink():
            backup(legacy)
        for directory in [claude_skills, HOME_DIR / '.agents/skills', opencode_dir / 'skills']:
            link(skill, directory / skill.name)

    for rule in sorted((ROOT / 'rules/codex').glob('*.rules')):
        link(rule, codex_dir / 'rules' / rule.name)
    link(ROOT / 'workspace/AGENTS.md', ROOT.parent / 'AGENTS.md')
    link(ROOT / 'workspace/AGENTS.md', ROOT.parent / 'CLAUDE.md')
    print(f'Connected {len(skills)} skills, global instructions and workspace map.')


if __name__ == '__main__':
    main()
