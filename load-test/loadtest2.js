// Load test for the EcoBuy load balancer.
// Usage:  node loadtest2.js http://YOUR-LOAD-BALANCER-DNS-NAME
// Three phases: quiet, spike, quiet. It prints a line every 10 seconds.
const base = process.argv[2];
if (!base) { console.log('Usage: node loadtest2.js http://<load-balancer-dns>'); process.exit(1); }

const phases = [
  { name: 'quiet', seconds: 60,  concurrency: 2 },
  { name: 'SPIKE', seconds: 1200, concurrency: 40 },
  { name: 'quiet', seconds: 120, concurrency: 2 },
];

let stats = { n: 0, errors: 0, total: 0 };
const servers = new Set();

async function worker(stopAt) {
  while (Date.now() < stopAt) {
    const t = Date.now();
    try {
      const r = await fetch(base + '/work');
      const j = await r.json();
      servers.add(j.served_by);
      if (!r.ok) stats.errors++;
    } catch (e) { stats.errors++; }
    stats.n++; stats.total += Date.now() - t;
  }
}

(async () => {
  const t0 = Date.now();
  for (const p of phases) {
    const stopAt = Date.now() + p.seconds * 1000;
    const workers = Array.from({ length: p.concurrency }, () => worker(stopAt));
    const timer = setInterval(() => {
      const avg = stats.n ? (stats.total / stats.n).toFixed(0) : 0;
      console.log(`${((Date.now() - t0) / 1000).toFixed(0).padStart(4)} s  phase=${p.name}  requests=${stats.n}  avg=${avg} ms  errors=${stats.errors}  instances_seen=${servers.size}`);
      stats = { n: 0, errors: 0, total: 0 };
    }, 10000);
    await Promise.all(workers);
    clearInterval(timer);
  }
  console.log('Done. Different instances that served requests:', [...servers].join(', '));
})();
