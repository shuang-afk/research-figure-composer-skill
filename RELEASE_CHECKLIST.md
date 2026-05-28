# Release Checklist

Use this checklist before publishing or tagging a new version.

## Skill Integrity

- [ ] `skills/research-figure-composer/SKILL.md` has valid YAML frontmatter with only `name` and `description`.
- [ ] `agents/openai.yaml` matches the current skill behavior.
- [ ] No generated `__pycache__`, local test outputs, private data, or temporary files are included.
- [ ] Example SVGs are intentionally bundled under `assets/examples/`.

## Validation

Run from the repository root:

```powershell
$env:PYTHONUTF8 = '1'
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skills\research-figure-composer"
python ".\skills\research-figure-composer\scripts\validate_svg.py" ".\skills\research-figure-composer\assets\examples\palette-data.svg"
python ".\skills\research-figure-composer\scripts\validate_svg.py" ".\skills\research-figure-composer\assets\examples\palette-diagram.svg"
```

## GitHub Publish

```powershell
git status
git add README.md LICENSE NOTICE.md CHANGELOG.md RELEASE_CHECKLIST.md .gitignore skills
git commit -m "Publish research figure composer skill"
git branch -M main
git remote add origin https://github.com/shuang-afk/research-figure-composer-skill.git
git push -u origin main
```

## Install Smoke Test

On another Codex environment or after moving the old local skill out of the way:

```powershell
$env:PYTHONUTF8 = '1'
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo shuang-afk/research-figure-composer-skill --path skills/research-figure-composer
```

Restart Codex and ask:

```text
用 $research-figure-composer 生成一个折线图
```
