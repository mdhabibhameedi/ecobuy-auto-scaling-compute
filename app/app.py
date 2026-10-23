import math, socket, time, urllib.request
from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Bamboo toothbrush set", "price": 4.99},
    {"id": 2, "name": "Reusable beeswax wraps", "price": 9.50},
    {"id": 3, "name": "Recycled notebook", "price": 3.75},
    {"id": 4, "name": "Stainless steel bottle", "price": 14.00},
    {"id": 5, "name": "Organic cotton tote bag", "price": 6.25},
    {"id": 6, "name": "Solar phone charger", "price": 22.90},
]


def instance_id():
    """Ask the EC2 metadata service which instance served the request."""
    try:
        t = urllib.request.Request("http://169.254.169.254/latest/api/token", method="PUT",
                                   headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"})
        token = urllib.request.urlopen(t, timeout=1).read().decode()
        r = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id",
                                   headers={"X-aws-ec2-metadata-token": token})
        return urllib.request.urlopen(r, timeout=1).read().decode()
    except Exception:
        return socket.gethostname()


SERVED_BY = instance_id()


@app.route("/")
def home():
    rows = "".join(f"<li>{p['name']} - ${p['price']:.2f}</li>" for p in PRODUCTS)
    return (f"<h1>EcoBuy</h1><p>Eco-friendly products</p><ul>{rows}</ul>"
            f"<p><small>Served by instance: {SERVED_BY}</small></p>")


@app.route("/health")
def health():
    return "ok", 200


@app.route("/api/products")
def products():
    return jsonify({"served_by": SERVED_BY, "products": PRODUCTS})


@app.route("/work")
def work():
    """Busy for about 200 ms of CPU so load tests can push CPU usage up."""
    end = time.time() + 0.2
    n = 0
    while time.time() < end:
        math.sqrt(n * n + 1)
        n += 1
    return jsonify({"served_by": SERVED_BY, "loops": n})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
