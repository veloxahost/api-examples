"""Minimal VeloxaHost API client (stdlib only).

    export VELOXA_API_KEY=veloxa_...
    python veloxa.py list
    python veloxa.py create web-01 --cpu 2 --memory 2048 --disk 40
    python veloxa.py state web-01 restart
    python veloxa.py volume db-data 50GiB
    python veloxa.py alert "High CPU" cpu_percent 80 --channels email
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = os.environ.get("VELOXA_API", "https://console.veloxahost.com/api/v1")


class Veloxa:
    def __init__(self, key: str, api: str = API):
        self.key, self.api = key, api.rstrip("/")

    def request(self, method: str, path: str, body=None, retries: int = 3):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.api + path, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.key}")
        req.add_header("Content-Type", "application/json")
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries:
                    time.sleep(int(e.headers.get("Retry-After", "5")))
                    continue
                detail = e.read().decode(errors="replace")
                raise SystemExit(f"{method} {path} -> HTTP {e.code}: {detail}")

    def instances(self):
        res = self.request("GET", "/instances")
        return res if isinstance(res, list) else (res or {}).get("instances", (res or {}).get("data", []))

    def create(self, name, cpu=1, memory_mb=1024, disk_gb=20, image="ubuntu/24.04"):
        return self.request("POST", "/instances", {
            "name": name, "type": "container", "image": image,
            "cpu_limit": cpu, "memory_limit_mb": memory_mb, "disk_size_gb": disk_gb,
        })

    def state(self, name, action):
        return self.request("POST", f"/instances/{name}/state", {"action": action})

    def volume(self, name, size, pool="default"):
        return self.request("POST", f"/storage/pools/{pool}/volumes", {"name": name, "config": {"size": size}})

    def alert(self, name, metric, threshold, condition="gt", channels="email", cooldown=15):
        return self.request("POST", "/alerts/rules", {
            "name": name, "metric": metric, "condition": condition,
            "threshold": threshold, "channels": channels, "cooldown_minutes": cooldown,
        })


def main():
    key = os.environ.get("VELOXA_API_KEY") or sys.exit("export VELOXA_API_KEY first")
    v = Veloxa(key)
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    c = sub.add_parser("create"); c.add_argument("name")
    c.add_argument("--cpu", type=int, default=1); c.add_argument("--memory", type=int, default=1024)
    c.add_argument("--disk", type=int, default=20)
    s = sub.add_parser("state"); s.add_argument("name")
    s.add_argument("action", choices=["start", "stop", "restart", "freeze", "unfreeze"])
    vo = sub.add_parser("volume"); vo.add_argument("name"); vo.add_argument("size")
    a = sub.add_parser("alert"); a.add_argument("name"); a.add_argument("metric")
    a.add_argument("threshold", type=float); a.add_argument("--channels", default="email")
    args = p.parse_args()

    if args.cmd == "list":
        for i in v.instances():
            print(f"{i.get('name', ''):<24} {i.get('status', ''):<10} {i.get('type', '')}")
    elif args.cmd == "create":
        print(json.dumps(v.create(args.name, args.cpu, args.memory, args.disk), indent=2))
    elif args.cmd == "state":
        print(json.dumps(v.state(args.name, args.action), indent=2))
    elif args.cmd == "volume":
        print(json.dumps(v.volume(args.name, args.size), indent=2))
    elif args.cmd == "alert":
        print(json.dumps(v.alert(args.name, args.metric, args.threshold, channels=args.channels), indent=2))


if __name__ == "__main__":
    main()
