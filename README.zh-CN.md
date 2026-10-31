# github-launch-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/loomlab-ai/github-launch-skill/actions/workflows/ci.yml)

用 Agent Skill 把项目上架到 GitHub。

对代理说「ship this to GitHub」「上架 GitHub」或「准备开源」，就会加载本技能。它会写双语 README、About、许可证、CI 和 Pages 落地页，并写稳定标题和 Pages meta，再填检查清单。不拦截 `git push`。

[English](README.md)

## 用途

公开仓库的第一屏要写清：项目是什么、怎么跑、许可证、有没有人维护。搜索引擎和语言模型会引用这一屏。本技能在公开前写好这些文件，并填检查清单。

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

- 收集仓库类型、使用对象、语言
- 审查密钥、个人隐私、失效演示、许可证头、`.gitignore`、大体积二进制
- 写 `README.md` 与 `README.zh-CN.md`：章节顺序、命令、版本号相同
- 写 GitHub About（不超过 160 个字符）和 5–10 个 topics
- 许可证默认 MIT；需要专利授权时用 Apache-2.0，需要网络 copyleft 时用 AGPL-3.0
- 添加简短的 GitHub Actions 工作流（lint、测试或文档检查）
- 准备 `/docs` 下的 GitHub Pages，并写明在 Settings 里如何打开。技能不会替你打开 Pages
- GEO 与 SEO：稳定标题和 Pages meta
- 发布检查清单，由代理填写 `pass` / `fail` / `skip`
- 中文稿写完后做 doc-lint：删冗余、套话和翻译腔，保留技术术语和原意

## 安装

把 `skills/github-launch/` 复制到代理已经在读的技能目录。该目录里的 `assets/` 与 [templates/](templates/CHECKLIST.md) 相同，复制技能文件夹即可。要从仓库根目录读 `templates/`，再克隆整个仓库。

| 代理 | 当前项目 | 所有项目 |
| --- | --- | --- |
| Cursor | `.cursor/skills/` 或 `.agents/skills/` | `~/.cursor/skills/` 或 `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.opencode/skills/` 或 `.agents/skills/` | `~/.config/opencode/skills/` 或 `~/.agents/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Cursor 还会加载 `.claude/skills/`、`.codex/skills/`，以及主目录下的同名目录。Codex 没有列出本技能时，把同一文件夹再复制到 `~/.codex/skills/`。

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

技能没有出现时，新开一次会话。用自然语言触发，不需要斜杠命令。

## 用法

1. 安装技能。
2. 打开要发布的项目，在该项目里执行。只有正在修改本工具仓库时，才对本仓库执行。
3. 说：`ship this to GitHub`、`上架 GitHub` 或 `准备开源`。
4. 查看 diff 和 `.github/PUBLISH_CHECKLIST.md`。代理按 [skills/github-launch/SKILL.md](skills/github-launch/SKILL.md) 和 [templates/](templates/README.md.tmpl) 里的模板执行。
5. 密钥检查通过，并且你要把分支推到 GitHub 时，再推送。本仓库没有拒绝 `git push` 的钩子。

代理读取这些路径：

```text
skills/github-launch/SKILL.md
skills/github-launch/assets/     # 与 templates/ 内容相同
templates/
docs/                            # Pages 源文件；在 Settings 里打开
scripts/check_kit.py             # 本仓库的 CI
```

Pages 需自行打开：**Settings → Pages → Deploy from a branch**，目录选 **`/docs`**。落地页是 [docs/index.html](docs/index.html)。空文件 [docs/.nojekyll](docs/.nojekyll) 用来阻止 Jekyll 改写 HTML。站点可访问后，主页是 `https://loomlab-ai.github.io/github-launch-skill/`。把这个 URL 填进 About 的 homepage。本仓库不会替你打开 Pages。

建议的 About 描述（97 个字符）：

```text
Agent Skill that packages a project for GitHub: bilingual README, About, license, CI, Pages, SEO.
```

建议的 topics：`agent-skills`、`github`、`readme`、`seo`、`cicd`、`open-source`、`cursor`、`claude`。

About 描述和 topics 用上面这份英文。GitHub About 不是双语字段。

## 配置

没有配置文件。项目名、使用对象、版权持有者和公开联系方式都从目标仓库读取。目标仓库没有公开联系方式时，只链接 GitHub 所有者，不编造邮箱。不编造姓名、电话或雇主，也不抄本仓库的联系方式。

首次上架可以改 README，并补上缺失的 `LICENSE`、`.gitignore`、`.github/workflows/ci.yml`、`docs/` 和 `.github/PUBLISH_CHECKLIST.md`。不改写历史。发布后可以删掉检查清单。

新项目默认许可证为 MIT。已有 `LICENSE` 保持不动，除非你明确要求更换。

除非你明确要求把仓库改为公开，否则不改可见性。密钥检查未通过时，不改为公开。

## 许可证

[MIT](LICENSE)。Copyright (c) 2026 LoomLab。

## 联系

[LoomLab](https://github.com/loomlab-ai) · [lofisuchat@gmail.com](mailto:lofisuchat@gmail.com) · GitHub Sponsors · [X @su_lofi](https://x.com/su_lofi)
