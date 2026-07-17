#!/usr/bin/env python3
# Publica AT Designs en Vercel (público). Token en la variable de entorno VT.
import os, json, ssl, urllib.request, urllib.error, pathlib
TOKEN = os.environ.get("VT", "").strip()
if not TOKEN: raise SystemExit("Falta el token en VT")
NAME = "at-designs"
html = (pathlib.Path(__file__).parent / "index.html").read_text(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
def api(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=180, context=ctx)
        return r.getcode(), json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")
code, res = api("POST", "https://api.vercel.com/v13/deployments?skipAutoDetectionConfirmation=1", {
    "name": NAME, "files": [{"file": "index.html", "data": html}],
    "projectSettings": {"framework": None}, "target": "production"})
print("deploy status:", code)
if code >= 400: print("ERROR:", json.dumps(res)[:400]); raise SystemExit(1)
api("PATCH", f"https://api.vercel.com/v9/projects/{NAME}", {"ssoProtection": None})
print("OK -> https://at-designs.vercel.app")
