---
name: github-launch
description: >-
  Package a software project for public GitHub: bilingual README (English
  and zh-CN), About description and topics, LICENSE, GitHub Pages, minimal
  CI, GEO/SEO (stable headings, title, meta), a Chinese doc-lint pass,
  and a code-content review. Use
  when the user says "ship this to GitHub", "上架 GitHub", "准备开源",
  "publish to GitHub", or "open source this". Procedure only; it does not
  block git push.
license: MIT
compatibility: >-
  Cursor, Claude Code, OpenCode, and Codex. Needs git and a text editor.
  GitHub CLI is optional.
metadata:
  author: loomlab
  version: "1.0"
---

# Launch a project on GitHub

Soft skill. This file is the procedure. It is not a hard control: it does not register a hook, a required status check, or a permission rule that rejects `git push`. Same framing as a soft skill in an agent safety kit — documentation the agent follows, not a blocker. There is nothing to override.

Do the edits, write the checklist, and show it. Do not push while a secret or private-data item is `fail`. If the user still says to push, warn once in the checklist and do not fight the tool. Do not rewrite git history.

Do not copy this kit's contact details, topics, or copyright line into the target. Those belong to the github-launch-skill repository only. Take the target's name, owner, and contacts from that repo or from the user.

## When to run

Run when the user says any of:

- ship this to GitHub
- 上架 GitHub
- 准备开源
- publish to GitHub
- open source this
- github launch

Do not run it for an ordinary code change that happens to touch a README.

## Templates

Read the template, then write the target file. Do not invent a second outline.

Resolve the template root in order:

1. `<kit>/templates/` when this file is `<kit>/skills/github-launch/SKILL.md`.
2. [assets/](assets/README.md.tmpl) next to this file, when only the skill folder was copied. `assets/` is a byte copy of `templates/`.

| Write this in the target | Template |
| --- | --- |
| `README.md` | [README.md.tmpl](../../templates/README.md.tmpl) |
| `README.zh-CN.md` | [README.zh-CN.md.tmpl](../../templates/README.zh-CN.md.tmpl) |
| About text in the report | [ABOUT.txt](../../templates/ABOUT.txt) |
| `.github/workflows/ci.yml` | [ci.yml.tmpl](../../templates/.github/workflows/ci.yml.tmpl) |
| `docs/index.md` or `docs/index.html` (one, not both) | [index.md.tmpl](../../templates/docs/index.md.tmpl) or [index.html.tmpl](../../templates/docs/index.html.tmpl) |
| New MIT `LICENSE` | [LICENSE.MIT.txt](../../templates/LICENSE.MIT.txt) |
| `.github/PUBLISH_CHECKLIST.md` | [CHECKLIST.md](../../templates/CHECKLIST.md) |

Placeholder tokens look like `{{PROJECT_NAME}}`: uppercase letters, digits, underscores. Replace every one, including tokens that expand into several lines. A GitHub Actions expression looks like `${{ hashFiles('package.json') }}`. Leave those in workflow files. After editing, search the target:

```bash
rg -n '\{\{[A-Z0-9_]+\}\}' README.md README.zh-CN.md LICENSE docs .github/PUBLISH_CHECKLIST.md || true
```

Any hit in those paths is unfinished. Do not run that pattern-delete over `*.yml`.

Delete HTML comments that tell you how to fill a template. They are not part of the published file.

Keep commands, URLs, flags, and version numbers identical in the English and Chinese READMEs. Translate the prose, then run the Chinese polish in step 3.

## Steps

Edit the target repository. Do not edit this kit unless the kit is the target.

### 1. Intake

Read the tree before asking. Record the answers in the checklist note.

