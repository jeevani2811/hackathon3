import pytest
from backend.app.orchestration.dag import DAGScheduler

def test_ready_subtasks_resolution():
    subtasks = [
        {"id": "st-1", "dependencies": [], "status": "pending"},
        {"id": "st-2", "dependencies": ["st-1"], "status": "pending"},
        {"id": "st-3", "dependencies": ["st-1", "st-2"], "status": "pending"}
    ]
    
    # Initially only st-1 should be ready
    ready = DAGScheduler.get_ready_subtasks(subtasks, completed_ids=set())
    assert len(ready) == 1
    assert ready[0]["id"] == "st-1"

    # Once st-1 is completed, st-2 should become ready
    ready = DAGScheduler.get_ready_subtasks(subtasks, completed_ids={"st-1"})
    assert len(ready) == 1
    assert ready[0]["id"] == "st-2"

    # Once st-1 and st-2 are completed, st-3 should become ready
    ready = DAGScheduler.get_ready_subtasks(subtasks, completed_ids={"st-1", "st-2"})
    assert len(ready) == 1
    assert ready[0]["id"] == "st-3"

def test_cycle_detection():
    # Acyclic graph
    acyclic = [
        {"id": "a", "dependencies": []},
        {"id": "b", "dependencies": ["a"]},
        {"id": "c", "dependencies": ["b"]}
    ]
    assert not DAGScheduler.has_cycles(acyclic)

    # Graph with cycle: a -> b -> c -> a
    cyclic = [
        {"id": "a", "dependencies": ["c"]},
        {"id": "b", "dependencies": ["a"]},
        {"id": "c", "dependencies": ["b"]}
    ]
    assert DAGScheduler.has_cycles(cyclic)
