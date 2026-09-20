#!/command/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Antigravity Remote Control
# Starts the Antigravity Remote Control daemon (agy remote-control serve)
# ==============================================================================

set -e

bashio::log.info "Starting Antigravity Remote Control bootstrap..."

# 0. Ensure cross-compatibility between /config and /homeassistant paths
if [ -d /homeassistant ] && [ ! -e /config ]; then
    ln -sf /homeassistant /config
elif [ -d /config ] && [ ! -e /homeassistant ]; then
    ln -sf /config /homeassistant
fi

# 1. Ensure persistent storage layout in /data/.gemini
mkdir -p /data/.gemini/config/projects /data/.gemini/antigravity-cli

# Symlink /root/.gemini to /data/.gemini
rm -rf /root/.gemini
ln -sf /data/.gemini /root/.gemini

# 2. Token & state auto-migration / synchronization from /homeassistant/.gemini or /config/.gemini
if [ -f /homeassistant/.gemini/antigravity-cli/antigravity-oauth-token ]; then
    if [ ! -f /data/.gemini/antigravity-cli/antigravity-oauth-token ] || [ /homeassistant/.gemini/antigravity-cli/antigravity-oauth-token -nt /data/.gemini/antigravity-cli/antigravity-oauth-token ]; then
        bashio::log.info "Migrating/synchronizing Antigravity OAuth credentials from /homeassistant/.gemini..."
        cp -a /homeassistant/.gemini/. /data/.gemini/ 2>/dev/null || true
    fi
elif [ -f /config/.gemini/antigravity-cli/antigravity-oauth-token ]; then
    if [ ! -f /data/.gemini/antigravity-cli/antigravity-oauth-token ] || [ /config/.gemini/antigravity-cli/antigravity-oauth-token -nt /data/.gemini/antigravity-cli/antigravity-oauth-token ]; then
        bashio::log.info "Migrating/synchronizing Antigravity OAuth credentials from /config/.gemini..."
        cp -a /config/.gemini/. /data/.gemini/ 2>/dev/null || true
    fi
fi

if [ ! -f /data/.gemini/antigravity-cli/antigravity-oauth-token ]; then
    bashio::log.warning "No existing Antigravity OAuth token found! Authentication will be required."
fi

# Ensure strict permissions on token
if [ -f /data/.gemini/antigravity-cli/antigravity-oauth-token ]; then
    chmod 600 /data/.gemini/antigravity-cli/antigravity-oauth-token
fi

# 3. Read and apply configuration options
INSTANCE_NAME="homeassistant"
if bashio::config.has_value 'instance_name'; then
    INSTANCE_NAME=$(bashio::config 'instance_name')
fi

bashio::log.info "Configured instance name: ${INSTANCE_NAME}"

# Update ~/.gemini/config/config.json safely preserving any existing user settings
if [ -f /data/.gemini/config/config.json ]; then
    TMP_JSON=$(mktemp)
    if jq --arg host "$INSTANCE_NAME" '.userSettings.cliRemoteControlHostname = $host' /data/.gemini/config/config.json > "$TMP_JSON" 2>/dev/null; then
        mv "$TMP_JSON" /data/.gemini/config/config.json
    else
        rm -f "$TMP_JSON"
    fi
fi

if [ ! -f /data/.gemini/config/config.json ]; then
    cat << EOF > /data/.gemini/config/config.json
{
  "userSettings": {
    "cliRemoteControlHostname": "${INSTANCE_NAME}",
    "themeMode": "THEME_MODE_LIGHT"
  }
}
EOF
fi

# Ensure outside-of-project.json exists
if [ ! -f /data/.gemini/config/projects/outside-of-project.json ]; then
    cat << 'EOF' > /data/.gemini/config/projects/outside-of-project.json
{
  "id": "outside-of-project",
  "name": "Outside of Project",
  "projectResources": {}
}
EOF
fi

# 4. Binary check & fallback
if [ ! -x /usr/local/bin/agy ]; then
    if [ -x /config/bin/agy ]; then
        bashio::log.info "Copying agy binary from /config/bin/agy..."
        cp -f /config/bin/agy /usr/local/bin/agy
        chmod +x /usr/local/bin/agy
    elif [ -x /homeassistant/bin/agy ]; then
        bashio::log.info "Copying agy binary from /homeassistant/bin/agy..."
        cp -f /homeassistant/bin/agy /usr/local/bin/agy
        chmod +x /usr/local/bin/agy
    else
        bashio::log.info "Downloading agy binary..."
        curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- -d /usr/local/bin
        chmod +x /usr/local/bin/agy
    fi
fi

# 5. Handle Auto-Update check
if bashio::config.true 'auto_update'; then
    bashio::log.info "Checking for Antigravity CLI updates..."
    /usr/local/bin/agy update || bashio::log.warning "Auto-update check failed or host offline; continuing with current version."
fi

CURRENT_VER=$(/usr/local/bin/agy --version 2>/dev/null || echo "unknown")
bashio::log.info "Antigravity CLI version: ${CURRENT_VER}"

# 6. Verify Home Assistant CLI availability
if command -v ha >/dev/null 2>&1; then
    bashio::log.info "Home Assistant CLI available at $(command -v ha)"
else
    bashio::log.warning "Home Assistant CLI not found in PATH"
fi

# 7. Set working directory to Home Assistant root
if [ -d /config ]; then
    cd /config
elif [ -d /homeassistant ]; then
    cd /homeassistant
fi

bashio::log.info "Working directory set to: $(pwd)"
bashio::log.info "Starting 'agy remote-control serve' in foreground..."

# 8. Execute daemon in foreground
exec /usr/local/bin/agy remote-control serve
