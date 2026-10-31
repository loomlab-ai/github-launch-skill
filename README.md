# github-launch-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml)

An Agent Skill that packages a project for GitHub.

Say "ship this to GitHub", "上架 GitHub", or "准备开源" and the agent loads it. It writes a bilingual README, About, license, CI, a Pages landing, GEO notes, and a checklist. It does not block `git push`.

[中文说明](README.zh-CN.md)

## Purpose

Someone opening a public repository starts with the first screen: what the project is, how to run it, the license, and whether anyone maintains it. Search engines and language models quote that screen. This skill packages the project before it is public by writing the files and filling the checklist.

## Quick start

```bash
git clone https://github.com/loomlab-ai/github-launch-skill.git
mkdir -p .cursor/skills
cp -R github-launch-skill/skills/github-launch .cursor/skills/github-launch
```

Open the project you want to publish and tell the agent:

```text
ship this to GitHub
```

Other agents and user-level paths are in [Install](#install). The steps are in [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md).

## Features

- Collect project facts: repository kind, audience, and languages
- Review repository contents: secrets, personal data, dead demos, license headers, `.gitignore`, and large binaries
- Write `README.md` (English) and `README.zh-CN.md` with the same structure and the same facts
- Write a GitHub About description (160 characters or fewer) and 5–10 topics
- License: MIT by default; Apache-2.0 when you need a patent grant, AGPL-3.0 when you need network copyleft
- Add a short GitHub Actions workflow (lint, test, or a docs check)
- Prepare GitHub Pages under `/docs`, and state how to turn it on in Settings (the skill does not enable Pages)
- GEO and SEO: stable headings, an FAQ, and Pages meta
- A publish checklist the agent fills with `pass`, `fail`, or `skip`

## Install

Copy `skills/github-launch/` into a skills directory the agent already reads. The `assets/` directory in that folder matches [templates/](templates/CHECKLIST.md), so copying the skill folder is enough. Clone the whole repository when you want to read `templates/` from the repository root.

| Agent | This project | All projects |
| --- | --- | --- |
| Cursor | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` or `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.opencode/skills/` or `.agents/skills/` | `~/.config/opencode/skills/` or `~/.agents/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Cursor also loads `.claude/skills/`, `.codex/skills/`, and those directories under your home folder. If Codex does not list the skill, copy the same folder to `~/.codex/skills/` as well.

```bash
git clone https://github.com/loomlab-ai/github-launch-skill.git

mkdir -p .cursor/skills
cp -R github-launch-skill/skills/github-launch .cursor/skills/

mkdir -p .claude/skills
cp -R github-launch-skill/skills/github-launch .claude/skills/

mkdir -p .opencode/skills
cp -R github-launch-skill/skills/github-launch .opencode/skills/

mkdir -p .agents/skills
cp -R github-launch-skill/skills/github-launch .agents/skills/
```

If the skill does not appear, start a new session. Trigger it in plain language. No slash command is required.

## Usage

1. Install the skill.
2. Open the project to publish. Run the steps on that project. Do not run them on this kit unless you are editing the kit.
3. Say: `ship this to GitHub`, `上架 GitHub`, or `准备开源`.
4. Review the diff and `.github/PUBLISH_CHECKLIST.md`. The agent follows [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md) and the templates under [templates/](templates/README.md.tmpl).
5. Push when the secret check has passed and you want the branch on GitHub. This repository has no hook that refuses `git push`.

What the agent reads:

```text
skills/github-launch/SKILL.md
skills/github-launch/assets/     # same files as templates/
templates/
docs/                            # Pages source; enable it in Settings
scripts/check_kit.py             # CI for this kit
```

Turn Pages on yourself: **Settings → Pages → Deploy from a branch**, folder **`/docs`**. The landing page is [docs/index.html](docs/index.html). The empty file [docs/.nojekyll](docs/.nojekyll) stops Jekyll from rewriting the HTML. Once the site is reachable, the homepage is `https://loomlab-ai.github.io/github-launch-skill/`. Put that URL in the About homepage field. This repository will not turn Pages on for you.

Suggested About description (97 characters):

```text
Agent Skill that packages a project for GitHub: bilingual README, About, license, CI, Pages, SEO.
```

Suggested topics: `agent-skills`, `github`, `readme`, `seo`, `cicd`, `open-source`, `cursor`, `claude`.

## Configuration

No configuration file. The agent reads the project name, audience, copyright holder, and public contact from the target repository. If the target has no public contact, it links the GitHub owner and does not invent an email. It does not invent a personal name, phone number, or employer, and it does not copy this repository's contact line.

On a first launch, the agent may edit the README and add these files when they are missing: `LICENSE`, `.gitignore`, `.github/workflows/ci.yml`, `docs/`, and `.github/PUBLISH_CHECKLIST.md`. It does not rewrite history. You can delete the checklist after you publish.

The default license for a new project is MIT. An existing `LICENSE` stays unless you explicitly ask to change it.

## FAQ

### Does this skill block git push?

No. It is a soft skill: steps plus a checklist. It does not install a git hook, set a GitHub ruleset, or use a tool permission to reject `git push`.

### Will it enable GitHub Pages?

No. It can add a `/docs` site and the homepage URL to put in About. Turn Pages on under Settings → Pages → Deploy from a branch → `/docs`. See [Usage](#usage).

### Which license does it pick?

MIT by default, unless the repository already has a license, or you need Apache-2.0 (patent grant) or AGPL-3.0 (network copyleft). It will not swap a license silently.

### How do the English and Chinese READMEs stay aligned?

Same section order, commands, and version numbers. A change that touches one file must touch the other.

### What if the project should not be public yet?

Say so. The skill still writes the packaging files. It does not change visibility unless you explicitly ask it to make the repository public, and it will not do that while the secret check is failing.

## License

[MIT](LICENSE). Copyright (c) 2026 LoomLab.

## Contact

[LoomLab](https://github.com/loomlab-ai) · [lofisuchat@gmail.com](mailto:lofisuchat@gmail.com) · GitHub Sponsors · [X @su_lofi](https://x.com/su_lofi)
