# Changelog

## 1.3.1

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.3.1.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Improved navigation in the `/diff` file view: `←`/`→` now open the next or previous file at its first change with the hunk header and leading context in view, each file remembers its cursor and scroll position when you switch files or go back to the file list, `n`/`N` continue into the next or previous file's changes instead of stopping at the last change in the current file, and the key-hint footer drops the generic scroll and page hints and wraps onto extra lines instead of being cut off on narrow terminals.
- Improved the `/diff` file view header to show where you are: it now ends with a right-aligned `change A/B · file X/Y` position, counting the block of added or removed lines under the cursor and the file's place in the file list (`file X/Y` is left out when only one file changed, and the position is hidden on narrow terminals).
- Fixed `/rewind` in very long conversations listing older messages as `(empty message)` and failing with an error when you picked one: messages that were cleared to save space now show their original text, dimmed and labeled `cleared to save space, can't rewind here`, and can no longer be selected.
- Fixed installing, reinstalling, and uninstalling plugins with `/plugin` on Windows failing while one of the plugin's MCP servers was running: the CLI now stops the plugin's MCP servers before replacing or deleting its folder and restarts them afterwards, and if another Antigravity process such as another `agy` session, the Antigravity Hub, or the `remote-control` daemon still holds the plugin open, it tells you to close it and retry. Plugin manifests, `mcp_config.json`, and `hooks.json` files saved with a UTF-8 byte-order mark now load, and installing from a marketplace no longer overwrites an existing plugin folder that came from a different source.
- Fixed markdown custom agents ignoring `skills:`, `plugins:`, `rules:`, `agents:`, and `hooks:` entries written as paths relative to the agent's own file when the agent ran as a subagent or as the main agent; such entries now resolve against the agent's directory, so an agent that lists `agents: [child.md]` can invoke `child`.
- Fixed subagents that stopped on an error, such as running out of quota or model capacity, being shown as `Done` in `/agents` and the list of running agents; they now show `Error:` with the reason, and the error clears once the subagent makes further progress.
- Fixed `/tasks`, the active task list, and the status line's task count showing only background shell commands; timers and recurring jobs the agent schedules, and other tools running in the background, now appear there too and are shown as `completed` or `failed` without a made-up exit code.
- Fixed messages sent with `Queued Messages` set to `Send Immediately` in `/config` being silently queued until the end of the turn whenever the agent had already written or updated an artifact, such as a task list or plan, during that turn; they now reach the agent right away.
- Fixed terminal notifications not firing when the agent stops to ask you a question; with `Notifications` turned on in `/config`, the CLI now alerts you for pending questions just as it does for tool permission prompts.
- Fixed restarting an MCP server from `/mcp` sometimes leaving it stopped, with an error such as `Failed to stop existing instances for reload: ... signal: killed`, when the old server process took too long to exit; the server now always starts again.
- Fixed the sign-in error for accounts that need to verify their identity or appeal a Terms of Service block sometimes showing only `Verify your account to continue.` with no link; the verification or appeal link now always appears, and the CLI no longer suggests logging out and back in when that would not help.
- Fixed `GEMINI_API_KEY` sessions failing a turn as if you had cancelled it when the connection to the Gemini API was dropped internally; the CLI now retries the request instead.

## 1.3.0

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.3.0.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Changed the default `Verbosity` setting from `high` to `medium`, so the conversation view now groups related tool calls and thoughts into concise summaries while keeping commands and responses visible. This applies to everyone who never picked a verbosity, including anyone who selected `high` while it was still the default; set `Verbosity` back to `high` in `/config` to see every tool call, command, and thought in full again.
- Changed `j` and `k` in the `/diff` file view to move the line cursor like the up and down arrow keys, matching the file list and Vim, instead of jumping to the next or previous file; use the left and right arrow keys to switch files.
- Fixed trackpad and mouse-wheel scrolling in the conversation view jumping back and forth, most noticeably over SSH or inside tmux, by ignoring the sideways part of diagonal swipes and limiting how far a single fast scroll step can move; `Page Up` and `Page Down` still move a full page.
- Fixed files and folders whose paths contain spaces, `#`, `%`, or other special characters, or that sit on a Windows drive, being mishandled across the CLI: `@` file mentions, `/codesearch` results, and file links in agent responses now open the right file, and workspace trust and project-scoped custom agents now recognize projects created in the Antigravity desktop app in such folders.

