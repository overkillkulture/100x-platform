#!/bin/bash
mkdir -p TRINITY_COORDINATION/active_instances
cat > TRINITY_COORDINATION/active_instances/instance-2.json <<EOJ
{"instance_num": 2, "role": "C2-Architect", "status": "ONLINE", "registered_at": "$(date -Iseconds)", "current_task": "Available", "pid": $$}
EOJ
echo "✅ Instance 2 (C2-Architect) REGISTERED!"
cat TRINITY_COORDINATION/active_instances/*.json 2>/dev/null | grep -o '"role":"[^"]*"' | wc -l | xargs -I {} echo "Total registered: {}/6"
