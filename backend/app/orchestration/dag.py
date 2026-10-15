from typing import List, Dict, Set, Any

class DAGScheduler:
    @staticmethod
    def get_ready_subtasks(
        all_subtasks: List[Dict[str, Any]], 
        completed_ids: Set[str]
    ) -> List[Dict[str, Any]]:
        """
        Returns all subtasks whose dependencies have been completely satisfied,
        whose current status is 'pending', and which have not yet completed.
        """
        ready = []
        for st in all_subtasks:
            if st.get("status") == "pending" and st.get("id") not in completed_ids:
                deps = st.get("dependencies", [])
                if all(dep in completed_ids for dep in deps):
                    ready.append(st)
        return ready

    @staticmethod
    def has_cycles(subtasks: List[Dict[str, Any]]) -> bool:
        """
        Detects cycles in the subtask dependency graph using topological sorting / DFS.
        """
        adj = {st["id"]: st.get("dependencies", []) for st in subtasks}
        visited = {}  # 0 = unvisited, 1 = visiting, 2 = visited

        def dfs(node):
            if visited.get(node) == 1:
                return True
            if visited.get(node) == 2:
                return False
            visited[node] = 1
            for parent in adj.get(node, []):
                if dfs(parent):
                    return True
            visited[node] = 2
            return False

        for node in adj:
            if visited.get(node, 0) == 0:
                if dfs(node):
                    return True
        return False
