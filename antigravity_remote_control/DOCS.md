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
```

- **`instance_name`**: The unique hostname identifier shown in the Antigravity web dashboard (`antigravity.google.com`). Default is `homeassistant`.

## Authentication

If you previously authenticated `agy` in the SSH add-on or on the host, this add-on **automatically detects and migrates** your existing OAuth token from `/homeassistant/.gemini/` or `/config/.gemini/` on initial launch.

If starting fresh without prior credentials:
1. Start the add-on.
2. Check the **Log** tab in Home Assistant.
3. If an authentication URL is printed, copy and open the link in your browser to sign in with your Google account.
4. The authentication token is persisted permanently in `/data/.gemini/` and will survive reboots and container upgrades.

## Local AI Microservice REST API (Port 8199)

In addition to remote browser control, this add-on runs a native, local HTTP microservice on `http://127.0.0.1:8199`. Because the add-on runs with `host_network: true`, Home Assistant automations, REST commands, and external scripts can execute Gemini reasoning with zero external dependencies:

### 1. Using Antigravity as Home Assistant Assist Voice Brain (OpenAI Conversation)

You can turn Gemini 3.8 Flash (running under your Google AI Ultra subscription quota via `agy`) into your default **Home Assistant Voice Assistant & Conversation Agent**:

1. In Home Assistant, go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for and select **OpenAI Conversation**.
3. Fill in the connection settings:
   - **API Key**: `antigravity` (or any placeholder string)
   - Click **Submit**.
4. In the integration options:
   - Expand **Advanced Settings** (if prompted) or click **Configure**.
   - Set **Server URL** to:
     ```text
     http://127.0.0.1:8199/v1
     ```
   - Select **Model**: `gemini-3.8-flash-low` (or `gemini-3.1-pro-low`).
5. Open Home Assistant Assist (voice button in top-right or mobile app) and select your Antigravity conversation agent!

---

### REST API Endpoints

#### 1. `GET /v1/models`
Returns available models in standard OpenAI format:
```bash
curl http://127.0.0.1:8199/v1/models
```

#### 2. `POST /v1/chat/completions`
Standard OpenAI chat completion endpoint supporting multi-turn conversations and vision:
```bash
curl -X POST http://127.0.0.1:8199/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.8-flash-low",
    "messages": [
      {"role": "system", "content": "You are a smart home assistant."},
      {"role": "user", "content": "Are the doors locked?"}
    ]
  }'
```

#### 3. `POST /v1/classify` (Entity-Aware Multimodal Vision)
Inspects camera frames or snapshot images. Supports **4 flexible input modes**:
- **Direct HA Camera Entity** (fetches live snapshot from HA Core automatically):
  ```bash
  curl -X POST http://127.0.0.1:8199/v1/classify \
    -H "Content-Type: application/json" \
    -d '{"camera_entity": "camera.front_door"}'
  ```
- **Local File Path**:
  ```bash
  curl -X POST http://127.0.0.1:8199/v1/classify \
    -H "Content-Type: application/json" \
    -d '{"image_path": "/config/www/delivery_latest.jpg"}'
  ```
- **Base64 Payload**:
  ```bash
  curl -X POST http://127.0.0.1:8199/v1/classify \
    -H "Content-Type: application/json" \
    -d '{"image_base64": "data:image/jpeg;base64,..."}'
  ```
- **External Image URL**:
  ```bash
  curl -X POST http://127.0.0.1:8199/v1/classify \
    -H "Content-Type: application/json" \
    -d '{"image_url": "https://example.com/snapshot.jpg"}'
  ```

#### 4. `POST /v1/prompt`
Submits arbitrary text prompts with optional JSON schema enforcement:
```bash
curl -X POST http://127.0.0.1:8199/v1/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Summarize this system alert: ...",
    "model": "gemini-3.8-flash-low"
  }'
```

#### 5. `GET /health`
Verifies microservice health and returns installed `agy` CLI version:
```bash
curl http://127.0.0.1:8199/health
```

---

## Logs

All daemon activity, connection events, and authentication state can be monitored in real time under the **Log** tab.

