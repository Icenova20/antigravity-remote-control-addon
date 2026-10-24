# Changelog

## 1.4.7

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.7.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added `lastUserInput` to the JSON that hook commands receive on stdin, so a hook can inspect the latest message you sent, for example to screen prompts before the agent acts on them.
- Added a temporary opt-in Halloween theme: turn on `Seasonal Themes` in `/config`, a row shown only while the theme is in season, for a Halloween startup banner, a moon-phase spinner, and a themed running light and prompt box borders.
- Improved Auto mode to ask for approval less often on routine commands, such as cleaning up temporary files, stopping a local process, or running a code formatter.
- Improved headless `-p` runs to use much less CPU, especially for long answers and when you have many saved conversations: they no longer build the conversation search index or render the transcript for display, and no longer start your custom status line and window title commands, none of which print mode shows.
- Improved rendering speed while a response streams, when a permission prompt appears, and when you resize the window.
- Improved MCP tools that are loaded on demand to return results of up to 10 KB directly to the agent; previously anything over 4 KB was saved to a file that the agent had to read in an extra step.
- Improved the `/help` shortcuts tab by leaving out basic navigation keys such as the arrow keys, so the more useful shortcuts are easier to find.
- Fixed skills, rules, custom agents, plugins, plugin MCP servers, and hooks not loading when you sign in with Application Default Credentials (`AGY_ADC_AUTH`).
- Fixed conversations compacting over and over when a single message, tool output, or attached document was too large to fit in the context.
- Fixed long links that wrap inside a Markdown table cell being linked only on their first line, to a truncated URL, so the whole link can now be clicked or copied. Tables in the default `Terminal` color scheme now use box-drawing borders instead of ASCII `|`, matching the other color schemes.
- Fixed copying a long command that wraps across rows in a code block or inline code, which now copies as a single line instead of with a line break at each wrap point; wrapped code-block lines also now break between words and keep the block's indentation.
- Fixed Vim mode's `r` replace, in Normal and Visual mode, leaving part of a collapsed `[Pasted text #N]` placeholder behind; the whole placeholder is now replaced.
- Fixed plugin and MCP server sign-ins not being saved on macOS and Windows when the token was too large for the system keychain; such tokens are now stored in the CLI's private secrets file.
- Fixed plugin MCP servers that sign in with OAuth being able to use a token saved by another user of the same computer account, or keeping the previous user's connection after you switch accounts or sign out. Their tokens now belong to the signed-in user and these servers reconnect when the user changes, so you may need to sign in to them again.

## 1.4.6

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.6.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added a `Configure MCP servers...` row for installed plugins in `/plugin`, so you can set or change a plugin's MCP server variables at any time without disabling and re-enabling it; plugins with missing values show `⚠ needs setup`, each server shows `✓ configured` or the variables it still needs, and saving restarts an enabled plugin's servers so the new values take effect.
- Improved terminal sandbox defaults to protect more credentials: sandboxed commands can no longer read or modify `~/.docker`, `~/.kube`, or `~/_netrc` unless you grant access explicitly. Previously `~/.docker` and `~/.kube` were writable inside the sandbox, so sandboxed commands that use Docker registry or Kubernetes cluster credentials now need an explicit grant.
- Improved context compaction, including `/compact`, to keep images, PDFs, and other files you attached in the conversation summary, so the agent can still see them after older history is summarized.
- Improved permission prompts so that allowing an action for the conversation, in the main agent or in a subagent, applies across the main conversation and all of its subagents instead of asking again for the same action.
- Improved the in-progress status line to show what the agent is waiting on, such as initializing MCP servers or retrying an unavailable model (for example `Model unavailable (attempt 2/10), retrying in 12s` with a live countdown), instead of a generic working label.
- Improved `/diff` to highlight the exact words that changed within each modified line, in every color scheme.
- Improved `agy plugin validate`: it now has `--help`, checks a plugin's context providers (missing `label` or `command`, invalid or duplicate triggers, unknown fields, missing command files), warns about `skills` entries in `plugin.json` that don't exist or contain no `SKILL.md`, and reports every `SKILL.md` the plugin loader skips, including skills listed through `plugin.json` or `skills.json`.
- Fixed terminal commands occasionally failing to start with `argument list too long` when the model returned a very large reasoning signature with the tool call.
- Fixed text cursors drifting away from the insertion point after wide characters (CJK, emoji), tabs, other Unicode spaces, and on soft-wrapped lines, including `Up`/`Down` landing on the wrong row, in the prompt and in the settings, permission amend, plugin setup, feedback, hooks, and artifact search boxes.
- Fixed the `Esc disabled during file edits` warning naming the wrong reject key when the prompt shows an extra choice, such as for edits outside the workspace in accept-edits mode.
- Fixed sign-in not persisting across restarts on macOS and Windows for enterprise accounts, because the saved credential exceeded the system keychain's size limit.

