# github-launch-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml)

用 Agent Skill 把项目上架到 GitHub。

对代理说「ship this to GitHub」「上架 GitHub」或「准备开源」即可加载。代理会写双语 README、About、许可证、CI、Pages 落地页和 GEO 说明，并填检查清单；不拦截 `git push`。

[English](README.md)

## 用途

别人打开公开仓库，先看第一屏：项目是什么、怎么跑、许可证、是否有人维护。搜索引擎和语言模型也会引用这一屏。本技能在公开前完成打包：直接写文件并填检查清单，不只给建议。

## 快速开始

```bash
git clone https://github.com/loomlab-ai/github-launch-skill.git
mkdir -p .cursor/skills
cp -R github-launch-skill/skills/github-launch .cursor/skills/github-launch
```

打开要发布的项目，对代理说：

```text
ship this to GitHub
```

其他代理和用户目录下的路径见[安装](#安装)。步骤见 [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md)。

## 功能

- 收集项目信息：仓库类型、读者、语言
- 审查仓库内容：密钥、个人隐私、失效演示、许可证头、`.gitignore`、大体积二进制
- 写出结构相同、事实一致的 `README.md`（英文）与 `README.zh-CN.md`
- 写 GitHub About（不超过 160 个字符）和 5–10 个 topics
- 许可证：默认 MIT；需要专利授权用 Apache-2.0，需要网络 copyleft 用 AGPL-3.0
- 添加尽量短的 GitHub Actions 工作流（lint、测试或文档检查）
- 准备 `/docs` 下的 GitHub Pages，并写明在 Settings 里如何打开（技能不会替你打开 Pages）
- GEO 与 SEO：稳定标题、FAQ、Pages meta
- 发布检查清单，由代理填 `pass` / `fail` / `skip`

## 安装

把 `skills/github-launch/` 复制到代理已在读取的技能目录。该目录内的 `assets/` 与 [templates/](templates/CHECKLIST.md) 内容相同，复制技能文件夹即可。若要从仓库根目录读 `templates/`，再克隆整个仓库。

| 代理 | 当前项目 | 所有项目 |
| --- | --- | --- |
| Cursor | `.cursor/skills/` 或 `.agents/skills/` | `~/.cursor/skills/` 或 `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.opencode/skills/` 或 `.agents/skills/` | `~/.config/opencode/skills/` 或 `~/.agents/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Cursor 还会加载 `.claude/skills/`、`.codex/skills/`，以及主目录下的同名目录。如果 Codex 没有列出这个技能，把同一文件夹再复制到 `~/.codex/skills/`。

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

技能未出现时，重开一次会话。用自然语言触发，无需斜杠命令。

## 用法

1. 安装技能。
2. 打开要发布的项目。对本项目执行步骤；除非你在改本工具仓库，否则不要对它执行。
3. 说：`ship this to GitHub`、`上架 GitHub` 或 `准备开源`。
4. 查看 diff 与 `.github/PUBLISH_CHECKLIST.md`。代理按 [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md) 和 [templates/](templates/README.md.tmpl) 下的模板执行。
5. 密钥检查通过、且你希望分支出现在 GitHub 上时再推送。本仓库没有拒绝 `git push` 的钩子。

代理会读取这些路径：

```text
skills/github-launch/SKILL.md
skills/github-launch/assets/     # 与 templates/ 内容相同
templates/
docs/                            # Pages 源文件；在 Settings 里打开
scripts/check_kit.py             # 本仓库的 CI
```

Pages 需自行打开：**Settings → Pages → Deploy from a branch**，目录选 **`/docs`**。落地页是 [docs/index.html](docs/index.html)。空文件 [docs/.nojekyll](docs/.nojekyll) 用于阻止 Jekyll 改写 HTML。站点可访问后，主页为 `https://loomlab-ai.github.io/github-launch-skill/`。把该 URL 填入 About 的 homepage。本仓库不会替你打开 Pages。

建议的 About 描述（97 个字符）：

```text
Agent Skill that packages a project for GitHub: bilingual README, About, license, CI, Pages, SEO.
```

建议的 topics：`agent-skills`、`github`、`readme`、`seo`、`cicd`、`open-source`、`cursor`、`claude`。

About 描述和 topics 用这一份英文。GitHub 的 About 栏不是双语字段。

## 配置

没有配置文件。代理从目标仓库读取项目名、读者、版权持有者和公开联系方式。若目标仓库没有公开联系方式，只链接 GitHub 所有者，不编造邮箱。不会编造个人姓名、电话或雇主，也不会把本仓库的联系方式抄过去。

首次上架时，代理可改 README、补缺失的 `LICENSE`、`.gitignore`、`.github/workflows/ci.yml`、`docs/` 和 `.github/PUBLISH_CHECKLIST.md`。不改写历史。发布后可删除检查清单。

新项目默认许可证为 MIT。已有 `LICENSE` 保持不动，除非你明确要求更换。

## 常见问题

### 这个技能会阻止 git push 吗？

不会。它是软技能：步骤加清单。不安装 git hook，不设 GitHub ruleset，也不用工具权限拒绝 `git push`。

### 它会打开 GitHub Pages 吗？

不会。它可以添加 `/docs` 站点，并给出要填进 About 的主页 URL。在 Settings → Pages → Deploy from a branch → `/docs` 打开 Pages。见[用法](#用法)。

### 它会选哪种许可证？

默认 MIT。仓库已有许可证，或你需要 Apache-2.0（专利授权）或 AGPL-3.0（网络 copyleft）时除外。不会悄悄更换许可证。

### 中英文 README 如何保持一致？

章节顺序、命令、版本号相同。一次改动若动了其中一个文件，须同时改另一个。

### 如果项目还不该公开呢？

直接说明。技能仍会写打包文件。除非你明确要求把仓库设为公开，否则不改可见性；密钥检查未通过时也不会改为公开。

## 许可证

[MIT](LICENSE)。Copyright (c) 2026 LoomLab。

## 联系

[LoomLab](https://github.com/loomlab-ai) · [lofisuchat@gmail.com](mailto:lofisuchat@gmail.com) · GitHub Sponsors · [X @su_lofi](https://x.com/su_lofi)
