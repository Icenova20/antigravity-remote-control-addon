# Antigravity Home Assistant Add-on Repository

Official Home Assistant Add-on repository for running the Google Antigravity Remote Control daemon (`agy remote-control serve`).

## Add-ons in this Repository

| Add-on | Description | Architecture |
|---|---|---|
| **Antigravity Remote Control** | Standalone headless Antigravity Remote Control daemon connecting your Home Assistant instance to `antigravity.google.com`. | `amd64`, `aarch64` |

---

## Installation

1. In your Home Assistant frontend, navigate to **Settings** > **Add-ons** > **Add-on Store**.
2. Click the three vertical dots in the upper-right corner and select **Repositories**.
3. Add the repository URL:
   ```text
   https://github.com/Icenova20/antigravity-remote-control-addon
   ```
4. Click **Add**, then **Close**.
5. Locate **Antigravity Remote Control** in the store, click it, and click **Install**.

---

## Features

- **Native Debian Bookworm Base**: Eliminates Alpine musl / glibc relocation issues with native glibc support.
- **S6-Overlay Process Supervision**: Full service lifecycle management under s6-overlay with auto-restart on unexpected crashes.
- **Persistent Data Storage**: Stores authentication tokens and conversation cache in `/data/.gemini/` persisting across add-on updates.
- **Zero-Friction Token Auto-Migration**: Automatically inherits existing credentials from `/config/.gemini/` if present.
- **Home Assistant Supervisor API Integration**: Runs with manager privileges to query host diagnostics, supervise system services, and restart core on command.
- **Host Network Mode**: Loopback requests (`127.0.0.1:8123`) reach Home Assistant Core directly with minimal latency.
- **Live Logging**: Streams `agy` authentication status and command traces directly to the Home Assistant Add-on Log UI.

---

## Configuration

In the add-on configuration tab, customize the following options:

```yaml
instance_name: "homeassistant"
auto_update: true
```

- **`instance_name`** (*string*, default: `homeassistant`): The hostname identifier that will appear on [antigravity.google.com](https://antigravity.google.com).
- **`auto_update`** (*boolean*, default: `true`): Allows `agy` to verify and install background CLI binary updates on startup.

---

## Support & Development

Maintained by `Icenova20`. For questions or issues, open an issue in this repository.