## 1.4.5

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.5.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Improved how agent responses read: a blank line now separates the collapsed thought block from the response, and once the response starts, the collapsed thought shows only its `Thought for …` header instead of repeating a snippet of the thinking; expand it to see the full thinking.
- Improved `/` search in the `/diff` file view to count matches inside folded unchanged lines, such as `match 2/5 · +3 hidden` or `no matches · +1 hidden`, and the `f` hint now reads `show N hidden matches`.
- Improved `/diff`'s `Commit Tree` to mark the selected commit with the same `>` cursor and selection color as `All Changes` and `Per Turn` instead of a highlighted bar, and made `Per Turn` start with the cursor on the first file instead of its turn header.
- Improved recurring cron schedules created with the agent's `schedule` tool to fire at a consistent per-schedule offset instead of exactly on the cron boundary, to avoid traffic spikes: schedules that repeat within a day, such as every 30 minutes or hourly, now fire somewhere within their period, fixed-time schedules such as daily at 9:00 still fire within their scheduled minute, and the agent can request exact timing when a schedule needs it. `@every` schedules are unchanged.
- Improved idle CPU usage by pausing screen refreshes while nothing on screen changes, roughly halving the CLI's CPU use when it is idle.
- Improved CPU usage while a response streams by skipping redundant screen updates and refreshing the credit balance less often.
- Improved rendering speed for long conversations, and made long conversations load faster when you resume them.
- Improved startup CPU usage when the CLI refreshes its conversation summaries.
- Improved memory usage by allocating storage for the prompt and other text inputs as you type instead of reserving it up front.
- Fixed the agent silently retrying, potentially without end, when a model response was blocked by content safety filters.
- Fixed plugins failing to load when `plugin.json` gives `skills` as a single path string, such as `"skills": "./skills/"`, instead of an array, as some plugins written for other tools do.
- Fixed marketplace plugin installs and automatic updates failing with a checksum mismatch or network error when a download was briefly stale or interrupted; the CLI now retries the download once.

