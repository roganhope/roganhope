#!/usr/bin/env python3
"""Regenerate the README Skills section from skills.json.

Usage: python3 scripts/generate_skills.py
"""
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = ROOT / "skills.json"
README = ROOT / "README.md"

START_MARKER = "<!-- SKILLS:START -->"
END_MARKER = "<!-- SKILLS:END -->"


def badge_url(skill):
    label = urllib.parse.quote(skill["name"].replace("-", "--"))
    color = skill["color"]
    url = f"https://img.shields.io/badge/{label}-{color}?style=flat-square"
    if skill.get("logo"):
        url += f"&logo={skill['logo']}"
        if skill.get("logoColor"):
            url += f"&logoColor={skill['logoColor']}"
    return url


def render_group(group, lines, depth):
    skills = [s for s in group.get("skills", []) if s.get("include", True)]
    subgroups = group.get("groups", [])
    if not skills and not subgroups:
        return
    lines.append(f"{'#' * depth} {group['label']}")
    for skill in skills:
        lines.append(f"![{skill['name']}]({badge_url(skill)})")
    if skills:
        lines.append("")
    for subgroup in subgroups:
        render_group(subgroup, lines, depth + 1)


def render(groups):
    lines = [START_MARKER]
    for group in groups:
        render_group(group, lines, 3)
    lines.append(END_MARKER)
    return "\n".join(lines).rstrip("\n")


def main():
    groups = json.loads(SKILLS_JSON.read_text())
    section = render(groups)

    readme = README.read_text()
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    if not pattern.search(readme):
        raise SystemExit(
            f"Could not find {START_MARKER} / {END_MARKER} markers in README.md"
        )
    readme = pattern.sub(section, readme)
    README.write_text(readme)


if __name__ == "__main__":
    main()
