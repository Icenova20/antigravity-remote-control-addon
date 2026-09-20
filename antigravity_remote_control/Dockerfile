FROM ghcr.io/home-assistant/amd64-base-debian:bookworm

# Environment settings
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    HOME=/root

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        jq \
        procps \
        python3 \
        python3-pip \
        openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Google Antigravity CLI binary
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- -d /usr/local/bin \
    && chmod +x /usr/local/bin/agy

# Copy rootfs overlay
COPY rootfs /

# Set up S6 services and executable permissions
RUN chmod 755 /usr/local/bin/run_antigravity.sh \
    && chmod 755 /etc/s6-overlay/s6-rc.d/antigravity/run \
    && chmod 644 /etc/s6-overlay/s6-rc.d/antigravity/type \
    && mkdir -p /etc/s6-overlay/user-bundles.d/user/contents.d \
    && touch /etc/s6-overlay/user-bundles.d/user/contents.d/antigravity \
    && chmod 644 /etc/s6-overlay/user-bundles.d/user/contents.d/antigravity \
    && mkdir -p /etc/s6-overlay/s6-rc.d/user/contents.d \
    && touch /etc/s6-overlay/s6-rc.d/user/contents.d/antigravity \
    && chmod 644 /etc/s6-overlay/s6-rc.d/user/contents.d/antigravity
