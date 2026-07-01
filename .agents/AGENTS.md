# Project Customizations

## GitHub CLI & Git Push Troubleshooting
- If `git push` fails with a `Permission denied (publickey)` or authentication prompt:
  1. Ensure the Git remote URL uses HTTPS instead of SSH:
     ```bash
     git remote set-url origin https://github.com/<owner>/<repo>.git
     ```
  2. Configure Git to use the GitHub CLI (`gh`) as its secure credential helper:
     ```bash
     gh auth setup-git
     ```
  3. Run the push command again.

---

## User Command Preferences
- When the user explicitly requests to use terminal command-line tools (e.g., `gh cli`) instead of integrated tools or MCPs, run the corresponding terminal commands via `run_command` and avoid background API/MCP integrations.

---

## Branching & Merging Policy
- Always create and work inside a dedicated feature branch (e.g., `feat/...` or `fix/...`) when implementing changes in this repository.
- Do NOT merge your feature branches directly into the `main` branch. All merges must be initiated via pull requests on GitHub for peer review and tech lead approval.
