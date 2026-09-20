# Changelog

## 1.2.7

- Synced add-on version directly with Google Antigravity CLI release stream.
- Added automated GitHub Action (`check-upstream-agy.yml`) to notify Home Assistant when Google publishes new releases.
- Multi-architecture base for `amd64` and `aarch64` (`ghcr.io/home-assistant/{arch}-base-debian:bookworm`).
- Bundled official statically linked `ha` CLI (`v5.5.0`) with Supervisor manager privileges.
- Streamlined configuration options for single instance name setting.

## 1.0.1

- Multi-Architecture Support: Added `build.yaml` mapping for both `amd64` and `aarch64`.
- Integrated HA CLI: Bundled official statically linked `ha` CLI (`v5.5.0`).
- Auto-Update Engine: Added Antigravity CLI updates on startup.
- Config & State Safety: Safe JSON merging of `cliRemoteControlHostname`.

## 1.0.0

- Initial release of the dedicated Antigravity Remote Control Home Assistant add-on.
- Native Debian Bookworm base with glibc runtime.
- S6-overlay v3 process supervision (`agy remote-control serve`).
- Home Assistant UI lifecycle controls (Start, Stop, Restart, Watchdog, Log viewer).