## 1.4.4

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.4.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added Auto mode on Windows 11 version 24H2 and later for personal Google Accounts, selectable via `--mode auto`, `Agent Mode` in `/config`, `Shift+Tab`, or Remote Control Settings (`Agent` remains the default).
- Added whole-file toggle (`f`) and hunk folding (`Ctrl+O`) to `Commit Tree` and `Per Turn` views in `/diff`, and consolidated `Per Turn` diffs so multiple edits to a file in one turn appear as a single combined diff.
- Added `_meta["antigravity.google/root_conversation_id"]` to MCP `tools/call` requests so MCP servers receive the top-level conversation ID even when a tool is called from a nested subagent.
- Improved Auto mode's review of commands that leave the terminal sandbox to include the assistant's preceding question on short replies like `yes`, check every subcommand in pipelines, and prompt before destructive Git or file commands.
- Improved `agy plugin validate` with stricter checks across `plugin.json`, MCP server configs, `hooks.json`, and sidecar manifests for invalid JSON syntax, unknown fields, bad variable placeholders, unrecognized hook tool matchers, and missing hook scripts.
- Improved CPU and memory usage while streaming responses by caching streamed code-block syntax tokens, rendered Markdown blocks, and inline file-edit confirmation diffs across frames.
- Improved `/compact` and automatic compaction to retain tool declarations on summarization requests so the model API reuses its cached prompt prefix.
- Improved Remote Control on tablets and foldables to use the multi-pane layout with touch-sized controls instead of collapsing to the phone view, and kept popovers open while dragging scrollbars.
- Fixed subagents losing plugins inherited from the parent session, and fixed plugin-bundled subagents with `plugins.inherit_user: false` and restricted MCP tools failing to start with `mcp spec not found for provider`.
- Fixed rules and `SKILL.md` skills loading twice when discovered from both a standalone customization folder and an enabled plugin.
- Fixed long rows wrapping instead of truncating at the terminal width in `/diff`'s `Commit Tree` and `Per Turn` lists, and `Per Turn` headers truncating prompts at 50 characters.
- Fixed the prompt box staying mid-screen after closing panels, dropdowns, or inline prompts, and blank gaps appearing above the prompt in `Medium` verbosity mode.
- Fixed `Ctrl+Z` undo in the prompt mishandling pasted text, merging typing with recalled history entries, recording no-op `Backspace` or `Delete` steps, and truncating characters near emoji.
- Fixed MCP client sessions and background connection routines leaking when `tools/list` failed during server startup or when the CLI shut down while a server was connecting.
- Fixed the system prompt's user rules wording so `GEMINI.md` and `AGENTS.md` rules explicitly override earlier built-in instructions instead of only instructions that follow them.
- Fixed supported media attachments with parameterized MIME types such as `audio/webm; codecs=opus` being rejected as unsupported.
- Fixed several UI issues in Remote Control, including clipped headers and dialogs on phones, iOS Safari zoom on input focus, `Enable Telemetry` and `Marketing Emails` reverting while Settings loads, and dragged URLs losing query or `#` parameters.
- Fixed rendering and export bugs in Remote Control, including broken nested code blocks, `$VAR` shell variables parsed as LaTeX, broken media previews, blurry or blank diagrams in `Copy Image` and `Export as PDF`, and background-tab timer drift.

