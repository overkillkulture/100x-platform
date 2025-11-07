#!/bin/bash
mkdir -p TRINITY_COORDINATION/active_instances
cat > TRINITY_COORDINATION/active_instances/instance-4.json <<EOJ
{"instance_num": 4, "role": "C4-Specialist", "status": "ONLINE", "registered_at": "$(date -Iseconds)", "current_task": "Available", "pid": $$}
EOJ
echo "✅ Instance 4 (C4-Specialist) REGISTERED!"
cat TRINITY_COORDINATION/active_instances/*.json 2>/dev/null | grep -o '"role":"[^"]*"' | wc -l | xargs -I {} echo "Total registered: {}/6"
