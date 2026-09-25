# Changelog

## 1.2.11

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.11.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Improved reasoning effort level for models with different support, selectable with `--effort` or from the effort gauge in `/effort` and `/model`.
- Changed plugins placed directly in `~/.gemini/config/plugins` so that a plugin whose MCP server needs configuration variables now starts disabled until you enable it, matching plugins installed through `/plugin`.
- Fixed Mermaid diagrams and LaTeX rendering as rows of garbled placeholder characters in WezTerm and the VS Code integrated terminal; these terminals are no longer assumed to support Kitty graphics and now show the ASCII fallback
- Fixed copying text from the artifact viewer when `Copy on Select` is turned off in `/config`: the viewer no longer captures the mouse, so your terminal's own selection and copy shortcut work, and `Ctrl+C` goes back to interrupting or exiting
- Fixed project custom agents in .agents/agents/ not being found or selectable in workspaces created in the Desktop App, in already-trusted workspaces, under execution with --agent, in headless (-p / --prompt) runs, and in the /agents panel.

## 1.2.10

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.10.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added `medium` verbosity mode to `/config`, between `high` and `low`, which groups related tool calls and thoughts into concise summaries (such as `Explored N files`) while keeping commands and responses visible; the Verbosity setting and each option now describe what they show
- Improved Mermaid diagram and LaTeX rendering in the artifact viewer on Kitty-compatible terminals: artifacts are pre-rendered in the background so diagrams appear as soon as the viewer opens, images are uploaded once at a smaller size, and zooming with `Ctrl+=` / `Ctrl+-` no longer flickers between the old and new sizes
- Improved the artifact viewer footer by combining the separate top and bottom hints into one `g/G top/bottom` entry, labeling `m` with the view it switches to (diagram, LaTeX, ASCII, or raw), and fixing hints that contain arrow symbols wrapping onto a new line too early
- Improved terminal sandbox behavior so the agent asks to bypass the sandbox less often: it now knows sandboxed commands can read and write its own artifact and scratch directories, and it tries the sandbox first even after an earlier command needed a bypass
- Changed the step title of commands that exit with a non-zero code from `Errored` to `Failed`
- Changed how directory entries in `skills.json`, `rules.json`, `agents.json`, and `plugins.json` are scanned: an entry now loads only the items directly inside the directory, the same as a `.agents/skills/` folder, instead of recursively loading everything beneath it; to load a nested item, name it in `include_only`, for example `{"path": "shared_skills", "include_only": ["category/my-skill"]}`
- Fixed pressing `Esc` while the suggestions dropdown is open interrupting the agent's turn; it now closes the dropdown, and a second `Esc` interrupts
- Fixed Mermaid diagrams and LaTeX leaving a blank gap inside `tmux` or GNU `screen` when the outer terminal supports Kitty graphics; the CLI now falls back to ASCII diagrams unless images actually reach the terminal, and `CLI_GRAPHICS=kitty` still forces image mode for setups with image passthrough configured
- Fixed headless (`-p` / `--prompt`) runs that streamed part of a response and then ended on a model or agent error exiting with code 0; they now exit with code `3` and print the `AGY_ERROR` line, and JSON error output includes the partial response, while multi-turn `stream-json` sessions still warn and continue
- Fixed machines set up with the old Remote Control installer script crash-looping after an upgrade; when the CLI is launched by that deprecated background service it now unregisters the service and points to `remote-control start` instead of restarting repeatedly
- Fixed files that subagents write inside their own Git worktree being treated as artifacts, which demanded artifact metadata and left `.metadata.json` files in the worktree; subagent worktrees now live under a `worktrees/` directory in the app data directory

## 1.2.9

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.9.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added `@<subagent> <message>` prompt syntax to send a message directly to a subagent conversation, with autocomplete listing running and completed subagents
- Added Vim numeric count multipliers so counts apply to operators, motions, and actions in Normal and Visual modes, including `3dw`, `2d3w`, `3dd`, `3x`, `3rX`, `3p`, `3u`, `[count]G`/`gg`/`$`, and counted text objects such as `2di(`
- Improved `GEMINI_API_KEY` sessions to reduce behavior discrepancies with the non-API-key sign-in path
- Improved the artifact viewer to show a Left/Right pan hint in the footer when a wide diagram overflows the window
- Improved `/rewind` to show a relative timestamp for each step and to focus the most recent step when the panel opens
- Improved command allow-listing suggestions to recognize `jj config` and `jj op` subcommands when offering to always allow a command
- Fixed headless (`-p` / `--prompt`) runs leaving daemon background processes running after exit, which could hang scripts reading the CLI's output until end-of-file; daemon processes now terminate when the run ends
- Fixed headless (`-p` / `--prompt`) runs cancelling still-running background tasks about 5 seconds after the agent went idle; runs now wait for background tasks until the `--print-timeout` deadline, up to a 30-minute cap
- Fixed a conversation-history database corruption risk where checking the database file for write access could silently drop file locks held by concurrent CLI processes on the same file
- Fixed context compaction failing when the tool configuration used for compaction checkpoints was rejected in certain scenarios
- Fixed a backend crash when a streamed model response chunk arrived without its response envelope, which terminated the session with connection errors
- Fixed markdown table column alignment when a table cell contains file links that wrap across lines
- Fixed markdown file links to code symbols dropping their display text and rendering the raw path instead
- Fixed incomplete enterprise sign-ins (for example closing the browser window before finishing license or project selection) leaving behind a stuck partial credential; such credentials are now cleared automatically so sign-in can be retried cleanly
- Fixed the browser companion page title to read `Antigravity CLI` instead of `Antigravity Cli`

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