## 1.4.3

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.3.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added `/` search to the `/diff` file list and file view: matches are highlighted as you type, the search prompt shows how many matches the diff and each file contain, `Enter` jumps to the first match, and `n`/`N` step through matches one at a time across every file, with `match A/B` in the file view header. `n`/`N` in the artifact viewer now also step through matches one at a time, including several on the same line, instead of jumping from line to line.
- Improved `agy plugin validate` to also check a plugin's hooks, sidecars, and component lists: it reports an error when `hooks.json`, a `sidecar.json`, or a `skills.json`, `rules.json`, `agents.json`, or `sidecars.json` file can't be parsed, and warns about unknown hook events, hook matchers that aren't valid regular expressions and so never match, a `hooks/hooks.json` file (which isn't read), list entries with no path or with a path missing from the plugin, `commands/` folders and `workflows/` Markdown files (which plugins don't load), and a Claude Code-style top-level `"hooks"` key, which loads as a single hook named `hooks`.
- Improved timer labels in `/tasks` and the active task list to show durations in days, hours, minutes, and seconds, such as `1d 2h timer` or `5m timer`, instead of raw seconds such as `93784s timer`.
- Fixed Gemini 4 Argon not shown in `/model` and `--model` when you connect with a `GEMINI_API_KEY`.
- Fixed the CLI offering options that need the terminal sandbox on systems where it can't run, such as Linux systems that block unprivileged user namespaces and Windows before Windows 11 24H2.
- Fixed subagents and custom agents in Auto mode asking you to approve every command that would leave the terminal sandbox; like the main agent's, their commands are now first reviewed by a separate agent, so safe commands run without asking and risky ones still prompt you.
- Fixed the agent losing track of its most recently started subagents after a conversation was compacted, because the summary included each subagent's full initial prompt and was cut off before their conversation IDs; the summary now keeps only each subagent's type, role, and result, which also leaves more room in the context window.
- Fixed a `PostToolUse` hook that fails to run, for example because its command is missing, exits with an error, times out, or prints invalid JSON, marking the tool call it follows as failed even though the tool succeeded; the failure is now logged and the tool keeps its result.
- Fixed the agent failing to create empty files such as `__init__.py` or `.gitkeep`, and failing to write or edit regular project files with `... is not a valid artifact path` when the model sent blank artifact details.
- Fixed updating or reinstalling a marketplace plugin on Windows leaving it half-deleted when another `agy` session, the Antigravity desktop app, or the Remote Control background service had it open; the installed plugin now stays intact until the new copy is in place, and the previous version is restored if the replacement fails.
- Fixed `agy plugin install` and `agy plugin import` writing color codes into piped or redirected output, ignoring `NO_COLOR`, and showing raw codes in older Windows consoles; like `agy plugin validate`, they now use color only in a terminal and follow `NO_COLOR`, `CLICOLOR`, and `CLICOLOR_FORCE`.
- Fixed Remote Control on iPhone and iPad asking you to accept the `Security Notice & Data Use` terms and showing the `Enable Notifications` prompt again every time you reopened it; it now remembers your answers, along with your theme, layout, and dismissed tips.
- Fixed the prompt cursor appearing in the wrong place after resizing the terminal (sometimes on the `↑ N more lines` indicator or below the input box), when a slash command's completion hint didn't fit on the last line of the prompt (the hint is now shortened or left out), when the prompt was taller than the terminal, after pressing `Up` or `Down` onto a line with CJK characters or emoji, and after entering Vim visual mode, which also rewrapped the text.
- Fixed the cursor drifting on lines with emoji such as 👩‍💻, 👍🏽, or ⚠️ inside tmux 3.6 and later, and after returning from your external editor (`Ctrl+G`) or a `Ctrl+Z` suspend in terminals that support grapheme-cluster widths.
- Fixed the cursor drifting and lines wrapping too early under Japanese, Chinese, or Korean locales such as `LANG=ja_JP.UTF-8` when text contains characters like `→`, `…`, `─`, or `•`, which parts of the CLI counted as two columns wide while the rest drew them as one.
- Fixed `Left`, `Right`, `Backspace`, and `Delete` in the prompt and other text boxes moving over or deleting only part of an emoji such as 👩‍💻 or 👍🏽, a flag, or a letter with a combining accent, and fixed text boxes cutting off a wide character, such as a CJK character or emoji, at the end of a wrapped line instead of moving it to the next line.
- Fixed lines containing combining marks or other zero-width characters wrapping too early or leaving blank rows in `/diff` and the inline diff preview, and being cut off with `…` too soon in `/artifact` previews.

## 1.4.2

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.2.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Fixed conversation history not showing in Remote Control in daemon mode.

## 1.4.0

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.4.0.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added terminal status reporting over OSC 7501: in terminals that support it, the tab or window shows whether the CLI is working, waiting for your input, done, or failed. The CLI checks for support first, so other terminals are unaffected. Set `AGY_CLI_OSC7501=off` to turn it off, `AGY_CLI_OSC7501=on` for a terminal that supports it but doesn't answer the check, or `AGY_CLI_OSC7501_MESSAGES=brief` to show only the status without details such as the pending command or question.
- Added the `alt+m` shortcut (`Option+m` on macOS when Option is set to act as Alt) to send a message using the opposite of your `Queued Messages` setting in `/config`, so you can send right away while in `Queue` mode, or queue a message while in `Send Immediately` mode.
- Improved `agy plugin validate` so it checks a plugin with the same rules the CLI uses to load it, instead of simplified checks that rejected valid plugins (such as a manifest without a `name`) and missed problems that kept a plugin from loading. It lists each error and warning with its file and line, accepts a plugin directory or its `plugin.json`, warns about common `plugin.json` mistakes such as unknown fields (with "did you mean" suggestions), invalid names, and components placed inside `.antigravity-plugin/` instead of the plugin root, and adds `--strict` to fail on warnings and `--json` for a machine-readable report in CI.
- Fixed the CLI refusing every message with `Eligibility check failed` until you restarted it when the service was briefly unavailable or rate-limited at launch; the check now retries temporary errors and no longer locks the session.
- Fixed plugin MCP servers that use a variable in a request header, such as `"Authorization": "Bearer ${TOKEN}"`, sending the literal placeholder and failing to authenticate; headers now get the value you configured, like the server's command, arguments, and environment already did.
- Fixed the `/diff` Commit Tree view: the header now counts commits instead of lines, the cursor stops only on commit rows and `Enter` opens that commit, the view fills the terminal height, and it shows the latest 100 commits (previously 10) with scrolling.
- Fixed the agent losing track of its file changes, tasks, and session cost when a background command finished while the agent kept working; they no longer roll back to the point where that command started.
- Fixed a background command's final output sometimes missing from its task log; the output is now always recorded when the command finishes or is canceled.
- Fixed links to directories disappearing from agent responses; they now show the directory name, for example `pipelines/`.

## 1.3.5

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.3.5.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added Auto mode, which approves file edits and safe commands without asking and still prompts before irreversible actions; commands that would leave the terminal sandbox are first reviewed by a separate agent. Choose it with `--mode auto`, from `Agent Mode` in `/config`, or by pressing `Shift+Tab` to cycle modes. Auto mode is available on Linux and macOS, with Windows support coming later.
- Added the `/compact` command to compact the conversation on demand and free up the context window: `/compact` on its own summarizes the conversation and ends the turn, and `/compact <message>` summarizes it and then answers your message. While it runs the CLI shows a `Compacting conversation...` progress label that you can cancel with `Esc`, and when it finishes it shows how many steps were summarized and how much smaller the context became.
- Added syntax highlighting to the `/diff` file view, with token colors for each color scheme and a background tint on added and removed lines. With the `Terminal` color scheme the CLI detects whether your terminal has a light or dark background and picks matching colors. The color scheme previews in `/config` and first-run setup now show a sample exactly as `/diff` draws it.
- Added folding to the `/diff` file view: each hunk header now shows how many unchanged lines are hidden above it, `Ctrl+O` expands or collapses the fold nearest the cursor, and `f` switches between showing only the changes and the whole file. Both keys work on uncommitted changes when the file on disk still matches the diff, and the footer explains when they can't be used.
- Improved `/diff` performance on very large files by rendering only the rows on screen, so scrolling, expanding folds, and opening the whole file no longer freeze the CLI. Expanding folds and showing the whole file are turned off for files over 100,000 lines or 10 MB, and the footer says why.
- Fixed colors being reduced to 256 colors in iTerm2 over SSH, where `COLORTERM` is not forwarded; the CLI now uses full 24-bit color when `LC_TERMINAL=iTerm2` is set, unless `COLORTERM` or `NO_COLOR` says otherwise.

## 1.3.4

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.3.4.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added a `--json` flag to `agy plugin list` for machine-readable output, and fixed the command showing only imported plugins: it now lists every installed plugin, including ones installed from a marketplace, with its version and whether it is enabled.
- Changed `--model` and `/model` to accept a base model name without `--effort`: instead of failing with an error asking for `--effort`, the CLI now picks the model's default thinking level (the server's default for that model, otherwise medium, otherwise the lowest available).
- Improved Remote Control so the browser's Settings modal opens for CLI sessions and shows the settings the CLI actually uses (project and global permissions, queued messages, AI credits, telemetry, and artifact review) instead of a notice that settings can't be changed in the browser, and `agy remote-control serve` sessions now use your saved `settings.json` and save changes made in the browser back to it.
- Improved the `/model` picker for Business sign-in with a Google Cloud project on pay-as-you-go: third-party models your project can't access are now hidden instead of failing when you send a message.
- Fixed long stalls when model requests fail repeatedly: the agent now waits at most 30 seconds between automatic retries instead of up to 4 minutes.
- Fixed remote MCP servers that use OAuth signing you out after a temporary network failure, timeout, or server error; saved sign-ins are now cleared only when the server or its authorization server actually rejects them.
- Fixed `--agent` silently running the default agent when the name matches no agent: headless `-p` runs now exit with code 1 and list the available agents, and interactive sessions show an `Agent Not Found` warning before falling back to the default agent.
- Fixed combining `--print` with `--prompt-interactive` exiting with status 0 after reporting the conflict; it now exits with status 2 like other print-mode usage errors.
- Fixed `/diff` showing `No uncommitted changes` in Git, Mercurial, and Jujutsu repositories configured to always color output, for example with `color.ui = always`.
- Fixed `@conversation:` suggestions getting stuck on `Fetching matches for ...` when conversation search is slow; after 2 seconds the list now falls back to your local conversations.
- Fixed the `Agents:` row in `/plugin` plugin details leaving out subagents a plugin declares in its root `agents.json`; it now lists every loaded agent by name instead of by its `agents/` folder name.
- Fixed "Always allow" rules approved from a Remote Control browser session still applying after you removed them in the browser's rules editor or the shared tab of `/permissions`; these rules are now saved only to the shared `config.json`.
- Fixed requests failing with `thinking_budget and thinking_level are not supported together` when signed in with Application Default Credentials and using a model that has a thinking level.
- Fixed a conversation failing on every later request after the agent read a truncated or header-only WebM file; such files are now rejected when read instead of being attached.

