#!/bin/bash
mkdir -p TRINITY_COORDINATION/active_instances
cat > TRINITY_COORDINATION/active_instances/instance-6.json <<EOJ
{"instance_num": 6, "role": "C6-Specialist", "status": "ONLINE", "registered_at": "$(date -Iseconds)", "current_task": "Available", "pid": $$}
EOJ
echo "✅ Instance 6 (C6-Specialist) REGISTERED!"
cat TRINITY_COORDINATION/active_instances/*.json 2>/dev/null | grep -o '"role":"[^"]*"' | wc -l | xargs -I {} echo "Total registered: {}/6"
