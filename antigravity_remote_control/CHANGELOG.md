# Changelog

## 1.2.8

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.8.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Improved context compaction to spread its user-request budget across all captured prompts, so a long initial instruction is no longer truncated to a small fixed slice when the other prompts in the conversation are short
- Improved context compaction to size summary and truncation budgets from the model's full context window instead of the compaction trigger threshold, so compacted summaries and background-task lists are no longer prematurely cut short
- Fixed PDF and audio tool outputs and attachments failing with `unsupported mime type` errors on custom models configured in `settings.json`; custom models now accept PDFs by default and honor the `modelFeatures` media flags for images, video, PDF, and audio
- Fixed pressing `Ctrl+G` to edit the prompt in a full-screen terminal editor such as `vim` hanging with `Vim: Warning: Output is not to a terminal`; external editors now run against a real terminal stdout
- Fixed voice dictation sessions longer than 4 minutes failing with a deadline error and erasing the drafted transcription; recordings now automatically stop and finalize at 3 minutes 30 seconds
- Fixed the startup banner displaying a Google Cloud Project ID for consumer (non-enterprise) sign-ins
- Fixed a stack-overflow crash when loading or compacting conversations containing background-task, subagent-management, messaging, or scheduling steps
- Fixed forked conversations inheriting step output data from steps after the fork point, which could collide with new steps produced in the fork
- Fixed a background poller and timer leaking for every conversation session, slowly accumulating memory over long-running sessions
- Fixed canceled conversation and workspace creation requests continuing to provision resources in the background; aborted requests now stop immediately
- Fixed quitting the CLI taking around 5 extra seconds before the process exited; shutdown now cancels open streaming connections immediately instead of waiting for a forced timeout

## 1.2.7

### 📦 Add-on & Container Wrapper
- Synced add-on version directly with Google Antigravity CLI release stream.
- Added automated GitHub Action (`check-upstream-agy.yml`) to monitor and notify Home Assistant of new upstream releases.
- Multi-architecture base for `amd64` and `aarch64` (`ghcr.io/home-assistant/{arch}-base-debian:bookworm`).
- Bundled official statically linked `ha` CLI (`v5.5.0`) with Supervisor manager privileges.
- Streamlined configuration options for single instance name setting.
- Fixed relative markdown documentation link in add-on details page.

### 🤖 Google Antigravity CLI (`agy`)
- **Interactive Prompts**: Improved `ask_question` with Left/Right navigation between questions, inline previews of write-in answers, check marks on answered options, and single-step submission.
- **Enterprise Diagnostics**: Added active Google Cloud Project ID beneath the signed-in account and plan tier in the CLI startup banner.
- **API Retries**: Capped per-attempt API retry backoff at 30 seconds instead of waiting up to 4 minutes between attempts.
- **Customization Token Budgeting**: Allocated user and workspace rules a dedicated 20,000-token budget to prevent large rule sets from evicting skills, workflows, subagents, or MCP tools.
- **Tool Baseline**: Cleaned up default agent baseline by retiring legacy `find_by_name`, `grep_search`, and `list_dir` while keeping them available to custom agents.
- **Terminal Rendering**: Upgraded Bubble Tea to v2.0.9 for improved Kitty keyboard protocol stack handling on exit and screen clear.
- **Headless Execution**: Improved `-p` / `--prompt` background-task waiting notices, logged background tool progress, and reduced memory usage during large outputs.

---

## 1.0.1

### 📦 Add-on & Container Wrapper
- Added `build.yaml` mapping for multi-architecture builds (`amd64`, `aarch64`).
- Integrated `ha` CLI with internal Supervisor token auth.
- Implemented startup self-update routine.
- Safe JSON merging of `cliRemoteControlHostname` with `jq`.

### 🤖 Google Antigravity CLI (`agy`)
- Bundled base version for initial supervised add-on release.

---

## 1.0.0

### 📦 Add-on & Container Wrapper
- Initial release of the dedicated Antigravity Remote Control Home Assistant add-on.
- Native Debian Bookworm base with glibc runtime.
- S6-overlay v3 process supervision (`agy remote-control serve`).
- Home Assistant UI lifecycle controls (Start, Stop, Restart, Watchdog, Log viewer).