## 1.2.17

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.17.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added announcement cards above the prompt for model launches, deprecations, and other service notices. Cards appear one at a time, newest first; press `Esc` on an empty prompt to dismiss the current card permanently and show the next one, and sending a message hides the card for the rest of the session.
- Improved the Windows command sandbox so sandboxed commands no longer need administrator rights, and common tools such as Python, Git, and `npm` work inside the sandbox out of the box.
- Fixed markdown table columns drifting out of alignment when a cell contains emoji such as ⚠️ or 👍🏽 or scripts with combining characters such as Hindi, which affected every session over SSH or inside tmux.
- Fixed `.tiff` images being reported with the wrong file type and silently converted to PNG when the agent viewed them.

## 1.2.16

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.16.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added `←`/`→` shortcuts to `/config`: on a highlighted setting they switch to the previous or next value and save it right away, without opening the dropdown, and the footer shows a `←/→ Change` hint
- Improved responsiveness in long conversations in no flicker (altscreen) mode: resizing the terminal no longer freezes or lags the CLI, the full-screen view redraws the messages on screen first instead of showing text wrapped for the old width until the whole conversation has re-rendered, and interrupting the agent with `Esc` or resuming a conversation no longer re-renders every step already on screen.
- Improved mouse text selection in the `altscreen` view and in the artifact viewer: dragging past the top or bottom now auto-scrolls, the selection stays on its text while the agent streams or you scroll with the wheel, and copying includes lines that scrolled off screen, without line numbers or comment previews from the artifact viewer
- Improved the always-allow suggestion when approving `go` commands: approving a command such as `go vet` or `go build` now offers to allow that subcommand with any arguments, while `go run`, `go test`, `go generate`, `go install`, and `go tool` still require the exact command
- Improved the `Send Immediately` option for Queued Messages in `/config`: a message you send while earlier messages are still queued now goes to the agent together with them, in order, instead of joining the queue, and a message that fails to send mid-turn goes back to the queue instead of being lost
- Changed how the agent generates images: it now hands image requests to a built-in `image-generator` subagent, which writes the prompt, checks each result with up to three attempts, and saves the images to the conversation's artifacts, so image generation appears as a subagent run in the conversation
- Fixed the agent stalling when a background command it was waiting on crashed or was killed by the system, for example when it ran out of memory; the agent now sees the command finish with its exit code, such as `137` or `134`, and keeps going
- Fixed headless `-p` runs sometimes exiting before the agent could respond to a background command that finished after its first turn
- Fixed `k` in Vim Normal mode recalling the last history entry instead of your queued messages when pressed on the top line, which could send a queued message twice; `k` now pulls queued messages back into the editor like the `Up` arrow does
- Fixed `skills.json`, `rules.json`, and other customization manifests in a parent `.agents/` directory being ignored when a session started in a subdirectory; manifests now load from every `.agents/` directory between the working directory and the project root
- Fixed the `/` menu listing built-in skills that the current agent does not enable, which inserted instructions for tools the agent could not use when selected
- Fixed settings failing to load when `~/.gemini/config/config.json` starts with a UTF-8 byte order mark, as files saved by Notepad or PowerShell `Set-Content` on Windows do
- Fixed slash-command output and alerts where a line exactly as wide as the terminal had its last word pushed to the start of the next line without indentation

