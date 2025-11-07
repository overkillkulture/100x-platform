#!/bin/bash
mkdir -p TRINITY_COORDINATION/active_instances
cat > TRINITY_COORDINATION/active_instances/instance-1.json <<EOF
{"instance_num": 1, "role": "C1-Mechanic", "status": "ONLINE", "registered_at": "$(date -Iseconds)", "current_task": "Managing Hub", "pid": $$}
EOF
echo "✅ Instance 1 (C1-Mechanic) REGISTERED!"
cat TRINITY_COORDINATION/active_instances/*.json 2>/dev/null | grep -o '"role":"[^"]*"' | wc -l | xargs -I {} echo "Total registered: {}/6"
