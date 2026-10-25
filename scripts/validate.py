#!/usr/bin/env python3
"""Check every skill: frontmatter limits, and that referenced files exist."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
    folder = skill.parent
    text = skill.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{skill}: missing frontmatter")
        continue
    fields = dict(
        (k.strip(), v.strip())
        for k, _, v in (line.partition(":") for line in m.group(1).splitlines() if ":" in line)
    )
    name, desc = fields.get("name", ""), fields.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errors.append(f"{skill}: name must be 1-64 chars of a-z, 0-9, hyphen")
    if name != folder.name:
        errors.append(f"{skill}: name '{name}' does not match folder '{folder.name}'")
    if "anthropic" in name or "claude" in name:
        errors.append(f"{skill}: name may not contain 'anthropic' or 'claude'")
    if not desc or len(desc) > 1024:
        errors.append(f"{skill}: description must be 1-1024 chars (got {len(desc)})")
    if re.search(r"<[a-z/]", desc):
        errors.append(f"{skill}: description may not contain XML tags")
    if len(text.splitlines()) > 500:
        errors.append(f"{skill}: SKILL.md over 500 lines")
    for ref in re.findall(r"`(references/[^`]+\.md)`", text):
        if not (folder / ref).is_file():
            errors.append(f"{skill}: missing {ref}")
    for md in (folder / "references").glob("*.md"):
        for ref in re.findall(r"`((?:references/)?[\w-]+\.md)`", md.read_text()):
            if not ((folder / ref).is_file() or (md.parent / ref).is_file()):
                errors.append(f"{md}: missing {ref}")

    for case in ("trigger-queries.json", "behavior-cases.json"):
        if not (folder / "evals" / case).is_file():
            errors.append(f"{folder}: missing evals/{case}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("ok")
