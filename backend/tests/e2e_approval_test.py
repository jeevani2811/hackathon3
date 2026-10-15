import urllib.request
import json
import time

base_url = 'http://127.0.0.1:8000/api/v1'

print("=== STARTING HUMAN-IN-THE-LOOP (HITL) APPROVAL TEST ===")

# Create Task in SUPERVISED mode
payload = json.dumps({
    'title': 'High-Stakes Financial Production Migration',
    'objective': 'Execute production database update and broadcast operational alert to webhooks',
    'context': 'Requires multi-stage authorization and cryptographic action payload audit',
    'mode': 'supervised',
    'priority': 'critical',
    'parameters': {'budget_threshold': 50000}
}).encode('utf-8')

req = urllib.request.Request(f'{base_url}/tasks', data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as resp:
    task = json.loads(resp.read().decode('utf-8'))
task_id = task['id']
print(f"1. Supervised Task Created -> ID: {task_id}, Status: {task['status']}")

# Poll for pending approvals
approval_found = None
for i in range(15):
    time.sleep(1)
    req = urllib.request.Request(f'{base_url}/approvals?task_id={task_id}&status=pending')
    with urllib.request.urlopen(req) as resp:
        approvals = json.loads(resp.read().decode('utf-8'))
    if approvals:
        approval_found = approvals[0]
        print(f"2. Found Pending Approval: {approval_found['title']} (Type: {approval_found['action_type']})")
        break

if not approval_found:
    print("Warning: No pending approvals found in 15 seconds.")
else:
    appr_id = approval_found['id']
    decide_payload = json.dumps({
        'decision': 'approve',
        'decision_notes': 'Operator cryptographically approved this sensitive action.'
    }).encode('utf-8')
    req = urllib.request.Request(f'{base_url}/approvals/{appr_id}/decide', data=decide_payload, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as resp:
        decide_res = json.loads(resp.read().decode('utf-8'))
    print(f"3. Approval Response Status: {decide_res['status']}")

    # Wait for completion
    for i in range(15):
        time.sleep(1)
        req = urllib.request.Request(f'{base_url}/tasks/{task_id}')
        with urllib.request.urlopen(req) as resp:
            t_data = json.loads(resp.read().decode('utf-8'))
        print(f"   Status at tick {i+1}: {t_data['status']}")
        if t_data['status'] in ('completed', 'failed'):
            break

print("=== HITL APPROVAL TEST FINISHED ===")
