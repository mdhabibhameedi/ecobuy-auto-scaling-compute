"""Generates the two SYNTHETIC datasets for the EcoBuy assignment.
traffic.csv  - hourly website hits for 7 days (with a sale-evening spike on day 5)
metrics.json - simulated CPU and memory usage over the same hours
All values are generated, not real customer data."""
import csv, json, math, random
from datetime import datetime, timedelta

random.seed(42)
start = datetime(2026, 11, 1, 0, 0)
traffic, metrics = [], []
for h in range(7 * 24):
    t = start + timedelta(hours=h)
    daily = 0.5 + 0.5 * math.sin((t.hour - 9) / 24 * 2 * math.pi)
    base = 300 + 900 * max(daily, 0)
    sale = 1 if (t.day == 5 and 18 <= t.hour <= 22) else 0
    hits = int(base * (4.5 if sale else 1) * random.uniform(0.85, 1.15))
    traffic.append({"timestamp": t.strftime("%Y-%m-%d %H:%M"), "hits": hits, "sale_event": sale})
    cpu = min(97, 8 + hits / 55 + random.uniform(-3, 3))
    mem = min(90, 30 + hits / 220 + random.uniform(-2, 2))
    metrics.append({"timestamp": t.strftime("%Y-%m-%d %H:%M"),
                    "cpu_percent": round(cpu, 1), "memory_percent": round(mem, 1)})

with open("traffic.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["timestamp", "hits", "sale_event"])
    w.writeheader(); w.writerows(traffic)
with open("metrics.json", "w") as f:
    json.dump({"source": "synthetic", "interval": "1 hour", "data": metrics}, f, indent=2)
print("rows:", len(traffic), "peak hits:", max(r["hits"] for r in traffic),
      "peak cpu:", max(m["cpu_percent"] for m in metrics))