## 1.3.3

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.3.3.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added a pinned prompt header in no flickering mode while you scroll back through a long conversation: the prompt that produced the response you're reading stays at the top of the transcript, and clicking it jumps back to that prompt.
- Added support for MCP servers to mark a tool as always loaded by setting `_meta: {"antigravity/alwaysLoad": true}` on it in their `tools/list` response, so the agent gets that tool directly instead of discovering it on demand.
- Added support for a root-level `agents.json` in plugins, so a plugin can declare its subagents the same way it declares skills and rules with `skills.json` and `rules.json`.
- Changed the macOS terminal sandbox to block sandboxed commands from reading `~/Library/Application Support` by default, since desktop apps keep credentials and session tokens there; previously it was readable, and you can still allow it explicitly in your sandbox rules.
- Improved error messages: a request that fails with an HTML error page, for example from a corporate proxy, now shows the page title instead of the raw HTML, other long non-JSON error bodies are cut off after 500 bytes, and reaching your individual quota is reported right away instead of being retried.
- Improved search in the `/plugin` Installed tab: you can now type spaces in a search query, press `Enter` to finish searching, then use `Space` to toggle the selected plugin and `Enter` to expand its details; start typing again to resume the search.
- Fixed an expired or revoked sign-in showing an unclear error mid-session; the agent now says `Authentication expired. Please log back in.`, and a token refresh that was already in flight no longer restores the expired credentials.
- Fixed `/add-dir` claiming it added a path that doesn't exist or isn't a directory; it now reports `directory not found` or `not a directory`.
- Fixed `/btw` side questions running your user and workspace hooks, which could make hooks such as stop hooks loop or add extra steps to a quick question.
- Fixed Jujutsu (`jj`) commands run by the agent, such as `jj diff` or `jj log`, hanging in an interactive pager; agent commands now set `JJ_PAGER=cat` alongside `PAGER` and `GIT_PAGER`.
- Fixed subagents started with a `branch` or `share` workspace in a multi-repository workspace silently working in your real checkout; each repository now gets its own isolated copy.
- Fixed a stopped subagent staying in the active agents list while it still had an approval pending; stopping it now clears its pending approvals right away.
- Fixed `--remote-control` failing when you sign in with Application Default Credentials (`AGY_ADC_AUTH`); Remote Control doesn't support ADC yet, so the flag now exits with a clear error and the `/remote-control` command is hidden.
- Fixed custom `alt` keybindings such as `alt+s` not working with the macOS Option key in terminals that don't treat Option as Meta, such as Terminal.app and VS Code-based terminals.
- Fixed `/keybindings` silently doing nothing when the configured editor can't be found; it now shows an error.
- Fixed `agy plugin validate` and plugin listings missing skills declared through the `skills` field in `plugin.json` or ignoring `skills.json` exclusions, so they now match the skills that actually load, and fixed a race that could drop results when importing plugins.
- Fixed sandboxed commands failing with `Access is denied.` on Windows when PowerShell 7 was installed from the Microsoft Store; the agent now falls back to Windows PowerShell in that case.
- Fixed `/diff` showing the error from `git diff HEAD` instead of the real cause, such as a corrupt index, when the fallback `git diff` also fails.
- Fixed file links in agent responses whose line anchor was percent-encoded, such as `file.go%23L795`; the label now shows the line number and the link opens the correct line.
- Fixed separate links to the same URL highlighting together when you hover over one of them in terminals that support clickable links.
- Fixed counts in tool steps and the `/codesearch` panel, which now read "Found 1 result", "1 match", "1 file", and "Wrote 1 line" instead of "1 results", and the file-creation step reporting one line too many.

