#!/usr/bin/env python3
"""Regenerate the README Projects section from projects.json.

Usage: python3 scripts/generate_projects.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_JSON = ROOT / "projects.json"
README = ROOT / "README.md"
IMAGE_DIR = "assets/project-images"
IMAGE_WIDTH = 480
IMAGE_HEIGHT = 300
CARD_BGCOLOR = "#f6f8fa"

START_MARKER = "<!-- PROJECTS:START -->"
END_MARKER = "<!-- PROJECTS:END -->"


def render(projects):
    lines = [START_MARKER]
    for project in projects:
        if not project.get("include", True):
            continue
        name = project["name"]
        url = project["url"]
        lines.append('<table width="100%">')
        lines.append(f'<tr><td align="center" bgcolor="{CARD_BGCOLOR}">')
        if project.get("image"):
            image_src = f"{IMAGE_DIR}/{project['image']}"
            lines.append(
                f'<a href="{url}"><img src="{image_src}" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" alt="{name}"></a>'
            )
            lines.append("<br><br>")
        lines.append(f'<b><a href="{url}">{name}</a></b>')
        lines.append("<br>")
        lines.append(project["description"])
        lines.append("</td></tr>")
        lines.append("</table>")
        lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines).rstrip("\n")


def main():
    projects = json.loads(PROJECTS_JSON.read_text())
    section = render(projects)

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
