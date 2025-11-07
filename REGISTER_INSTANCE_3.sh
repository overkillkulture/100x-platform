#!/bin/bash
mkdir -p TRINITY_COORDINATION/active_instances
cat > TRINITY_COORDINATION/active_instances/instance-3.json <<EOJ
{"instance_num": 3, "role": "C3-Oracle", "status": "ONLINE", "registered_at": "$(date -Iseconds)", "current_task": "Available", "pid": $$}
EOJ
echo "✅ Instance 3 (C3-Oracle) REGISTERED!"
cat TRINITY_COORDINATION/active_instances/*.json 2>/dev/null | grep -o '"role":"[^"]*"' | wc -l | xargs -I {} echo "Total registered: {}/6"
