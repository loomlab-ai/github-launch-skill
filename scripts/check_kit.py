#!/usr/bin/env python3
"""Check the github-launch-skill kit. Python stdlib only."""

from __future__ import annotations

import filecmp
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "skills" / "github-launch" / "assets"
SKILL = ROOT / "skills" / "github-launch" / "SKILL.md"

REQUIRED = [
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "CONTRIBUTING.md",
    ".gitignore",
    "llms.txt",
    "docs/llms.txt",
    "docs/index.html",
    "docs/.nojekyll",
    "skills/github-launch/SKILL.md",
    ".github/workflows/ci.yml",
    "scripts/check_kit.py",
    "templates/README.md.tmpl",
    "templates/README.zh-CN.md.tmpl",
    "templates/ABOUT.txt",
    "templates/llms.txt.tmpl",
    "templates/LICENSE.MIT.txt",
    "templates/.github/workflows/ci.yml.tmpl",
    "templates/docs/index.md.tmpl",
    "templates/docs/index.html.tmpl",
    "templates/CHECKLIST.md",
]

EN_H2 = [
    "Why",
    "Quick start",
    "Features",
    "Install",
    "Usage",
    "Configuration",
    "FAQ",
    "License",
    "Contact",
]
ZH_H2 = [
    "为什么",
    "快速开始",
    "功能",
    "安装",
    "用法",
    "配置",
    "常见问题",
    "许可证",
    "联系",
]

LINK_FILES = [
    "README.md",
    "README.zh-CN.md",
    "CONTRIBUTING.md",
    "skills/github-launch/SKILL.md",
    "docs/index.html",
    "llms.txt",
    "docs/llms.txt",
]

PUBLIC_COPY = [
    "README.md",
    "README.zh-CN.md",
    "docs/index.html",
    "llms.txt",
    "docs/llms.txt",
]

TOKEN_FREE = PUBLIC_COPY + ["CONTRIBUTING.md"]

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def headings(text: str, level: int) -> list[str]:
    prefix = "#" * level + " "
    found = []
    for line in text.splitlines():
        if line.startswith(prefix) and not line.startswith(prefix + "#"):
            found.append(line[len(prefix) :].strip())
    return found


def slug(heading: str) -> str:
    chars: list[str] = []
    for ch in heading.strip().lower():
        if ch.isalnum() or ch in "-_":
            chars.append(ch)
        elif ch.isspace():
            chars.append("-")
    text = "".join(chars)
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md is missing YAML frontmatter")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        fail("SKILL.md frontmatter is not closed")
        return {}
    lines = text[4:end].splitlines()
    data: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line[0] in " \t":
            fail(f"SKILL.md frontmatter has an unexpected indent: {line!r}")
            return data
        key, _, rest = line.partition(":")
        rest = rest.strip()
        i += 1
        if rest in {">", ">-", "|", "|-"}:
            block: list[str] = []
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(block) if rest.startswith(">") else "\n".join(block)
            continue
        if rest == "":
            nested: list[str] = []
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                nested.append(lines[i].strip())
                i += 1
            data[key] = "\n".join(nested)
            continue
        if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in {'"', "'"}:
            rest = rest[1:-1]
        data[key] = rest
    return data


