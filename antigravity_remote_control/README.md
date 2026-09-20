# Antigravity Remote Control for Home Assistant

Runs the headless Google Antigravity Remote Control daemon (`agy remote-control serve`) as a native, supervised Home Assistant add-on.

## Features

- **Decoupled Architecture**: No longer dependent on SSH add-on keepalive scripts or Alpine musl/glibc shims.
- **Multi-Architecture Base**: Built on official Debian Bookworm base (`ghcr.io/home-assistant/{arch}-base-debian:bookworm`) supporting `amd64` and `aarch64`.
- **Integrated HA CLI**: Includes `ha` CLI configured with Supervisor manager privileges for autonomous server management.
- **Auto-Restart & Supervision**: Monitored by s6-overlay with native Home Assistant Watchdog integration.
- **Persistent State**: Credentials and sessions remain persistent in `/data/.gemini/` across restarts and updates.
- **Direct Management**: Provides native Home Assistant controls: Start, Stop, Restart, Auto-boot, and Log viewer.

## Installation

1. In Home Assistant, navigate to **Settings > Add-ons > Add-on Store**.
2. Click the three dots in the top-right corner, select **Repositories**, and add:
   ```text
   https://github.com/Icenova20/antigravity-remote-control-addon
   ```
3. Locate **Antigravity Remote Control** in the store, click **Install**, and then click **Start**.

For source code and issue tracking, visit the [GitHub Repository](https://github.com/Icenova20/antigravity-remote-control-addon).
