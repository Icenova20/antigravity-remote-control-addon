#!/usr/bin/env python3
"""
Antigravity Local AI Microservice
Exposes a lightweight, native HTTP REST API for local Gemini prompt, multimodal
classification, and OpenAI-compatible chat completions inside Home Assistant,
running natively on Debian Bookworm (glibc).
"""

import base64
import http.server
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

PORT = 8199
AGY_BIN = "/usr/local/bin/agy"
DEFAULT_MODEL = "gemini-3.8-flash-low"
DEFAULT_TIMEOUT = 30.0
MODELS_LIST = [
    "gemini-3.8-flash-low",
    "gemini-3.1-pro-low",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

def resolve_path(path_str):
    """Resolves file paths across /config and /homeassistant mounts."""
    if not path_str or not isinstance(path_str, str):
        return path_str
    if os.path.exists(path_str):
        return path_str
    if path_str.startswith('/homeassistant') and os.path.exists(path_str.replace('/homeassistant', '/config', 1)):
        return path_str.replace('/homeassistant', '/config', 1)
    if path_str.startswith('/config') and os.path.exists(path_str.replace('/config', '/homeassistant', 1)):
        return path_str.replace('/config', '/homeassistant', 1)
    return path_str

def fetch_ha_camera_snapshot(camera_entity):
    """Fetches a camera snapshot from Home Assistant Core via the Supervisor API."""
    token = os.environ.get('SUPERVISOR_TOKEN')
    if not token:
        raise RuntimeError("SUPERVISOR_TOKEN not available; cannot query Home Assistant Core")

    entity_clean = camera_entity.strip()
    url = f"http://supervisor/core/api/camera_proxy/{entity_clean}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = resp.read()
                out_path = f"/dev/shm/cam_{uuid.uuid4().hex}.jpg"
                with open(out_path, "wb") as f:
                    f.write(data)
                return out_path
            raise RuntimeError(f"Home Assistant Core returned HTTP {resp.status}")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch camera snapshot for {entity_clean}: {e}")

def save_base64_image(b64_str):
    """Decodes a base64 or data URI image to a temporary file in RAM disk."""
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]
    raw_data = base64.b64decode(b64_str)
    out_path = f"/dev/shm/b64_{uuid.uuid4().hex}.jpg"
    with open(out_path, "wb") as f:
        f.write(raw_data)
    return out_path

