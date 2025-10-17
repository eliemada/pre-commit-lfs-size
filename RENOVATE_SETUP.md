# Renovate Setup Guide

This repository includes a Renovate configuration to automatically keep dependencies up to date.

## What is Renovate?

Renovate is a bot that automatically creates Pull Requests to update your dependencies. It:
- Monitors your dependencies for updates
- Creates PRs with updates
- Groups related updates together
- Can auto-merge minor updates
- Requires approval for major version changes

## Setup Instructions

### Option 1: GitHub App (Recommended)

1. **Install the Renovate GitHub App**:
   - Go to https://github.com/apps/renovate
   - Click "Install" or "Configure"
   - Select your account (`eliemada`)
   - Choose "Only select repositories"
   - Select `pre-commit-lfs-size`
   - Click "Install"

2. **Renovate will automatically**:
   - Detect the `renovate.json` configuration
   - Create an initial "Configure Renovate" PR
   - Start monitoring your dependencies
   - Create a Dependency Dashboard issue

3. **Review and merge the onboarding PR**:
   - Renovate will create a PR titled "Configure Renovate"
   - Review the changes
   - Merge when ready

### Option 2: Self-Hosted Renovate

If you prefer to run Renovate yourself:

1. **Create a GitHub Personal Access Token**:
   - Go to https://github.com/settings/tokens
   - Create token with `repo` and `workflow` scopes
   - Save the token securely

2. **Add as GitHub Secret**:
   - Go to repository Settings → Secrets → Actions
   - Add secret named `RENOVATE_TOKEN` with your token

3. **Create GitHub Actions workflow**:
   - The workflow file would be: `.github/workflows/renovate.yml`
   - (Not included by default - let me know if you want this)

## Configuration Overview

Your `renovate.json` includes:

### Grouped Updates

1. **🔍 Linting & testing tools** (`ruff`, `pytest`, `pytest-cov`)
   - Auto-merges minor/patch updates
   - Keeps your dev tools current

2. **📦 Build system** (`setuptools`, `wheel`)
   - Auto-merges minor/patch updates
   - Ensures build tools stay updated

3. **🚨 Major version updates**
   - Requires manual approval via Dependency Dashboard
   - Prevents breaking changes without review

### Features Enabled

- **Dependency Dashboard**: Creates an issue listing all pending updates
- **Lock file maintenance**: Updates `uv.lock` weekly (Mondays at 3am)
- **Automatic labels**: Tags PRs with `dependencies` label
- **Commit message prefix**: Uses `:arrow_up:` emoji for update commits
- **PR limits**: Maximum 3 concurrent PRs to avoid overwhelming you

## Dependency Dashboard

After Renovate is enabled, it will create an issue titled "Dependency Dashboard" that shows:
- Pending updates
- Ignored dependencies
- Rate-limited PRs
- PRs awaiting approval

You can control updates by checking boxes in this issue.

## How Updates Work

### Automatic Updates (Auto-merge)
Minor and patch updates to dev dependencies are automatically merged:
```
ruff: 0.14.1 → 0.14.2  ✅ Auto-merged
pytest: 8.4.2 → 8.4.3  ✅ Auto-merged
```

### Manual Review Required
Major updates need approval:
```
ruff: 0.14.1 → 0.15.0  ⏸️ Awaits approval in Dependency Dashboard
pytest: 8.4.2 → 9.0.0  ⏸️ Awaits approval in Dependency Dashboard
```

## Customizing the Configuration

Edit `renovate.json` to customize behavior:

### Change update schedule
```json
"schedule": ["after 9pm on sunday"]
```

### Disable auto-merge
```json
"automerge": false
```

### Add more package groups
```json
{
  "groupName": "📝 Documentation tools",
  "matchPackagePatterns": ["^mkdocs", "^sphinx"]
}
```

### Change timezone
```json
"timezone": "Europe/London"
```

## Monitoring Renovate

### Check Renovate Status
- View the Dependency Dashboard issue
- Check recent PRs labeled `dependencies`
- Look at repository Insights → Dependency graph

### Troubleshooting

**Renovate not creating PRs?**
1. Check if it's installed: https://github.com/apps/renovate
2. Look at Dependency Dashboard for rate limits
3. Check if PRs are in draft mode

**Too many PRs?**
- Adjust `prConcurrentLimit` in `renovate.json`
- Use `schedule` to limit when PRs are created
- Increase grouping of related dependencies

**Need to ignore a dependency?**
Add to `renovate.json`:
```json
"ignoreDeps": ["package-name"]
```

## Benefits for This Project

For `pre-commit-lfs-size`, Renovate will:
1. Keep `ruff` updated → Latest linting rules
2. Keep `pytest` updated → New testing features
3. Update GitHub Actions → Latest action versions
4. Maintain `uv.lock` → Consistent builds
5. Alert you to security updates → Stay secure

## Useful Links

- [Renovate Documentation](https://docs.renovatebot.com/)
- [Configuration Options](https://docs.renovatebot.com/configuration-options/)
- [GitHub App](https://github.com/apps/renovate)
- [Renovate Playground](https://app.renovatebot.com/dashboard) (test configs)

## Next Steps After Setup

1. ✅ Merge the onboarding PR from Renovate
2. ✅ Review the Dependency Dashboard issue
3. ✅ Let Renovate create its first update PRs
4. ✅ Review and merge/close PRs as appropriate
5. ✅ Adjust configuration based on your preferences

---

**Note**: Renovate respects your branch protection rules and CI checks. PRs will only auto-merge if:
- CI passes (GitHub Actions)
- Branch is up to date
- Auto-merge is enabled for that package group