## 1.2.14

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.14.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added the `Queued Messages` option to `/config`: keep the default `Queue` to hold follow-up messages until the current turn ends, or choose `Send Immediately` to interrupt the agent with them; it can also be set with `"queuedMessages": "send-immediately"` in `settings.json`, which was previously ignored
- Improved `remote-control start` on Linux machines without a systemd user service manager, such as most containers: instead of failing, it now starts the daemon as a background process and warns that it will not restart after a crash or start at boot; `remote-control status` shows its PID and `remote-control stop` shuts it down
- Improved loading long conversations: resuming a conversation with thousands of steps is noticeably faster because the CLI no longer scans every step up front
- Improved automatically generated conversation titles to take images and files attached to your first message into account, so screenshot- or file-driven requests get specific titles and messages with only attachments get a title too
- Improved the sign-in error shown to accounts blocked for a Terms of Service violation, which now includes a link to submit an appeal
- Changed `--json-schema` to reject plain text, bare type names such as `string`, and missing schema files instead of silently treating them as a string schema; these inputs, and any schema whose root is not `"type": "object"`, now fail at startup with an error and exit code `1`
- Fixed the prompt cursor drifting away from the end of the text after emoji such as ⚠️ or 👩‍💻, or scripts with combining marks such as Devanagari and Thai, especially inside `tmux`, and fixed prompt wrapping splitting such characters across two lines
- Fixed the agent hanging when it tried to view a pipe, socket, or device file, and a conversation getting stuck with `INVALID_ARGUMENT` errors after the agent viewed a truncated MP4, MOV, or M4A recording; both are now rejected up front with a clear message
- Fixed resuming a conversation whose history had a missing step, for example after a crash or an interrupted write, hiding the most recent steps and letting new messages overwrite them

## 1.2.13

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.13.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Improved rate-limit handling when the model API returns a retry delay: the CLI now waits the delay the server asks for instead of a fixed 5 seconds, and stops right away instead of retrying when the delay is longer than 30 seconds or the quota is a daily or billing cap
- Improved rendering efficiency, cutting CPU use and memory churn while the conversation view redraws, such as during fast scrolling or while the agent is working
- Improved the artifact viewer's `m` hint to name the content and the mode it switches to, such as `diagram ASCII`, `diagram source`, or `math image`, instead of `toggle ASCII` or `toggle raw`
- Fixed the workspace trust dialog, the `/help` panel, and the sign-in and MCP authentication screens clipping text on narrow terminals of around 40 columns; long lines and navigation hints now wrap, and the `/help` tab bar compacts to fit

## 1.2.12

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.2.12.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Improved scrolling in the full-screen view: bursts of mouse-wheel or trackpad events are now coalesced before redrawing, which cuts CPU use and reduces scroll lag in long conversations and the artifact viewer
- Improved `GEMINI_API_KEY` sessions to stop immediately when the Gemini API reports an exhausted daily quota, a project or billing-account spend cap, or depleted prepaid credits, instead of spending several minutes on retries that cannot succeed; short-lived per-minute rate limits are still retried
- Fixed resuming a long conversation in `medium` or `low` verbosity taking many seconds and lagging while history replayed: earlier tool groups now appear already finished instead of each re-animating, and keys pressed during the replay no longer refresh a half-loaded transcript
- Fixed the terminal or tab title changing to a string like `Ga=q,f=32,...` every time the CLI starts inside GNU `screen`, `tmux` (including iTerm2 `tmux -CC` tabs), or Zellij; the CLI no longer sends its image-support probe through a multiplexer, and `CLI_GRAPHICS=kitty` still forces image mode
- Fixed Vim mode ignoring non-ASCII characters such as `é` or `中` after `r`, `f`, `F`, `t` and `T`, `fv` and `fV` in Visual mode leaving Visual mode instead of extending the selection, and `D`, `C`, or Visual `~`/`u`/`U` recording an empty undo step and clearing redo history when they changed nothing

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