def download_image_url(img_url):
    """Downloads an external image URL to /dev/shm/."""
    req = urllib.request.Request(img_url, headers={"User-Agent": "Antigravity-HA/1.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        if resp.status == 200:
            data = resp.read()
            out_path = f"/dev/shm/url_{uuid.uuid4().hex}.jpg"
            with open(out_path, "wb") as f:
                f.write(data)
            return out_path
        raise RuntimeError(f"HTTP {resp.status} downloading image")

class AntigravityAPIHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        data = json.dumps(payload, indent=2).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        sys.stderr.write(f"[antigravity-api] {self.address_string()} - {format % args}\n")

    def do_GET(self):
        # Healthcheck
        if self.path in ('/health', '/status'):
            version = "unknown"
            if os.path.exists(AGY_BIN):
                try:
                    res = subprocess.run([AGY_BIN, "--version"], capture_output=True, text=True, timeout=5)
                    if res.returncode == 0:
                        version = res.stdout.strip()
                except Exception:
                    pass

            self._send_json(200, {
                "status": "ok",
                "service": "antigravity-api",
                "agy_version": version,
                "models": MODELS_LIST,
                "timestamp": int(time.time())
            })
            return

        # OpenAI-compatible models list
        if self.path in ('/v1/models', '/models'):
            models_data = []
            for m in MODELS_LIST:
                models_data.append({
                    "id": m,
                    "object": "model",
                    "created": 1789900000,
                    "owned_by": "google-antigravity",
                    "permission": [],
                    "root": m,
                    "parent": None
                })
            self._send_json(200, {
                "object": "list",
                "data": models_data
            })
            return

        self._send_json(404, {"error": "Endpoint not found", "success": False})

    def do_POST(self):
        valid_endpoints = (
            '/v1/prompt',
            '/v1/classify',
            '/v1/chat/completions',
            '/chat/completions'
        )
        if self.path not in valid_endpoints:
            self._send_json(404, {"error": "Endpoint not found", "success": False})
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            params = json.loads(body.decode('utf-8')) if body else {}
        except Exception as e:
            self._send_json(400, {"error": f"Invalid JSON payload: {e}", "success": False})
            return

        model = params.get('model', DEFAULT_MODEL)
        timeout = float(params.get('timeout', DEFAULT_TIMEOUT))

        # ----------------------------------------------------------------------
        # 1. Native /v1/prompt endpoint
        # ----------------------------------------------------------------------
        if self.path == '/v1/prompt':
            prompt = params.get('prompt')
            if not prompt:
                self._send_json(400, {"error": "'prompt' field is required", "success": False})
                return

            schema = params.get('schema') or params.get('json_schema')
            if schema:
                prompt += (
                    f"\n\nYou must respond ONLY with a raw JSON object matching this schema:\n"
                    f"{json.dumps(schema, indent=2)}\n"
                    "Do not include markdown backticks or explanations."
                )

            cmd = [AGY_BIN, "--model", model, "--dangerously-skip-permissions", "-p", prompt]
            start_t = time.time()
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                duration = round(time.time() - start_t, 2)
                if res.returncode != 0:
                    self._send_json(500, {
                        "error": f"agy execution failed (code {res.returncode}): {res.stderr.strip()}",
                        "duration_sec": duration,
                        "success": False
                    })
                    return

                self._send_json(200, {
                    "response": res.stdout.strip(),
                    "model": model,
                    "duration_sec": duration,
                    "success": True
                })
            except subprocess.TimeoutExpired:
                self._send_json(504, {
                    "error": f"agy execution timed out after {timeout}s",
                    "duration_sec": round(time.time() - start_t, 2),
                    "success": False
                })
            except Exception as e:
                self._send_json(500, {
                    "error": f"Internal execution error: {e}",
                    "duration_sec": round(time.time() - start_t, 2),
                    "success": False
                })
            return

        # ----------------------------------------------------------------------
        # 2. Native /v1/classify endpoint (supports file, camera_entity, base64, URL)
        # ----------------------------------------------------------------------
        if self.path == '/v1/classify':
            temp_files_to_clean = []
            resolved_path = None

            try:
                if params.get('camera_entity'):
                    resolved_path = fetch_ha_camera_snapshot(params['camera_entity'])
                    temp_files_to_clean.append(resolved_path)
                elif params.get('image_base64'):
                    resolved_path = save_base64_image(params['image_base64'])
                    temp_files_to_clean.append(resolved_path)
                elif params.get('image_url'):
                    resolved_path = download_image_url(params['image_url'])
                    temp_files_to_clean.append(resolved_path)
                elif params.get('image_path'):
                    resolved_path = resolve_path(params['image_path'])
                else:
                    self._send_json(400, {
                        "error": "One of 'image_path', 'camera_entity', 'image_base64', or 'image_url' is required",
                        "success": False
                    })
                    return

                if not resolved_path or not os.path.exists(resolved_path):
                    self._send_json(404, {
                        "error": f"Image file not found: {resolved_path}",
                        "success": False
                    })
                    return

                prompt = params.get('prompt')
                schema = params.get('schema') or params.get('json_schema')

                if not prompt:
                    prompt = (
                        f"Inspect the image file {resolved_path}. Is this a delivery drop-off or package left at the door, "
                        "or is it a resident/visitor carrying personal items, groceries, backpack, or walking past? "
                        "Output ONLY a raw JSON object with keys: "
                        "\"is_delivery\" (bool: true if a courier is dropping off, taking photo of, or has left a delivery parcel/box/bag/food at the door; false for personal items, groceries, worn bags, or passers-by), "
                        "\"carrier\" (string: Amazon, UPS, FedEx, USPS, DHL, DoorDash, UberEats, Other, or None), "
                        "\"parcel_type\" (string: box, padded envelope, poly bag, food delivery, other, or none), "
                        "\"confidence\" (float between 0.0 and 1.0), "
                        "\"summary\" (short concise string describing what is happening). "
                        "Do not include markdown formatting or backticks."
                    )
                else:
                    prompt = prompt.replace("{image_path}", resolved_path)
                    if schema:
                        prompt += f"\n\nRespond ONLY with a JSON object conforming to:\n{json.dumps(schema, indent=2)}\nNo markdown backticks."

                cmd = [AGY_BIN, "--model", model, "--dangerously-skip-permissions", "-p", prompt]
                start_t = time.time()
                try:
                    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                    duration = round(time.time() - start_t, 2)
                    if res.returncode != 0 or not res.stdout:
                        self._send_json(500, {
                            "error": f"agy execution failed (code {res.returncode}): {res.stderr.strip()}",
                            "duration_sec": duration,
                            "success": False
                        })
                        return

                    raw_output = res.stdout.strip()
                    match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                    parsed_json = None
                    if match:
                        try:
                            parsed_json = json.loads(match.group(0))
                        except Exception:
                            pass
                    if parsed_json is None:
                        try:
                            parsed_json = json.loads(raw_output)
                        except Exception:
                            pass

                    self._send_json(200, {
                        "classification": parsed_json,
                        "raw": raw_output,
                        "model": model,
                        "duration_sec": duration,
                        "success": True
                    })
                except subprocess.TimeoutExpired:
                    self._send_json(504, {
                        "error": f"agy classification timed out after {timeout}s",
                        "duration_sec": round(time.time() - start_t, 2),
                        "success": False
                    })
                except Exception as e:
                    self._send_json(500, {
                        "error": f"Internal classification error: {e}",
                        "duration_sec": round(time.time() - start_t, 2),
                        "success": False
                    })
            finally:
                for tmp in temp_files_to_clean:
                    if os.path.exists(tmp):
                        try:
                            os.remove(tmp)
                        except Exception:
                            pass
            return

        # ----------------------------------------------------------------------
        # 3. OpenAI-Compatible /v1/chat/completions endpoint
        # ----------------------------------------------------------------------
        if self.path in ('/v1/chat/completions', '/chat/completions'):
            messages = params.get('messages', [])
            if not messages or not isinstance(messages, list):
                self._send_json(400, {
                    "error": {
                        "message": "'messages' array is required in chat completions request",
                        "type": "invalid_request_error",
                        "code": 400
                    }
                })
                return

            temp_files_to_clean = []
            prompt_parts = []

            try:
                for msg in messages:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')

                    if isinstance(content, str):
                        if role == 'system':
                            prompt_parts.append(f"System Instructions: {content}")
                        elif role == 'assistant':
                            prompt_parts.append(f"Previous Assistant Response: {content}")
                        else:
                            prompt_parts.append(f"User Request: {content}")
                    elif isinstance(content, list):
                        # Multimodal message block
                        user_texts = []
                        for part in content:
                            if isinstance(part, dict):
                                if part.get('type') == 'text' and 'text' in part:
                                    user_texts.append(part['text'])
                                elif part.get('type') == 'image_url':
                                    img_info = part.get('image_url', {})
                                    img_url = img_info.get('url', '') if isinstance(img_info, dict) else str(img_info)
                                    if img_url.startswith('data:image'):
                                        tmp_img = save_base64_image(img_url)
                                        temp_files_to_clean.append(tmp_img)
                                        user_texts.append(f"[Image provided at {tmp_img}]")
                                    elif img_url.startswith(('http://', 'https://')):
                                        tmp_img = download_image_url(img_url)
                                        temp_files_to_clean.append(tmp_img)
                                        user_texts.append(f"[Image provided at {tmp_img}]")
                                    elif os.path.exists(resolve_path(img_url)):
                                        resolved = resolve_path(img_url)
                                        user_texts.append(f"[Image provided at {resolved}]")
                        prompt_parts.append(f"{role.capitalize()}: " + " ".join(user_texts))

                assembled_prompt = "\n\n".join(prompt_parts)
                cmd = [AGY_BIN, "--model", model, "--dangerously-skip-permissions", "-p", assembled_prompt]
                start_t = time.time()
                try:
                    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                    if res.returncode != 0:
                        self._send_json(500, {
                            "error": {
                                "message": f"agy execution failed (code {res.returncode}): {res.stderr.strip()}",
                                "type": "internal_error",
                                "code": 500
                            }
                        })
                        return

                    completion_text = res.stdout.strip()
                    created_time = int(time.time())
                    chat_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
                    p_tokens = len(assembled_prompt) // 4
                    c_tokens = len(completion_text) // 4

                    self._send_json(200, {
                        "id": chat_id,
                        "object": "chat.completion",
                        "created": created_time,
                        "model": model,
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": completion_text
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": p_tokens,
                            "completion_tokens": c_tokens,
                            "total_tokens": p_tokens + c_tokens
                        }
                    })
                except subprocess.TimeoutExpired:
                    self._send_json(504, {
                        "error": {
                            "message": f"Execution timed out after {timeout}s",
                            "type": "timeout_error",
                            "code": 504
                        }
                    })
                except Exception as e:
                    self._send_json(500, {
                        "error": {
                            "message": f"Internal execution error: {e}",
                            "type": "internal_error",
                            "code": 500
                        }
                    })
            finally:
                for tmp in temp_files_to_clean:
                    if os.path.exists(tmp):
                        try:
                            os.remove(tmp)
                        except Exception:
                            pass
            return

class ReusableThreadingServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True

def main():
    server_address = ('0.0.0.0', PORT)
    sys.stderr.write(f"[antigravity-api] Starting Antigravity Local AI Microservice on port {PORT}...\n")
    httpd = ReusableThreadingServer(server_address, AntigravityAPIHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == '__main__':
    main()
