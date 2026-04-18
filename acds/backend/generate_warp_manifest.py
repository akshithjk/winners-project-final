import json
import random
from datetime import datetime, timedelta

def main():
    ips = [f"192.168.1.{i}" for i in range(1, 20)] + [f"10.0.0.{i}" for i in range(1, 5)] + ["203.0.113.45", "198.51.100.22", "8.8.8.8"]
    types = ["BruteForce", "C2Beacon", "Exfiltration", "CorrelatedIncident"]
    severities = ["Medium", "High", "Critical"]
    
    events = []
    base_time = datetime.utcnow()
    
    for i in range(5000):
        t = types[random.choices([0, 1, 2, 3], weights=[40, 30, 20, 10])[0]]
        sev = severities[random.choices([0, 1, 2], weights=[50, 30, 20])[0]]
        if t == "CorrelatedIncident": 
            sev = "Critical"
        fp = random.random() < 0.1
        if fp:
            sev = "Low"
            
        evt = {
            "alert_id": f"WARP-{i:05d}",
            "timestamp": (base_time - timedelta(minutes=5000 - i)).isoformat() + "Z",
            "src_ip": random.choice(ips),
            "dst_ip": random.choice(ips),
            "type": t,
            "severity": sev,
            "why_flagged": f"Warp speed synthetic detection for {t}. This is a stress-test payload simulating intense network traffic spanning multiple nodes.",
            "correlated": t == "CorrelatedIncident",
            "false_positive": fp,
            "mitre": {"id": "T" + str(random.randint(1000, 1500)), "name": t},
            "playbook": f"1. Isolate IP.\n2. Invalidate sessions.\n3. Analyze TTPs." if sev == "Critical" else ""
        }
        events.append(evt)
        
    with open("speed_test_manifest.json", "w") as f:
        json.dump(events, f)
    print("Generated 5000 events in speed_test_manifest.json")

if __name__ == "__main__":
    main()
