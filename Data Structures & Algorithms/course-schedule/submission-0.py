class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        prereqs = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            prereqs[course].append(prereq)
        on_path = set()
        safe = set()

        def dfs(course) -> bool:
            if course in on_path:
                return False
            if course in safe:
                return True
            on_path.add(course)
            for prereq in prereqs[course]:
                if not dfs(prereq):
                    return False
            on_path.remove(course)
            safe.add(course)
            return True

        for course in range(len(prereqs)):
            if not dfs(course):
                return False
        return True