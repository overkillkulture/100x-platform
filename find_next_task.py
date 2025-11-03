import json

with open('todo_brain_local.json', 'r') as f:
    brain = json.load(f)

completed_ids = {t['id'] for t in brain['tasks'] if t['status'] == 'Complete'}

# Find Trinity autonomous tasks (C1, C2, C3)
trinity_tasks = []
for task in brain['tasks']:
    if (task['status'] != 'Complete' and
        not task['commander_review'] and
        task['assigned_to'] in ['C1 Mechanic', 'C2 Architect', 'C3 Oracle']):
        deps_met = all(dep in completed_ids for dep in task.get('dependencies', []))
        if deps_met:
            trinity_tasks.append(task)

trinity_tasks.sort(key=lambda t: t['priority'], reverse=True)

print('🎯 NEXT TRINITY AUTONOMOUS TASKS:\n')
if trinity_tasks:
    for i, task in enumerate(trinity_tasks[:10], 1):
        print(f'{i}. Task #{task["id"]} (P{task["priority"]}): {task["task"]}')
        print(f'   Assigned: {task["assigned_to"]} | Est: {task["estimated_hours"]}h')
        print()
else:
    print('⚠️  No Trinity tasks available - all blocked on Commander decisions\n')

# Show what's blocking
commander_tasks = [t for t in brain['tasks'] if t['status'] != 'Complete' and t['commander_review']]
commander_tasks.sort(key=lambda t: t['priority'], reverse=True)
print(f'🚨 {len(commander_tasks)} Commander decisions needed:\n')
for task in commander_tasks[:5]:
    print(f'   Task #{task["id"]} (P{task["priority"]}): {task["task"]}')