## 1.3.2

### 📦 Add-on & Container Wrapper
- Upgraded bundled upstream Antigravity CLI binary to v1.3.2.
- Rebuilt container base images with latest security patches.

### 🤖 Google Antigravity CLI (agy)
- Added `/plugin`, an interactive manager for the official Antigravity plugin marketplace: browse and install plugins that bundle skills, MCP servers, subagents, rules, and hooks, or install them from your shell without opening the CLI with `agy plugin install <plugin-name>@antigravity-plugins-official`; install one straight from a folder on your computer with `+ Install from local directory...`; fill in any settings a plugin needs in a simple form before it turns on; and manage installed plugins with `/plugin install`, `uninstall`, `enable`, `disable`, and `list`.
- Added more options for plugin authors: keep the manifest in a `.antigravity-plugin/` or `.gemini-plugin/` folder, list skills in `plugin.json`, store data in a per-plugin folder available as `PLUGIN_DATA`, and ship command-line tools in a `bin/` folder that the agent can run by name.
- Improved plugin installs: the plugin list opens instantly, an interrupted install never leaves a half-installed plugin behind, and installing or removing plugins on Windows is more reliable.
- Improved plugin compatibility: plugins load every skill in their `skills/` folder, remote MCP servers start correctly once their settings are filled in, and a plugin's subagents can use the plugin's own MCP servers.
- Changed `--dangerously-skip-permissions` to stop auto-approving the agent's implementation plan in `/plan` mode: the flag now only skips tool permission prompts, so plans wait for your review again. Set `Artifact Review` in `/config` if you want plans and other artifacts to proceed automatically.
- Improved CPU usage while the agent runs long shell commands with a lot of output, since output that is already valid UTF-8 is no longer rescanned in full on every update.
- Fixed `Tab`, `→`, and `←` in the `/diff` Commit Tree view moving the cursor to other lines instead of switching views as the `←/→ switch view` hint says, and added `Shift+Tab` to switch to the previous view in every `/diff` tab.
- Fixed the `/resume` conversation picker crashing when you pressed `Enter` to import a conversation from the `Other` tab on a narrow terminal, and conversation titles with CJK characters being cut off mid-character.
- Fixed conversations that collect many images failing on Claude models: images the agent views or you attach are now scaled down to at most 2576 pixels per side (previously 4096), keeping them within the model's limits however many images a conversation contains.
- Fixed a timer the agent scheduled with a wake-up condition keeping a CPU core at 100% until it expired when the condition could no longer be met; the timer now waits idly and fires on schedule.

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