def files_under(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    found: dict[str, Path] = {}
    for path in root.rglob("*"):
        if path.is_file():
            found[path.relative_to(root).as_posix()] = path
    return found


def sync_assets() -> None:
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    shutil.copytree(TEMPLATES, ASSETS)


def field(text: str, key: str) -> str:
    prefix = key + ":"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return ""


def strip_markdown_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def check_links(rel: str) -> None:
    path = ROOT / rel
    raw = path.read_text(encoding="utf-8")
    text = strip_markdown_code(raw) if rel.endswith(".md") else raw
    slugs = {slug(item) for item in headings(raw, 1) + headings(raw, 2) + headings(raw, 3)}
    targets = re.findall(r"\]\(([^)\s]+)", text)
    targets += re.findall(r'(?:href|src)="([^"]+)"', text)
    for target in targets:
        if "{{" in target or target.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        fragment = ""
        path_part = target
        if "#" in target:
            path_part, fragment = target.split("#", 1)
        if path_part == "":
            if fragment and fragment not in slugs:
                fail(f"{rel}: missing heading #{fragment}")
            continue
        dest = (path.parent / path_part).resolve()
        try:
            dest.relative_to(ROOT)
        except ValueError:
            fail(f"{rel}: link escapes the repo: {target}")
            continue
        if not dest.exists():
            fail(f"{rel}: broken link {target}")


def check_placeholders(rel: str, required: list[str]) -> None:
    text = read(rel)
    for token in required:
        if token not in text:
            fail(f"{rel}: missing placeholder {token}")


def normalized_mit(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("Copyright (c) "):
            lines.append("Copyright (c) YEAR HOLDER")
        else:
            lines.append(line)
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    if "--sync-assets" in sys.argv:
        sync_assets()

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            fail(f"missing {rel}")
    if ERRORS:
        report()
        return 1

    skill_text = read("skills/github-launch/SKILL.md")
    line_count = skill_text.count("\n") + (0 if skill_text.endswith("\n") else 1)
    if line_count > 500:
        fail(f"SKILL.md is {line_count} lines; keep it at 500 or fewer")

    meta = parse_frontmatter(skill_text)
    if meta.get("name") != "github-launch":
        fail(f"SKILL.md name is {meta.get('name')!r}, want github-launch")
    description = meta.get("description", "")
    if not 1 <= len(description) <= 1024:
        fail(f"SKILL.md description length is {len(description)}")
    for phrase in (
        "ship this to GitHub",
        "上架 GitHub",
        "准备开源",
        "does not block git push",
    ):
        if phrase not in description:
            fail(f"SKILL.md description missing {phrase!r}")
    for phrase in ("soft skill", "git push", "llms.txt", "160"):
        if phrase not in skill_text:
            fail(f"SKILL.md body missing {phrase!r}")
    if "author: loomlab" not in meta.get("metadata", ""):
        fail("SKILL.md metadata.author is not loomlab")

    en = read("README.md")
    zh = read("README.zh-CN.md")
    if headings(en, 2) != EN_H2:
        fail(f"README.md H2 order is {headings(en, 2)}")
    if headings(zh, 2) != ZH_H2:
        fail(f"README.zh-CN.md H2 order is {headings(zh, 2)}")
    en_h3 = headings(en, 3)
    zh_h3 = headings(zh, 3)
    if len(en_h3) < 3 or len(en_h3) != len(zh_h3):
        fail(f"FAQ H3 counts differ: en={len(en_h3)} zh={len(zh_h3)}")
    if "does not block `git push`" not in en:
        fail("README.md does not say it does not block git push")
    if "不拦截 `git push`" not in zh:
        fail("README.zh-CN.md does not say it does not block git push")

    about = read("templates/ABOUT.txt")
    summary = field(about, "example_description")
    topics = [item.strip() for item in field(about, "example_topics").split(",") if item.strip()]
    homepage = field(about, "example_homepage")
    if not summary or len(summary) > 160:
        fail(f"example_description length is {len(summary)}")
    if not 5 <= len(topics) <= 10:
        fail(f"example_topics count is {len(topics)}")
    for topic in topics:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", topic):
            fail(f"illegal example topic {topic!r}")
    for rel in ("README.md", "README.zh-CN.md", "docs/index.html", "llms.txt"):
        if summary not in read(rel):
            fail(f"{rel}: missing the About description")
    for rel in ("README.md", "README.zh-CN.md"):
        if homepage not in read(rel):
            fail(f"{rel}: missing homepage {homepage}")
        for topic in topics:
            if f"`{topic}`" not in read(rel):
                fail(f"{rel}: missing topic {topic}")

    for rel in PUBLIC_COPY:
        text = read(rel)
        for needle in (
            "lofisuchat@gmail.com",
            "https://github.com/loomlab-ai",
            "https://x.com/su_lofi",
            "GitHub Sponsors",
        ):
            if needle not in text:
                fail(f"{rel}: missing contact {needle}")

    for path in (*files_under(TEMPLATES).values(), *files_under(ASSETS).values()):
        text = path.read_text(encoding="utf-8")
        for needle in ("lofisuchat", "su_lofi"):
            if needle in text:
                fail(f"{path.relative_to(ROOT)}: kit contact leaked into a template")

    for rel in TOKEN_FREE:
        found = re.findall(r"\{\{[A-Z0-9_]+\}\}", read(rel))
        if found:
            fail(f"{rel}: leftover placeholders {found}")

    banned_domain = "loomlab" + ".ai"
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".gif", ".webp"}:
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        if banned_domain in body:
            fail(f"{path.relative_to(ROOT)}: contains an unrelated product domain")

    license_text = read("LICENSE")
    if "Copyright (c) 2026 LoomLab" not in license_text:
        fail("LICENSE copyright line is not Copyright (c) 2026 LoomLab")
    if "Permission is hereby granted" not in license_text:
        fail("LICENSE is not the MIT grant")
    if normalized_mit(license_text) != normalized_mit(read("templates/LICENSE.MIT.txt")):
        fail("templates/LICENSE.MIT.txt drifted from LICENSE")

    html = read("docs/index.html")
    for attr in (
        "<title>",
        'name="description"',
        'rel="canonical"',
        'property="og:title"',
        'property="og:description"',
        'property="og:url"',
        'type="application/ld+json"',
    ):
        if attr not in html:
            fail(f"docs/index.html missing {attr}")
    described = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not described or len(described.group(1)) > 160:
        fail("docs/index.html meta description missing or longer than 160")
    canonical = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    og_url = re.search(r'<meta property="og:url" content="([^"]*)"', html)
    if (
        not canonical
        or not og_url
        or canonical.group(1) != homepage
        or og_url.group(1) != homepage
    ):
        fail("canonical, og:url, and example_homepage disagree")
    match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
        flags=re.S,
    )
    if not match:
        fail("docs/index.html JSON-LD block missing")
    else:
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            fail(f"docs/index.html JSON-LD does not parse: {exc}")
        else:
            if data.get("@type") != "SoftwareSourceCode":
                fail("JSON-LD @type is not SoftwareSourceCode")
            if data.get("name") != "github-launch-skill":
                fail("JSON-LD name is not github-launch-skill")

    if read("llms.txt") != read("docs/llms.txt"):
        fail("docs/llms.txt is not the same file as llms.txt")
    llms = read("llms.txt")
    if not llms.startswith("# github-launch-skill\n"):
        fail("llms.txt must start with the project H1")
    if "\n> " not in llms:
        fail("llms.txt is missing the blockquote summary")

    workflow = read(".github/workflows/ci.yml")
    for needle in ("actions/checkout@v7", "permissions:", "python3 scripts/check_kit.py"):
        if needle not in workflow:
            fail(f"ci.yml missing {needle}")
    starter = read("templates/.github/workflows/ci.yml.tmpl")
    for needle in (
        "actions/checkout@v7",
        "permissions:",
        "hashFiles",
        "test -f README.md",
        "test -f LICENSE",
    ):
        if needle not in starter:
            fail(f"ci.yml.tmpl missing {needle}")

    ignore = read(".gitignore")
    if ".env" not in ignore:
        fail(".gitignore does not ignore .env")

    check_placeholders(
        "templates/README.md.tmpl",
        [
            "{{PROJECT_NAME}}",
            "{{ONE_LINER}}",
            "{{WHY}}",
            "{{QUICKSTART}}",
            "{{FEATURES}}",
            "{{INSTALL}}",
            "{{USAGE}}",
            "{{CONFIGURATION}}",
            "{{FAQ}}",
            "{{LICENSE_LINE}}",
            "{{CONTACT}}",
        ],
    )
    check_placeholders(
        "templates/README.zh-CN.md.tmpl",
        [
            "{{PROJECT_NAME}}",
            "{{ONE_LINER_ZH}}",
            "{{WHY_ZH}}",
            "{{QUICKSTART_ZH}}",
            "{{FEATURES_ZH}}",
            "{{INSTALL_ZH}}",
            "{{USAGE_ZH}}",
            "{{CONFIGURATION_ZH}}",
            "{{FAQ_ZH}}",
            "{{LICENSE_LINE_ZH}}",
            "{{CONTACT_ZH}}",
        ],
    )
    for rel, token in (
        ("templates/ABOUT.txt", "{{ABOUT_DESCRIPTION}}"),
        ("templates/llms.txt.tmpl", "{{REPO_URL}}"),
        ("templates/CHECKLIST.md", "{{PROJECT_NAME}}"),
        ("templates/LICENSE.MIT.txt", "{{YEAR}}"),
        ("templates/LICENSE.MIT.txt", "{{COPYRIGHT_HOLDER}}"),
        ("templates/docs/index.md.tmpl", "{{PROJECT_NAME}}"),
        ("templates/docs/index.html.tmpl", "{{ABOUT_DESCRIPTION}}"),
        ("templates/docs/index.html.tmpl", "{{HOMEPAGE_URL}}"),
    ):
        if token not in read(rel):
            fail(f"{rel}: missing {token}")

    template_files = files_under(TEMPLATES)
    asset_files = files_under(ASSETS)
    if set(template_files) != set(asset_files):
        fail(
            "templates/ and skills/github-launch/assets/ differ: "
            f"only templates {sorted(set(template_files) - set(asset_files))}, "
            f"only assets {sorted(set(asset_files) - set(template_files))}"
        )
    for rel_path in sorted(set(template_files) & set(asset_files)):
        same = filecmp.cmp(template_files[rel_path], asset_files[rel_path], shallow=False)
        if not same:
            fail(f"asset drifted from template: {rel_path}")

    for rel in LINK_FILES:
        check_links(rel)

    report()
    return 1 if ERRORS else 0


def report() -> None:
    if ERRORS:
        print("check_kit: FAIL")
        for item in ERRORS:
            print(f"- {item}")
    else:
        print("check_kit: ok")


if __name__ == "__main__":
    sys.exit(main())
