import json
import random
from datetime import datetime, timedelta

def main():
    ips = [f"192.168.1.{i}" for i in range(1, 20)] + [f"10.0.0.{i}" for i in range(1, 5)] + [f"185.220.101.{i}" for i in range(20, 30)]
    types = ["BruteForce", "C2Beacon", "Exfiltration", "CorrelatedIncident"]
    severities = ["Low", "Medium", "High", "Critical"]
    
    events = []
    base_time = datetime.utcnow()
    
    for i in range(5000):
        t = types[random.choices([0, 1, 2, 3], weights=[40, 30, 20, 10])[0]]
        sev = severities[random.choices([0, 1, 2, 3], weights=[30, 30, 20, 20])[0]]
        if t == "CorrelatedIncident": 
            sev = "Critical"
            
        evt = {
            "alert_id": f"ACDS-{i:05d}",
            "timestamp": (base_time - timedelta(minutes=5000 - i)).isoformat() + "Z",
            "src_ip": random.choice(ips),
            "dst_ip": random.choice(ips),
            "type": t,
            "severity": sev,
            "why_flagged": f"High-speed synthetic detection for {t}.",
            "correlated": t == "CorrelatedIncident",
            "false_positive": sev == "Low",
            "mitre": {"id": "T" + str(random.randint(1000, 1500)), "name": t},
            "playbook": f"1. Isolate IP.\n2. Invalidate sessions.\n3. Analyze TTPs." if sev == "Critical" else ""
        }
        events.append(evt)
        
    with open("sample_logs.json", "w") as f:
        json.dump(events, f)
    print("Generated 5000 pre-computed alerts in sample_logs.json")

if __name__ == "__main__":
    main()
