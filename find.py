import pygame
import numpy as np
from collections import deque
import heapq

pygame.init()


def make_odd(n: int) -> int:
    return n if n % 2 == 1 else n - 1


class MazeVisualizer:
    def __init__(
        self,
        maze_height=81,               # rows in cells (odd). cols auto to ~16:9
        fullscreen=True,
        slow_ratio=0.55,              # reduce orange: try 0.45–0.60
        wall_prob=0.72,               # increase black walls: try 0.68–0.80
        hud_height=80                 # top padding for text
    ):
        self.fullscreen = fullscreen
        self.slow_ratio = float(slow_ratio)
        self.wall_prob = float(wall_prob)
        self.hud_h = int(hud_height)

        # 16:9 maze aspect ratio in cells
        self.maze_rows = make_odd(int(maze_height))
        self.maze_cols = make_odd(int(round(self.maze_rows * 16 / 9)))

        flags = pygame.SCALED
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
            info = pygame.display.Info()
            size = (info.current_w, info.current_h)  # must be non-zero with SCALED
        else:
            size = (1280, 720)

        self.screen = pygame.display.set_mode(size, flags)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Pathfinding Algorithm Visualizer")

        # Compute cell size to fit maze below HUD
        usable_h = max(1, self.height - self.hud_h)
        self.cell_size = min(self.width // self.maze_cols, usable_h // self.maze_rows)

        self.maze_px_w = self.cell_size * self.maze_cols
        self.maze_px_h = self.cell_size * self.maze_rows

        self.off_x = (self.width - self.maze_px_w) // 2
        self.off_y = self.hud_h + (usable_h - self.maze_px_h) // 2

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (100, 150, 255)
        self.BLUE_SLOW = (80, 120, 200)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (200, 100, 255)
        self.PURPLE_SLOW = (140, 70, 190)
        self.ORANGE = (255, 220, 0)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Fira Sans", 48)

        self.start = (1, 1)
        self.goal = (self.maze_rows - 2, self.maze_cols - 2)

        self.maze = self.generate_maze()
        self.build_static_surface()
        self.reset_frame()

    # ---------- Maze generation (dense, solvable, 16:9) ----------

    def generate_maze(self):
        rows, cols = self.maze_rows, self.maze_cols
        maze = np.ones((rows, cols), dtype=np.uint8)
        weights = np.ones((rows, cols), dtype=np.uint8)

        start = self.start
        goal = self.goal

        # Carve a guaranteed path (randomized DFS tunnels)
        stack = [start]
        maze[start] = 0
        path_cells = {start}

        while stack:
            x, y = stack[-1]
            if (x, y) == goal:
                break

            candidates = []
            for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and maze[nx, ny] == 1:
                    candidates.append((nx, ny))

            if candidates:
                nx, ny = candidates[np.random.randint(len(candidates))]
                mid = ((x + nx) // 2, (y + ny) // 2)
                maze[mid] = 0
                maze[nx, ny] = 0
                path_cells.add(mid)
                path_cells.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # Fill remaining cells with lots of walls, but NEVER overwrite path_cells
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if (i, j) in path_cells:
                    continue
                maze[i, j] = 1 if (np.random.rand() < self.wall_prob) else 0

        # Ensure start/goal open
        maze[start] = 0
        maze[goal] = 0

        # Terrain weights (orange tiles) on walkable cells
        np.random.seed(43)
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if maze[i, j] == 0:
                    weights[i, j] = 5 if (np.random.rand() < self.slow_ratio) else 1

        weights[start] = 1
        weights[goal] = 1

        self.weights = weights
        return maze

    # ---------- Fast drawing (static cache + solid fills, no outlines) ----------

    def build_static_surface(self):
        """Cache background (walls + slow tiles) once."""
        self.static_surf = pygame.Surface((self.width, self.height))
        self.static_surf.fill(self.WHITE)
        pygame.draw.rect(self.static_surf, self.WHITE, (0, 0, self.width, self.hud_h))

        for i in range(self.maze_rows):
            for j in range(self.maze_cols):
                x = self.off_x + j * self.cell_size
                y = self.off_y + i * self.cell_size
                r = (x, y, self.cell_size, self.cell_size)

                if self.maze[i, j] == 1:
                    pygame.draw.rect(self.static_surf, self.BLACK, r)
                elif self.weights[i, j] > 1:
                    pygame.draw.rect(self.static_surf, self.ORANGE, r)

    def reset_frame(self):
        """Blit cached background and draw start/goal."""
        self.screen.blit(self.static_surf, (0, 0))
        self.draw_cell(self.start, self.GREEN)
        self.draw_cell(self.goal, self.RED)
        pygame.display.flip()

    def cell_rect(self, pos):
        x = self.off_x + pos[1] * self.cell_size
        y = self.off_y + pos[0] * self.cell_size
        return (x, y, self.cell_size, self.cell_size)

    def draw_cell(self, pos, color):
        pygame.draw.rect(self.screen, color, self.cell_rect(pos))

    def draw_text(self, text, pos):
        surf = self.font.render(text, True, self.BLACK)
        self.screen.blit(surf, pos)

    def draw_hud(self, algo_name, visited_count, cost=None, elapsed_s=None, extra=None):
        # Clear HUD strip
        self.screen.blit(self.static_surf, (0, 0), (0, 0, self.width, self.hud_h))

        parts = [algo_name, f"Visited: {visited_count}"]
        if elapsed_s is not None:
            parts.append(f"Time: {elapsed_s:.3f}s")
        if cost is not None:
            parts.append(f"Cost: {cost}")
        if extra:
            parts.append(extra)

        sp = " " * 8
        self.draw_text(sp.join(parts), (10, 10))

    # ---------- Helpers ----------

    def handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        return False

    def wait_for_keypress(self):
        """Block until any key press (or quit/ESC)."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    return True
            self.clock.tick(60)

    def get_neighbors(self, pos):
        x, y = pos
        out = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze_rows and 0 <= ny < self.maze_cols and self.maze[nx, ny] == 0:
                out.append((nx, ny))
        return out

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def path_cost(self, path):
        if not path:
            return 0
        return int(sum(self.weights[p[0], p[1]] for p in path[1:]))

    def fps_from_delay(self, delay_ms):
        # delay_ms used as a speed knob: smaller => higher FPS cap
        if delay_ms is None:
            return 0
        delay_ms = int(delay_ms)
        if delay_ms <= 0:
            return 0
        return min(1000, max(30, 1000 // delay_ms))

    # ---------- Algorithms (incremental drawing + realtime timer) ----------

    def bfs(self, visualize=True, delay=1):
        start_ms = pygame.time.get_ticks()
        q = deque([self.start])
        prev = {self.start: None}
        visited = set([self.start])

        last_current = None
        fps = self.fps_from_delay(delay)

        while q:
            if self.handle_quit():
                return None, len(visited), 0, (pygame.time.get_ticks() - start_ms) / 1000.0

            current = q.popleft()

            if visualize:
                if last_current and last_current != self.start and last_current != self.goal:
                    color = self.BLUE_SLOW if self.weights[last_current[0], last_current[1]] > 1 else self.BLUE
                    self.draw_cell(last_current, color)

                if current != self.start and current != self.goal:
                    self.draw_cell(current, self.YELLOW)

                self.draw_cell(self.start, self.GREEN)
                self.draw_cell(self.goal, self.RED)

                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                self.draw_hud("Breadth-First Search", len(visited), elapsed_s=elapsed_s)
                pygame.display.update()

                if fps:
                    self.clock.tick(fps)

                last_current = current

            if current == self.goal:
                path = []
                cur = current
                while cur is not None:
                    path.append(cur)
                    cur = prev[cur]
                path.reverse()
                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                return path, len(visited), self.path_cost(path), elapsed_s

            for n in self.get_neighbors(current):
                if n not in visited:
                    visited.add(n)
                    prev[n] = current
                    q.append(n)

        elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
        return None, len(visited), 0, elapsed_s

    def dfs(self, visualize=True, delay=1):
        start_ms = pygame.time.get_ticks()
        stack = [self.start]
        prev = {self.start: None}
        visited = set()

        last_current = None
        fps = self.fps_from_delay(delay)

        while stack:
            if self.handle_quit():
                return None, len(visited), 0, (pygame.time.get_ticks() - start_ms) / 1000.0

            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            if visualize:
                if last_current and last_current != self.start and last_current != self.goal:
                    color = self.BLUE_SLOW if self.weights[last_current[0], last_current[1]] > 1 else self.BLUE
                    self.draw_cell(last_current, color)

                if current != self.start and current != self.goal:
                    self.draw_cell(current, self.YELLOW)

                self.draw_cell(self.start, self.GREEN)
                self.draw_cell(self.goal, self.RED)

                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                self.draw_hud("DFS", len(visited), elapsed_s=elapsed_s)
                pygame.display.update()

                if fps:
                    self.clock.tick(fps)

                last_current = current

            if current == self.goal:
                path = []
                cur = current
                while cur is not None:
                    path.append(cur)
                    cur = prev[cur]
                path.reverse()
                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                return path, len(visited), self.path_cost(path), elapsed_s

            for n in self.get_neighbors(current):
                if n not in visited:
                    if n not in prev:
                        prev[n] = current
                    stack.append(n)

        elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
        return None, len(visited), 0, elapsed_s

    def dijkstra(self, visualize=True, delay=1):
        start_ms = pygame.time.get_ticks()
        dist = {self.start: 0}
        prev = {}
        pq = [(0, self.start)]
        visited = set()

        last_current = None
        fps = self.fps_from_delay(delay)

        while pq:
            if self.handle_quit():
                return None, len(visited), 0, (pygame.time.get_ticks() - start_ms) / 1000.0

            d, current = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)

            if visualize:
                if last_current and last_current != self.start and last_current != self.goal:
                    color = self.BLUE_SLOW if self.weights[last_current[0], last_current[1]] > 1 else self.BLUE
                    self.draw_cell(last_current, color)

                if current != self.start and current != self.goal:
                    self.draw_cell(current, self.YELLOW)

                self.draw_cell(self.start, self.GREEN)
                self.draw_cell(self.goal, self.RED)

                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                self.draw_hud("Dijkstra", len(visited), cost=d, elapsed_s=elapsed_s)
                pygame.display.update()

                if fps:
                    self.clock.tick(fps)

                last_current = current

            if current == self.goal:
                path = []
                cur = current
                while cur != self.start:
                    path.append(cur)
                    cur = prev[cur]
                path.append(self.start)
                path.reverse()
                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                return path, len(visited), int(d), elapsed_s

            for n in self.get_neighbors(current):
                nd = d + int(self.weights[n[0], n[1]])
                if n not in dist or nd < dist[n]:
                    dist[n] = nd
                    prev[n] = current
                    heapq.heappush(pq, (nd, n))

        elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
        return None, len(visited), 0, elapsed_s

    def astar(self, visualize=True, delay=1):
        # Optimized A* with array g-scores + tie-break toward goal
        start_ms = pygame.time.get_ticks()

        rows, cols = self.maze_rows, self.maze_cols
        INF = 1e18
        g = np.full((rows, cols), INF, dtype=np.float64)
        px = np.full((rows, cols), -1, dtype=np.int32)
        py = np.full((rows, cols), -1, dtype=np.int32)
        closed = np.zeros((rows, cols), dtype=bool)

        sx, sy = self.start
        gx, gy = self.goal
        g[sx, sy] = 0.0

        # 1.0 = optimal (admissible). Increase (1.2–1.5) if you prefer fewer visited nodes.
        heur_w = 1.5

        def h(x, y):
            return abs(x - gx) + abs(y - gy)

        counter = 0
        open_heap = []
        h0 = h(sx, sy)
        heapq.heappush(open_heap, (h0, h0, counter, (sx, sy)))

        visited_count = 0
        last_current = None
        fps = self.fps_from_delay(delay)

        while open_heap:
            if self.handle_quit():
                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                return None, visited_count, 0, elapsed_s

            _, _, _, (x, y) = heapq.heappop(open_heap)
            if closed[x, y]:
                continue

            closed[x, y] = True
            visited_count += 1

            if visualize:
                cur = (x, y)

                if last_current and last_current != self.start and last_current != self.goal:
                    color = self.BLUE_SLOW if self.weights[last_current[0], last_current[1]] > 1 else self.BLUE
                    self.draw_cell(last_current, color)

                if cur != self.start and cur != self.goal:
                    self.draw_cell(cur, self.YELLOW)

                self.draw_cell(self.start, self.GREEN)
                self.draw_cell(self.goal, self.RED)

                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                self.draw_hud("A*", visited_count, cost=int(g[x, y]), elapsed_s=elapsed_s)
                pygame.display.update()

                if fps:
                    self.clock.tick(fps)

                last_current = cur

            if (x, y) == (gx, gy):
                path = []
                cx, cy = gx, gy
                while not (cx == sx and cy == sy):
                    path.append((cx, cy))
                    nx, ny = px[cx, cy], py[cx, cy]
                    cx, cy = nx, ny
                path.append((sx, sy))
                path.reverse()
                elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
                return path, visited_count, int(g[gx, gy]), elapsed_s

            gcur = g[x, y]
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
                    continue
                if self.maze[nx, ny] == 1 or closed[nx, ny]:
                    continue

                ng = gcur + float(self.weights[nx, ny])
                if ng < g[nx, ny]:
                    g[nx, ny] = ng
                    px[nx, ny] = x
                    py[nx, ny] = y

                    hn = h(nx, ny)
                    counter += 1
                    f = ng + heur_w * hn
                    # secondary key hn => better tie-break, pulls toward goal
                    heapq.heappush(open_heap, (f, hn, counter, (nx, ny)))

        elapsed_s = (pygame.time.get_ticks() - start_ms) / 1000.0
        return None, visited_count, 0, elapsed_s

    # ---------- Final path visualization (keep stats until keypress) ----------

    def show_final(self, algo_name, path, visited_count, cost, elapsed_s):
        if not path:
            return False

        self.reset_frame()

        for p in path:
            if p != self.start and p != self.goal:
                self.draw_cell(p, self.PURPLE_SLOW if self.weights[p[0], p[1]] > 1 else self.PURPLE)

        self.draw_cell(self.start, self.GREEN)
        self.draw_cell(self.goal, self.RED)

        extra = f"Path: {len(path)}"
        self.draw_hud(algo_name, elapsed_s=elapsed_s, visited_count=visited_count, cost=cost, extra=extra)
        pygame.display.flip()

        return self.wait_for_keypress()

    # ---------- Runner ----------

    def run_algorithm(self, name, delay=1):
        self.reset_frame()

        if name == "bfs":
            path, visited, cost, elapsed_s = self.bfs(visualize=True, delay=delay)
            label = "Breadth-First Search"
        elif name == "dfs":
            path, visited, cost, elapsed_s = self.dfs(visualize=True, delay=delay)
            label = "Depth-First Search"
        elif name == "dijkstra":
            path, visited, cost, elapsed_s = self.dijkstra(visualize=True, delay=delay)
            label = "Dijkstra's Algorithm"
        elif name == "astar":
            path, visited, cost, elapsed_s = self.astar(visualize=True, delay=delay)
            label = "A* Algorithm"
        else:
            path, visited, cost, elapsed_s = self.bfs(visualize=True, delay=delay)
            label = "Breadth-First Search"

        if path:
            cont = self.show_final(label, path, visited, cost, elapsed_s)
            if not cont:
                return None

        return path

    def compare_all(self, delay=1):
        for algo in ["bfs", "dfs", "dijkstra", "astar"]:
            out = self.run_algorithm(algo, delay=delay)
            if out is None:
                return

    def close(self):
        pygame.quit()


if __name__ == "__main__":
    visualizer = MazeVisualizer(
        maze_height=50,
        fullscreen=True,
        slow_ratio=0.2,   # fewer orange
        wall_prob=0.3,    # lots of black walls
        hud_height=80      # more top padding for text
    )

    # delay is a speed knob (FPS cap). delay=1 fast; delay=0 uncapped.
    visualizer.compare_all(delay=1)
    visualizer.close()