- Kind: library, application, CLI, documentation site, agent skill, template, or other.
- Audience: who runs it, in one sentence.
- Languages, from the files that are actually there: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.csproj`, or none.
- Name: GitHub repo name, or the folder name if there is no remote.
- Owner: the `origin` owner login. Copyright holder is that login unless the user gave a legal name. Do not guess a person's name from a username.
- Already present: README, `README.zh-CN.md`, LICENSE, `.gitignore`, `.github/workflows/`, `docs/`.

If `gh auth status` works:

```bash
gh repo view --json name,owner,description,repositoryTopics,homepageUrl,isPrivate,url
```

Ask the user only when a missing fact would otherwise be invented. The usual case is a copyright holder that is not the GitHub owner.

### 2. Code-content review

Search the tracked tree. Fix the working tree. Do not run `git filter-repo`, BFG, `git rebase`, or a force push. If a secret was already pushed, say to rotate it and that a history rewrite is a separate request.

Report path and line. Do not paste secret values into the checklist, the commit message, or the reply.

```bash
git ls-files -z | xargs -0 -r rg -n -i \
  -e 'BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY' \
  -e 'ghp_[A-Za-z0-9]{20,}' \
  -e 'github_pat_[A-Za-z0-9_]{20,}' \
  -e 'AKIA[0-9A-Z]{16}' \
  -e 'xox[baprs]-[A-Za-z0-9-]{10,}' \
  -e 'sk-(live|proj)-' \
  || true
git ls-files | rg '(^|/)(\.env|\.env\..*|[^/]+\.pem|id_rsa|id_ed25519|credentials\.json)$' || true
```

If `rg` is missing, use `git grep -I -n -E`. If `xargs` has no `-r`, skip the scan when `git ls-files` prints nothing. Ignore a hit that is only this skill documenting the pattern.

For a tracked secret: `git rm --cached -- <path>`, add the path to `.gitignore`, and tell the user to rotate the credential. A gitignore entry does not remove a file that is already tracked.

Personal data. Remove phone numbers, home addresses, private emails, machine paths, and employer names the user did not ask to publish. Keep a project email only when it is already that project's public contact. Do not add a phone number or an employer.

```bash
git grep -n -I -E '/Users/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\' || true
git grep -n -I -E '\+[0-9][0-9 ()-]{8,}' || true
```

Review email hits one by one. In the checklist write "removed an email from <path>" and do not repeat the address.

Dead demos. Replace a stock framework README (Create React App, Vite, Next.js, or a "TODO" description) when it does not describe this project. Remove demos that point at an old private host, embed personal screenshots, or ship example passwords. Keep a demo the README still presents as a feature; fix it, or mark the item `fail` with the reason.

License headers. MIT does not need a header on every source file. If `SPDX-License-Identifier` is already in the tree, it must match the LICENSE you will ship. Do not mass-edit headers on this pass.

```bash
git grep -n -I SPDX-License-Identifier || true
```

`.gitignore`. Create one if it is missing. If it exists, append rules; do not delete project rules. Always ignore `.env`, `.env.*` with an exception for `.env.example`, `*.pem`, and `*.key`. Also ignore dependency and build directories the stack uses (`node_modules/`, `.venv/`, `__pycache__/`, `dist/`, `target/`) and `.DS_Store`. Do not commit an `.env.example` that contains real values.

Large files. GitHub warns near 50 MB and rejects a file at 100 MB.

```bash
git ls-files -z | while IFS= read -r -d '' f; do
  bytes=$(wc -c < "$f" | tr -d ' ')
  if [ "$bytes" -ge 1048576 ]; then echo "$bytes $f"; fi
