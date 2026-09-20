# Antigravity Home Assistant Add-ons

[![GitHub Release](https://img.shields.io/github/v/release/Icenova20/antigravity-remote-control-addon?include_prereleases&color=41adf5&label=Version)](https://github.com/Icenova20/antigravity-remote-control-addon/releases)
[![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg)](https://github.com/Icenova20/antigravity-remote-control-addon)
[![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg)](https://github.com/Icenova20/antigravity-remote-control-addon)
[![License](https://img.shields.io/github/license/Icenova20/antigravity-remote-control-addon?color=blue)](LICENSE)

Official Home Assistant Add-on repository for running the Google Antigravity Remote Control daemon (`agy remote-control serve`).

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FIcenova20%2Fantigravity-remote-control-addon)

---

## Add-ons in this Repository

| Add-on | Description | Architecture |
|---|---|---|
| [**Antigravity Remote Control**](antigravity_remote_control/) | Standalone headless Google Antigravity Remote Control daemon connecting your Home Assistant instance directly to `antigravity.google.com`. | `amd64`, `aarch64` |

---

## Quick Installation

### Option 1: One-Click Installation (Recommended)
Click the badge below to open your Home Assistant instance and add this repository automatically:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FIcenova20%2Fantigravity-remote-control-addon)

### Option 2: Manual Installation
1. In your Home Assistant frontend, navigate to **Settings** > **Add-ons** > **Add-on Store**.
2. Click the three vertical dots in the upper-right corner and select **Repositories**.
3. Add the repository URL:
   ```text
   https://github.com/Icenova20/antigravity-remote-control-addon
   ```
4. Click **Add**, then **Close**.
5. Locate **Antigravity Remote Control** under the *Antigravity Add-ons* section, click it, and click **Install**.
6. Start the add-on and monitor the **Log** tab to authenticate or confirm active connection.

---

## Features

- **Native Debian Bookworm Base**: Eliminates Alpine musl / glibc relocation issues with native glibc support.
- **Dual-Service S6-Overlay Architecture**: Runs both the outbound remote control tunnel (`agy remote-control serve`) and the local AI microservice under s6-overlay with auto-restart on unexpected crashes.
- **Native Local AI Microservice (Port 8199)**: Exposes a lightweight HTTP REST API (`/v1/classify`, `/v1/prompt`, `/health`) for local Gemini prompt & multimodal image classification, accessible by any Home Assistant automation or script without dependencies.
- **Integrated Home Assistant CLI (`ha`)**: Bundles the official `ha` CLI with internal Supervisor manager privileges, enabling autonomous server administration.
- **Automated Upstream Sync**: Daily automated GitHub Action monitors Google's official release stream and alerts Home Assistant when a new `agy` binary is released.
- **Persistent Data Storage**: Stores authentication tokens and conversation cache in `/data/.gemini/`, persisting across add-on updates.
- **Zero-Friction Token Auto-Migration**: Automatically inherits existing credentials from `/homeassistant/.gemini/` or `/config/.gemini/` if present.
- **Host Network Mode**: Loopback requests (`127.0.0.1:8123`) reach Home Assistant Core directly with minimal latency.
- **Live Logging**: Streams `agy` authentication status and command traces directly to the Home Assistant Add-on Log UI.

---

## Configuration

In the add-on **Configuration** tab, customize the following option:

```yaml
instance_name: "homeassistant"
```

- **`instance_name`** (*string*, default: `homeassistant`): The hostname identifier that will appear on [antigravity.google.com](https://antigravity.google.com).

---

## Support & Issues

For questions, feature requests, or bug reports, please open an issue in this repository.
