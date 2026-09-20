# Home Assistant Add-on: Antigravity Remote Control

Runs the Google Antigravity Remote Control daemon (`agy remote-control serve`) as a managed, supervised background service within Home Assistant.

## How it works

The Antigravity CLI daemon establishes a secure outbound connection to Google Antigravity (`antigravity.google.com`), allowing authorized users to run autonomous tasks, manage Home Assistant, and control smart home integrations from the Antigravity web interface.

## Permissions & Privileges

This add-on requests:
- **`homeassistant_config:rw`**: Mounts `/config` and `/homeassistant` (your Home Assistant configuration directory) allowing `agy` to read and edit YAML configurations, scripts, and automations.
- **`share:rw`**: Mounts `/share` for persistent shared artifacts.
- **`ssl:ro`**: Access to local SSL certificates if configured.
- **`hassio_api: true` & `hassio_role: manager`**: Grants permission to manage other add-ons, query supervisor logs, execute `ha` CLI commands, and restart Home Assistant Core when requested.
- **`host_network: true`**: Allows low-latency loopback communication (`127.0.0.1:8123`) to Home Assistant Core.

## Tools Included

- **`agy`**: Google Antigravity CLI binary with auto-update support.
- **`ha`**: Home Assistant CLI preconfigured with Supervisor API credentials (`SUPERVISOR_TOKEN`) for autonomous system and add-on administration.
- **`git`**, **`curl`**, **`jq`**, **`python3`**, **`openssh-client`**: Core development utilities.

## Configuration

In the **Configuration** tab:

```yaml
instance_name: "homeassistant"
auto_update: true
```

- **`instance_name`**: The unique hostname identifier shown in the Antigravity web dashboard. Default is `homeassistant`.
- **`auto_update`**: Automatically checks for and applies new Antigravity CLI releases on startup.

## Authentication

If you previously authenticated `agy` in the SSH add-on or on the host, this add-on **automatically detects and migrates** your existing OAuth token from `/homeassistant/.gemini/` or `/config/.gemini/` on initial launch.

If starting fresh without prior credentials:
1. Start the add-on.
2. Check the **Log** tab in Home Assistant.
3. If an authentication URL is printed, copy and open the link in your browser to sign in with your Google account.
4. The authentication token is persisted permanently in `/data/.gemini/` and will survive reboots and container upgrades.

## Logs

All daemon activity, connection events, and authentication state can be monitored in real time under the **Log** tab.