done
```

List every tracked file at least 1 MB. Do not add a new file at least 5 MB unless the user said that binary is a release artifact. Remove build output, unused datasets, and archives. Leave images the README references. Do not delete a release binary silently.

### 3. README

Write `README.md` from [README.md.tmpl](../../templates/README.md.tmpl) and `README.zh-CN.md` from [README.zh-CN.md.tmpl](../../templates/README.zh-CN.md.tmpl) in the same edit. Then polish the Chinese.

Order:

1. H1 is the product name people search for, not "Welcome" or "Introduction".
2. One-liner: the first paragraph. What it is and who it is for.
3. Purpose, Quick start, Features, Install, Usage, Configuration, License, Contact.

English headings, exactly: `Purpose`, `Quick start`, `Features`, `Install`, `Usage`, `Configuration`, `License`, `Contact`.

Chinese headings, exactly: `用途`, `快速开始`, `功能`, `安装`, `用法`, `配置`, `许可证`, `联系`.

Do not add an FAQ heading (`FAQ` or `常见问题`). Do not link to one.

| Token | Write |
| --- | --- |
| `{{ONE_LINER}}` / `{{ONE_LINER_ZH}}` | One sentence. Product noun, what it does, who it is for. |
| `{{WHY}}` / `{{WHY_ZH}}` | Two to four sentences. The problem, then what this project does. |
| `{{QUICKSTART}}` / `{{QUICKSTART_ZH}}` | Shortest path to a result. Same commands in both files. |
| `{{FEATURES}}` / `{{FEATURES_ZH}}` | Bullets. Same facts in the same order. |
| `{{INSTALL}}` / `{{INSTALL_ZH}}` | Real install commands for this stack. |
| `{{USAGE}}` / `{{USAGE_ZH}}` | One working example. |
| `{{CONFIGURATION}}` / `{{CONFIGURATION_ZH}}` | Env vars or flags. If there are none, say so. Keep the heading. |
| `{{LICENSE_LINE}}` / `{{LICENSE_LINE_ZH}}` | License name, SPDX id, copyright, link to the file. |
| `{{CONTACT}}` / `{{CONTACT_ZH}}` | Contacts the project already published, or contacts in the user message. If none, link the GitHub owner only. |

If the user asked for English only, skip the Chinese file and mark the doc-lint checklist row `skip`. The default is both files.

After both drafts exist, polish `README.zh-CN.md` and any other Chinese product or technical page this launch writes. If a `doc-lint` skill is available, load it for this pass. Do not copy that skill into this repository.

- Cut redundancy, filler, and translationese. Keep the meaning.
- Keep technical English terms, commands, URLs, flags, and version numbers identical to `README.md`.
- Do not add sections to make the Chinese file longer.

### 4. About and topics

Write one description of at most 160 characters. Count it:

```bash
python3 -c 'print(len("PASTE"))'
```

Lead with the product noun. No hashtags, no "Welcome to", no emoji. This skill uses 160 even when GitHub's field allows more, so the sidebar and a search snippet stay one sentence.

Pick 5–10 topics. Lowercase, digits, hyphens, no spaces. Use nouns a stranger searches: language, domain, and `open-source` when that is true. Keep topics the repo already has. GitHub allows 20; stop there. Do not put a person's name in a topic.

If `gh auth status` succeeds, set them:

```bash
gh repo edit --description "DESCRIPTION" --add-topic topic-one --add-topic topic-two
```

If `gh` is missing or not authenticated, put the description and the topics in the report. Do not fail the run.

Do not pass `--homepage` until the Pages URL loads (step 7). Do not change visibility unless the user explicitly said to make the repository public and the secret scan passed. Otherwise leave visibility as it is and put `gh repo edit --visibility public` in the report, not in the shell.

### 5. LICENSE

If `LICENSE` or `LICENSE.md` already exists, keep it. Do not swap a license unless the user asked.

If there is no license:

| SPDX | When |
| --- | --- |
| MIT | Default. Permissive, no patent grant. |
| Apache-2.0 | The user wants an explicit patent grant. Common for libraries companies ship. Mention NOTICE if they already keep one. |
| AGPL-3.0 | The user wants network copyleft: a network service that runs modified code must offer that source. |

If they are unsure between Apache-2.0 and AGPL-3.0, ask. Do not pick AGPL silently. Do not invent a proprietary license.

For a new MIT file, copy [LICENSE.MIT.txt](../../templates/LICENSE.MIT.txt) and replace `{{YEAR}}` and `{{COPYRIGHT_HOLDER}}` only. Do not edit any other line. For Apache-2.0 or AGPL-3.0, copy the text verbatim from `https://choosealicense.com/licenses/apache-2.0/` or `https://choosealicense.com/licenses/agpl-3.0/`. Do not paraphrase a license. The SPDX id in both READMEs must match the file you wrote.

