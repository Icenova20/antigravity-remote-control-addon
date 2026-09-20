#!/usr/bin/env python3
"""
Antigravity Local AI Microservice
Exposes a lightweight, native HTTP REST API for local Gemini prompt & multimodal
classification inside Home Assistant, running natively on Debian Bookworm (glibc).
"""

import http.server
import json
import os
import re
import subprocess
import sys
import time

PORT = 8199
AGY_BIN = "/usr/local/bin/agy"
DEFAULT_MODEL = "gemini-3.8-flash-low"

class AntigravityAPIHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        data = json.dumps(payload, indent=2).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        # Keep logs clean and structured
        sys.stderr.write(f"[antigravity-api] {self.address_string()} - {format % args}\n")

    def do_GET(self):
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
                "timestamp": int(time.time())
            })
            return

        self._send_json(404, {"error": "Endpoint not found", "success": False})

    def do_POST(self):
        if self.path not in ('/v1/prompt', '/v1/classify'):
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
        timeout = float(params.get('timeout', 18.0))

        if self.path == '/v1/prompt':
            prompt = params.get('prompt')
            if not prompt:
                self._send_json(400, {"error": "'prompt' field is required", "success": False})
                return

            cmd = [
                AGY_BIN,
                "--model", model,
                "--dangerously-skip-permissions",
                "-p", prompt
            ]

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

        if self.path == '/v1/classify':
            image_path = params.get('image_path')
            if not image_path:
                self._send_json(400, {"error": "'image_path' field is required", "success": False})
                return

            # Resolve paths between /config and /homeassistant mounts
            resolved_path = image_path
            if not os.path.exists(resolved_path):
                if resolved_path.startswith('/homeassistant') and os.path.exists(resolved_path.replace('/homeassistant', '/config', 1)):
                    resolved_path = resolved_path.replace('/homeassistant', '/config', 1)
                elif resolved_path.startswith('/config') and os.path.exists(resolved_path.replace('/config', '/homeassistant', 1)):
                    resolved_path = resolved_path.replace('/config', '/homeassistant', 1)

            if not os.path.exists(resolved_path):
                self._send_json(404, {
                    "error": f"Image file not found: {image_path} (resolved as {resolved_path})",
                    "success": False
                })
                return

            prompt = params.get('prompt')
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
                # Ensure the resolved image path is embedded in the prompt
                prompt = prompt.replace("{image_path}", resolved_path)

            cmd = [
                AGY_BIN,
                "--model", model,
                "--dangerously-skip-permissions",
                "-p", prompt
            ]

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
