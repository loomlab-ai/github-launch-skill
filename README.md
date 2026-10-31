# github-launch-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml)

Agent Skill that launches your project onto GitHub.

Coding agents load it when you say "ship this to GitHub", "上架 GitHub", or "准备开源". The agent writes the packaging files — bilingual README, About text, license, CI, a Pages landing, GEO notes — and fills a checklist. It does not block `git push`.

[中文说明](README.zh-CN.md)

## Why

A public repository is judged from the first screen: what it is, how to run it, the license, and whether anyone maintains it. Later, search engines and language models quote that same screen. This skill is the packaging pass before the project is public. It writes files and a checklist. It does not hand you a list of tips and stop.

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

Other agents and the user-level paths are in [Install](#install). The procedure is [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md).

## Features

- Project intake: repository kind, audience, and languages
- Code-content review: secrets, personal data, dead demos, license headers, `.gitignore`, large binaries
- `README.md` (English) and `README.zh-CN.md`, same structure and the same facts
- GitHub About description (160 characters or fewer) and 5–10 topics
- LICENSE choice: MIT by default; Apache-2.0 or AGPL-3.0 when the project needs that grant or that copyleft
- A minimal GitHub Actions workflow for lint, test, or a docs check
- GitHub Pages from `/docs`, plus the clicks that turn it on (the skill does not enable Pages)
- GEO and SEO: stable headings, an FAQ, `llms.txt`, and meta tags on the Pages landing
- A publish checklist the agent fills with `pass`, `fail`, or `skip`

## Install

Copy `skills/github-launch/` into a skills directory your agent already reads. The folder includes `assets/`, the same files as [templates/](templates/CHECKLIST.md), so one copy is enough. Copy the whole kit if you would rather read `templates/` at the repository root.

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

Restart the session if the skill does not show up. You invoke it by asking. There is no required slash command.

## Usage

1. Install the skill.
2. Open the project to publish. Run the procedure on that project, not on this kit, unless you are changing the kit.
3. Ask: `ship this to GitHub`, `上架 GitHub`, or `准备开源`.
4. Read the diff and `.github/PUBLISH_CHECKLIST.md`. The agent follows [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md) and the files under [templates/](templates/README.md.tmpl).
5. Push when the checklist's secret scan passed and you want the branch on GitHub. Nothing in this repository refuses `git push`.

What the agent reads:

```text
skills/github-launch/SKILL.md
skills/github-launch/assets/     # same bytes as templates/
templates/
docs/                            # Pages source; enable it in Settings
scripts/check_kit.py             # CI for this kit
```

Enable Pages yourself: **Settings → Pages → Deploy from a branch**, folder **`/docs`**. The landing file is [docs/index.html](docs/index.html). An empty [docs/.nojekyll](docs/.nojekyll) keeps Jekyll from rewriting it. After the site loads, the homepage is `https://loomlab-ai.github.io/github-launch-skill/`. Put that URL in the About homepage field. This repository does not turn Pages on.

Suggested About description (105 characters):

```text
Agent Skill that launches your project onto GitHub: bilingual README, About, license, Pages, CI, and SEO.
```

Suggested topics: `agent-skills`, `github`, `readme`, `seo`, `cicd`, `open-source`, `cursor`, `claude`.

## Configuration

No configuration file. The agent takes the project name, audience, copyright holder, and public contact from the target repository. If the target has no public contact, it links the GitHub owner and leaves out an email. It does not invent a person, a phone number, or an employer, and it does not reuse this kit's contact line.

On a first launch the agent may edit README files, `LICENSE` (only if missing), `.gitignore`, `.github/workflows/ci.yml`, `docs/`, `llms.txt`, and `.github/PUBLISH_CHECKLIST.md`. It does not rewrite history. You can delete the checklist file after you publish.

Default license for a new project is MIT. An existing `LICENSE` stays unless you ask for a different one.

## FAQ

### Does this skill block git push?

No. It is a soft skill: a procedure and a checklist. It does not install a git hook, a GitHub ruleset, or a tool permission that rejects `git push`.

### Will it enable GitHub Pages?

No. It can add a `/docs` site and the homepage URL to put in About. You enable Pages under Settings → Pages → Deploy from a branch → `/docs`. See [Usage](#usage).

### Which license does it pick?

MIT, unless the repository already has a license, or you need Apache-2.0 (patent grant) or AGPL-3.0 (network copyleft). It will not swap a license silently.

### How do the English and Chinese READMEs stay aligned?

Same section order, same commands, same version numbers. A change to one file in a task includes the other.

### What if the project should not be public yet?

Say so. The skill still writes the packaging files. It does not change repository visibility unless you explicitly tell it to make the repo public, and it will not do that while a secret scan is failing.

## License

[MIT](LICENSE). Copyright (c) 2026 LoomLab.

## Contact

[LoomLab](https://github.com/loomlab-ai) · [lofisuchat@gmail.com](mailto:lofisuchat@gmail.com) · GitHub Sponsors · [X @su_lofi](https://x.com/su_lofi)
