import urllib.request
import json
import time

base_url = 'http://127.0.0.1:8000/api/v1'

print("=== STARTING FULL END-TO-END FLOW TEST ===")

# 1. Create Task
payload = json.dumps({
    'title': 'Autonomous Enterprise Market Intelligence Evaluation',
    'objective': 'Evaluate top 3 vector database engines for high-throughput series-B fintech infrastructure',
    'context': 'Focus on p99 latency under 20ms and compliance',
    'parameters': {'budget_threshold': 20000, 'strict_mode': True}
}).encode('utf-8')

req = urllib.request.Request(f'{base_url}/tasks', data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as resp:
    task = json.loads(resp.read().decode('utf-8'))
task_id = task['id']
print(f"1. Task Created -> ID: {task_id}, Status: {task['status']}")

# 2. Poll until workflow creates subtasks or reaches awaiting approval / completed
for i in range(15):
    time.sleep(1)
    req = urllib.request.Request(f'{base_url}/tasks/{task_id}')
    with urllib.request.urlopen(req) as resp:
        t_data = json.loads(resp.read().decode('utf-8'))
    print(f"   Step {i+1} -> Status: {t_data['status']}, Subtasks: {len(t_data.get('subtasks', []))}")
    if t_data['status'] in ('awaiting_approval', 'completed', 'failed'):
        break

# 3. Check approvals
req = urllib.request.Request(f'{base_url}/approvals?task_id={task_id}&status=pending')
with urllib.request.urlopen(req) as resp:
    approvals = json.loads(resp.read().decode('utf-8'))
print(f"2. Pending Approvals: {len(approvals)}")

# 4. If pending, approve it
if approvals:
    appr_id = approvals[0]['id']
    decide_payload = json.dumps({'decision': 'approved', 'decision_notes': 'Automated test approval'}).encode('utf-8')
    req = urllib.request.Request(f'{base_url}/approvals/{appr_id}/decide', data=decide_payload, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as resp:
        decide_res = json.loads(resp.read().decode('utf-8'))
    print(f"3. Approval Decided -> Status: {decide_res['status']}")
    
    # Wait for completion
    for i in range(10):
        time.sleep(1)
        req = urllib.request.Request(f'{base_url}/tasks/{task_id}')
        with urllib.request.urlopen(req) as resp:
            t_data = json.loads(resp.read().decode('utf-8'))
        print(f"   Post-Approval Step {i+1} -> Status: {t_data['status']}")
        if t_data['status'] in ('completed', 'failed'):
            break

# 5. Check Artifacts
req = urllib.request.Request(f'{base_url}/artifacts?task_id={task_id}')
with urllib.request.urlopen(req) as resp:
    artifacts = json.loads(resp.read().decode('utf-8'))
print(f"4. Artifacts Generated: {len(artifacts)}")
for a in artifacts:
    print(f"   - {a['file_name']} ({a['file_type']}, size: {a['size_bytes']} bytes)")
    # Test downloading content
    content_req = urllib.request.Request(f"{base_url}/artifacts/{a['id']}/download")
    with urllib.request.urlopen(content_req) as c_resp:
        data = c_resp.read()
        print(f"     Downloaded successfully: {len(data)} bytes")

print("=== TEST COMPLETED SUCCESSFULLY ===")
