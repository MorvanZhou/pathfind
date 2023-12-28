import time

import pathfind

m = [[2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2], [1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2],
     [1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2], [2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1],
     [1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1], [2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2],
     [2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1], [1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2],
     [2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1], [1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
     [1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1], [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
     [2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1], [1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1],
     [1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2]]

g = pathfind.transform.matrix2graph(m)
for method in [
    "a*",
    "bfs",
    "greedy",
    "dijkstra",
    "dfs",
    "d*lite",
    "jps"
]:
    ts = []
    for i in range(100):
        t0 = time.time()
        for j in range(15):
            pathfind.find(g, "7,7", "14,14", method=method)
        t1 = time.time()
        ts.append(t1 - t0)
    print(f"{method}: min={min(ts):.4f}, mean={sum(ts) / len(ts):.4f}")

"""
a*: min=0.0068, mean=0.0062
bfs: min=0.0217, mean=0.0201
greedy: min=0.0011, mean=0.0010
dijkstra: min=0.0288, mean=0.0261
dfs: min=0.0009, mean=0.0008
d*lite: min=0.0165, mean=0.0150
jps: min=0.0054, mean=0.0051
"""

"""
把 append 提出来
a*: min=0.0067, mean=0.0062
bfs: min=0.0206, mean=0.0195
greedy: min=0.0011, mean=0.0010
dijkstra: min=0.0269, mean=0.0257
dfs: min=0.0008, mean=0.0007
d*lite: min=0.0158, mean=0.0150
jps: min=0.0055, mean=0.0051
"""

"""
改成 deque 取代 for loop 迭代器
bfs: min=0.0192, mean=0.0195
dfs: min=0.0007, mean=0.0008
"""

"""
iter_explore 中，如果不是 return_cost，就不要返回 cost 了,也不更新 new_g 相关的数值
n = neighbor.node 移动到 continue 后面

a*: min=0.0042, mean=0.0043
bfs: min=0.0061, mean=0.0062
greedy: min=0.0009, mean=0.0009
dijkstra: min=0.0118, mean=0.0120
dfs: min=0.0005, mean=0.0005
d*lite: min=0.0131, mean=0.0134
jps: min=0.0050, mean=0.0052
"""

"""
check_neighbors 中，将类函数 is_visited(self, n) 和 set_g(self, g) 换成直接执行，减少引用

a*: min=0.0039, mean=0.0041
bfs: min=0.0053, mean=0.0054
greedy: min=0.0009, mean=0.0009
dijkstra: min=0.0108, mean=0.0110
dfs: min=0.0004, mean=0.0005
d*lite: min=0.0129, mean=0.0131
jps: min=0.0051, mean=0.0052
"""

"""
finder 中，将类函数 successors(self, n) 和 predecessors(self, n) 换成直接执行，减少类引用

a*: min=0.0038, mean=0.0039
bfs: min=0.0046, mean=0.0048
greedy: min=0.0008, mean=0.0009
dijkstra: min=0.0102, mean=0.0104
dfs: min=0.0004, mean=0.0004
d*lite: min=0.0128, mean=0.0131
jps: min=0.0051, mean=0.0052
"""

"""
self.g(n) 换成了 self._g[n.name]，减少了一次函数调用

a*: min=0.0034, mean=0.0034
bfs: min=0.0046, mean=0.0047
greedy: min=0.0008, mean=0.0009
dijkstra: min=0.0088, mean=0.0089
dfs: min=0.0004, mean=0.0004
d*lite: min=0.0119, mean=0.0121
jps: min=0.0051, mean=0.0052
"""

"""
tool 里面计算距离，都用 map 来 for

a*: min=0.0033, mean=0.0033
bfs: min=0.0046, mean=0.0047
greedy: min=0.0008, mean=0.0009
dijkstra: min=0.0086, mean=0.0088
dfs: min=0.0004, mean=0.0004
d*lite: min=0.0113, mean=0.0115
jps: min=0.0051, mean=0.0051
"""

"""
最后对比

a*: 0.0033 / 0.0068 = 0.48
bfs: 0.0046 / 0.0217 = 0.2
greedy: 0.0008 / 0.0011 = 0.72
dijkstra: 0.0086 / 0.0288 = 0.3
dfs: 0.0004 / 0.0009 = 0.44
d*lite: 0.0113 / 0.0165 = 0.68
jps: 0.0051 / 0.0054 = 0.94
"""
