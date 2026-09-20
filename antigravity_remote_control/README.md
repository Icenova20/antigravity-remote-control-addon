# Antigravity Remote Control for Home Assistant

Runs the headless Google Antigravity Remote Control daemon (`agy remote-control serve`) as a native, supervised Home Assistant add-on.

## Features

- **Decoupled Architecture**: No longer dependent on SSH add-on keepalive scripts or Alpine musl/glibc shims.
- **Native Debian Base**: Built on `ghcr.io/home-assistant/amd64-base-debian:bookworm` for native glibc compatibility and maximum stability.
- **Auto-Restart & Supervision**: Monitored by s6-overlay with native Home Assistant Watchdog integration.
- **Persistent State**: Credentials and sessions remain persistent in `/data/.gemini/` across restarts and updates.
- **Direct Management**: Provides native Home Assistant controls: Start, Stop, Restart, Auto-boot, and Log viewer.

## Installation

See [repository documentation](../README.md) for installation steps via the Home Assistant Add-on Store.
