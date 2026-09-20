# Changelog

## 1.0.1

- **Multi-Architecture Support**: Added `build.yaml` mapping for both `amd64` and `aarch64` base images (`ghcr.io/home-assistant/{arch}-base-debian:bookworm`).
- **Integrated HA CLI**: Bundled official statically linked `ha` CLI (`v5.5.0`) with Supervisor manager privileges.
- **Auto-Update Engine**: Implemented automatic Antigravity CLI updates on container startup when `auto_update: true`.
- **Config & State Safety**: Safe JSON merging of `cliRemoteControlHostname` with `jq` to prevent clobbering existing configuration.
- **Default Directory**: Set container working directory to `/config`.
- **Credential Synchronization**: Timestamp-aware OAuth token sync between host `/config/.gemini` and container `/data/.gemini`.

## 1.0.0

- Initial release of the dedicated Antigravity Remote Control Home Assistant add-on.
- Native Debian Bookworm base with glibc runtime.
- S6-overlay v3 process supervision (`agy remote-control serve`).
- Home Assistant UI lifecycle controls (Start, Stop, Restart, Watchdog, Log viewer).