### 6. CI

If `.github/workflows/` already runs tests, leave it and mark the checklist `pass`.

If it does not, add `.github/workflows/ci.yml` from [ci.yml.tmpl](../../templates/.github/workflows/ci.yml.tmpl), then:

- Delete the Node, Python, Go, and Rust steps that do not match intake.
- Point the remaining step at the project's real test or lint command.
- If there is no test suite, keep the required-files step (`README.md` and `LICENSE`) and say so in the checklist.
- Leave `permissions: contents: read`. Do not grant write permissions for a lint job.
- Do not add a Pages deploy workflow for a hand-written `docs/` tree. Deploy from a branch does not need one.

### 7. GitHub Pages

Record the decision in the checklist.

Use `docs/` on the default branch for a landing page or a few hand-written pages. Use a GitHub Actions build only when a generator is already in the repo (VitePress, Docusaurus, MkDocs, Sphinx, or a static export). Do not add that workflow in this pass unless the generator is already there.

Write one entry point:

- `docs/index.html` from [index.html.tmpl](../../templates/docs/index.html.tmpl) when the page should carry its own title, meta description, canonical URL, and Open Graph tags. Add an empty `docs/.nojekyll` so Jekyll does not rewrite the HTML.
- `docs/index.md` from [index.md.tmpl](../../templates/docs/index.md.tmpl) when the repo already uses Jekyll or the default Pages theme is enough.

Do not write both. `index.html` wins and the markdown file would be ignored.

Do not enable Pages. Do not call the Pages API. Tell the user to do this in the browser:

1. Repository → **Settings** → **Pages**.
2. **Build and deployment** → **Source**: Deploy from a branch.
3. Branch: the default branch. Folder: **`/docs`**.
4. Save. The settings page shows the site URL.
5. A project site is `https://<owner>.github.io/<repo>/`. A repository named `<owner>.github.io` is `https://<owner>.github.io/`.
6. After that URL loads, set the About homepage: `gh repo edit --homepage URL`. Until it loads, leave the homepage unset and record the URL in the report.

If the user said there should be no site, write nothing under `docs/` and mark the row `skip`.

### 8. GEO and SEO

Write so a search index and a language model quote the same facts. SEO is the stable headings from step 3, plus the title and Pages meta. Do not add an FAQ heading.

- The H1 is the product name. The first paragraph says what it is, who it is for, and the license. Scrapers cut the page short.
- Use that same product noun in Features. Do not stuff keywords.
- On `docs/index.html` set `<title>`, `meta name="description"` (160 characters or fewer), `link rel="canonical"`, `og:title`, `og:description`, and `og:url`. Use the About sentence for the meta description when it already states the product.
- Add JSON-LD `@type` `SoftwareSourceCode` only with facts you can point at: name, description, `codeRepository`, license URL. Publisher is an Organization. No star ratings, no invented author name.

### 9. Checklist

Fill [CHECKLIST.md](../../templates/CHECKLIST.md) and write it to `.github/PUBLISH_CHECKLIST.md`. Status is `pass`, `fail`, or `skip`. Leave no `TODO`. Notes are one line and contain no secret values.

Put the same table in the reply, under a launch report:

- About description and the character count
- Topics
- Homepage URL, and whether you set it
- Visibility: unchanged, or the command you ran
- Push: not run, or the branch you pushed

`fail` on secrets or private data means do not push. `fail` or `skip` on Pages does not block a push. The checklist does not install a hook. It does not reject `git push`.

Push the packaging commits only when the user asked to push, including a clear "ship" or "上架" after the files are ready, and the secret scan is `pass`. A first look that only asked for the packaging pass stops at the report.

## Done

Done means the files are edited, no `{{TOKEN}}` remains in the published paths, and the checklist is in `.github/PUBLISH_CHECKLIST.md` and in the reply. Do not say Pages is live. Do not say topics were set if `gh repo edit` did not succeed.
