# github-launch-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml)

把你的项目上架到 GitHub 的 Agent Skill。

当你说「ship this to GitHub」、「上架 GitHub」或「准备开源」时，编码代理会加载它。代理会写上架所需的文件：双语 README、About 文案、许可证、CI、Pages 落地页、GEO 说明，并填一张检查清单。它不拦截 `git push`。

[English](README.md)

## 为什么

公开仓库被人从第一屏判断：它是什么、怎么跑、用什么许可证、有没有人维护。之后搜索引擎和语言模型引用的也是这一屏。这个技能就是项目公开前的打包步骤。它写文件和检查清单，而不是丢下一串建议就停。

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

其他代理和用户级路径见[安装](#安装)。步骤写在 [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md)。

## 功能

- 项目登记：仓库类型、读者、语言
- 代码内容审查：密钥、个人隐私、失效演示、许可证头、`.gitignore`、大体积二进制
- `README.md`（英文）和 `README.zh-CN.md`，结构相同、事实相同
- GitHub About 描述（不超过 160 个字符）和 5–10 个 topics
- LICENSE：默认 MIT；需要专利授权时用 Apache-2.0，需要网络 copyleft 时用 AGPL-3.0
- 一份尽量短的 GitHub Actions 工作流，做 lint、测试或文档检查
- 从 `/docs` 提供 GitHub Pages，并写明打开它的点击路径（技能不会替你打开 Pages）
- GEO 与 SEO：稳定标题、FAQ、`llms.txt`、Pages 的 meta
- 代理填写的发布检查清单，状态为 `pass`、`fail` 或 `skip`

## 安装

把 `skills/github-launch/` 复制到代理已经在读的技能目录。该目录里的 `assets/` 与 [templates/](templates/CHECKLIST.md) 字节相同，只复制技能文件夹即可。若希望从仓库根目录读 `templates/`，克隆整个仓库。

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

技能没有出现时，重开一次会话。用自然语言触发，没有必须的斜杠命令。

## 用法

1. 安装技能。
2. 打开要发布的项目。对那个项目执行步骤，不要对这个工具仓库执行，除非你正在改这个工具仓库。
3. 说：`ship this to GitHub`、`上架 GitHub` 或 `准备开源`。
4. 看 diff 和 `.github/PUBLISH_CHECKLIST.md`。代理遵循 [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md) 和 [templates/](templates/README.md.tmpl) 下的模板。
5. 密钥检查为通过、且你希望分支在 GitHub 上时，再推送。本仓库没有拒绝 `git push` 的钩子。

代理会读这些路径：

```text
skills/github-launch/SKILL.md
skills/github-launch/assets/     # 与 templates/ 字节相同
templates/
docs/                            # Pages 源文件；在 Settings 里打开
scripts/check_kit.py             # 本仓库的 CI
```

Pages 需要你自己打开：**Settings → Pages → Deploy from a branch**，目录选 **`/docs`**。落地页是 [docs/index.html](docs/index.html)。空文件 [docs/.nojekyll](docs/.nojekyll) 用来阻止 Jekyll 改写 HTML。站点可访问之后，主页是 `https://loomlab-ai.github.io/github-launch-skill/`。把这个 URL 填进 About 的 homepage。本仓库不会替你打开 Pages。

建议的 About 描述（105 个字符）：

```text
Agent Skill that launches your project onto GitHub: bilingual README, About, license, Pages, CI, and SEO.
```

建议的 topics：`agent-skills`、`github`、`readme`、`seo`、`cicd`、`open-source`、`cursor`、`claude`。

About 描述和 topics 用这一份英文。GitHub 的 About 栏不是双语字段。

## 配置

没有配置文件。代理从目标仓库读取项目名、读者、版权持有者和公开联系方式。目标仓库没有公开联系方式时，只链接 GitHub 所有者，不编造邮箱。它不会编造个人姓名、电话或雇主，也不会把本仓库的联系方式抄过去。

首次上架时，代理可以改 README、补上缺失的 `LICENSE`、`.gitignore`、`.github/workflows/ci.yml`、`docs/`、`llms.txt` 和 `.github/PUBLISH_CHECKLIST.md`。它不改写历史。发布之后可以删掉检查清单。

新项目的默认许可证是 MIT。已有的 `LICENSE` 保持不动，除非你明确要求更换。

## 常见问题

### 这个技能会阻止 git push 吗？

不会。它是软技能：一份步骤和一张清单。它不安装 git hook，不设置 GitHub ruleset，也不用工具权限拒绝 `git push`。

### 它会打开 GitHub Pages 吗？

不会。它可以添加 `/docs` 站点，并给出要填进 About 的主页 URL。你在 Settings → Pages → Deploy from a branch → `/docs` 里打开 Pages。见[用法](#用法)。

### 它会选哪种许可证？

MIT。仓库里已有许可证，或你需要 Apache-2.0（专利授权）或 AGPL-3.0（网络 copyleft）时除外。它不会悄悄换许可证。

### 中英文 README 如何保持一致？

章节顺序相同，命令相同，版本号相同。一次改动如果动了其中一个文件，就要同时改另一个。

### 如果项目还不该公开呢？

直接说。技能仍会写打包文件。除非你明确要求把仓库设为公开，否则它不改可见性；密钥检查未通过时，它也不会改成公开。

## 许可证

[MIT](LICENSE)。Copyright (c) 2026 LoomLab。

## 联系

[LoomLab](https://github.com/loomlab-ai) · [lofisuchat@gmail.com](mailto:lofisuchat@gmail.com) · GitHub Sponsors · [X @su_lofi](https://x.com/su_lofi)
