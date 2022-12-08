import sys


class BinaryMaze:
    """
    A Binary Maze class with the following functions:
        is_valid(self, m, n)
        is_valid_backtracking(self, m, n)
        bfs_enqueue(self, m, n)
        add_to_path(self, m, n, direction)
        bfs(self, source, destination)
        backtrack(self, current_node)
        write_path(self, source, destination)
        cleanup(self)
        solve_puzzle(self, source, destination)
    """

    def __init__(self, board):
        """
        :param board:
        """
        self._board = board
        self._distance_from_source = 0
        self._min_distance = sys.maxsize
        self._board_rows = len(board)
        self._board_cols = len(board[0])
        # Stores the path to return.
        self._path = []
        self._path_tuple = ()
        self._path_string = ''
        self._possible_path = []
        # Creates a queue for BFS operations.
        self._queue = []
        # Stores the indexes visited and their distance from self._source.
        self._visited = [[(False, -1)] * self._board_cols for i in range(self._board_rows)]
        self._deadends = [[False] * self._board_cols for i in range(self._board_rows)]

    def is_valid(self, m, n):
        """
        :param m:
        :param n:
        :return:
        """
        if m <= -1 or m >= self._board_rows or n <= -1 or n >= self._board_cols or not self._board[m][
                n] or not self._board[m][n] == '-' or self._visited[m][n][0]:
            return False
        else:
            return True

    def is_valid_backtracking(self, m, n):
        """
        :param m:
        :param n:
        :return:
        """
        if m <= -1 or m >= self._board_rows or n <= -1 or n >= self._board_cols or self._visited[m][n][
                1] != self._distance_from_source or self._deadends[m][n]:
            return False
        else:
            return True

    def bfs_enqueue(self, m, n):
        """
        :param m:
        :param n:
        :return:
        """
        self._visited[m][n] = (True, self._distance_from_source + 1)
        queue_tuple = (m, n)
        self._queue.append(queue_tuple)

    def add_to_path(self, m, n, direction):
        """
        :param m:
        :param n:
        :param direction:
        :return:
        """
        current_node = (m, n)
        self._possible_path.append(current_node)
        self._path_string += direction
        self._distance_from_source += 1
        return current_node

    def bfs(self, source, destination):
        """
        :return:
        Time Complexity: O(V + E)
        """
        self._path_tuple = source

        # Get all adjacent vertices. If an adjacent has not been visited, then push it
        # to the queue.
        while self._queue:
            # Pop first vertex from queue.
            s = self._queue.pop(0)
            m = s[0]
            n = s[1]
            self._path_tuple = (m, n)
            self._distance_from_source = self._visited[m][n][1]

            # If we reached our destination.
            if self._path_tuple == destination:
                self._min_distance = self._distance_from_source
                self._visited[m][n] = (True, self._distance_from_source)
                break

            # Check for edge up.
            up = self.is_valid(m - 1, n)
            if up:
                self.bfs_enqueue(m - 1, n)
            # Check for edge down.
            down = self.is_valid(m + 1, n)
            if down:
                self.bfs_enqueue(m + 1, n)
            # Check for edge left.
            left = self.is_valid(m, n - 1)
            if left:
                self.bfs_enqueue(m, n - 1)
            # Check for edge right.
            right = self.is_valid(m, n + 1)
            if right:
                self.bfs_enqueue(m, n + 1)

    def backtrack(self, current_node):
        """
        :return:
        """
        if self._possible_path:
            self._possible_path.pop()
        self._path_string = self._path_string[:-1]
        self._distance_from_source -= 1
        m = current_node[0]
        n = current_node[1]
        self._deadends[m][n] = True
        if self._possible_path:
            current_node = self._possible_path[-1]
        m = current_node[0]
        n = current_node[1]

        return m, n

    def write_path(self, source, destination):
        """
        :param source:
        :param destination:
        :return:
        Time Complexity: O(m * n)!
        """
        self._possible_path.append(source)
        current_node = source
        m = current_node[0]
        n = current_node[1]
        self._distance_from_source = 1

        # Greedily choose next min distance and see if we reach destination with this path.
        while current_node != destination:
            while self._distance_from_source <= self._min_distance:
                # Check for edge up.
                up = self.is_valid_backtracking(m - 1, n)
                if up:
                    current_node = self.add_to_path(m - 1, n, 'U')
                    m = current_node[0]
                    n = current_node[1]
                    continue
                # Check for edge down.
                down = self.is_valid_backtracking(m + 1, n)
                if down:
                    current_node = self.add_to_path(m + 1, n, 'D')
                    m = current_node[0]
                    n = current_node[1]
                    continue

                # Check for edge left.
                left = self.is_valid_backtracking(m, n - 1)
                if left:
                    current_node = self.add_to_path(m, n - 1, 'L')
                    m = current_node[0]
                    n = current_node[1]
                    continue

                # Check for edge right.
                right = self.is_valid_backtracking(m, n + 1)
                if right:
                    current_node = self.add_to_path(m, n + 1, 'R')
                    m = current_node[0]
                    n = current_node[1]
                    continue

                # If we reached this far it means no options were valid.
                current_node = self.backtrack(current_node)
                m = current_node[0]
                n = current_node[1]

            # Our path reached min_length.
            if current_node == destination:
                final_path = (self._possible_path, self._path_string)
                self._path.append(final_path)

            # Backtrack, marking that index as a dead-end so it won't try it again.
            else:
                current_node = self.backtrack(current_node)
                m = current_node[0]
                n = current_node[1]

    def cleanup(self):
        """
        :return:
        """
        self._distance_from_source = 0
        self._min_distance = sys.maxsize
        self._path = []
        self._path_tuple = ()
        self._path_string = ''
        self._possible_path = []
        # Creates a queue for BFS operations.
        self._queue = []
        # Stores the indexes visited and their distance from self._source.
        self._visited = [[(False, -1)] * self._board_cols for i in range(self._board_rows)]
        self._deadends = [[False] * self._board_cols for i in range(self._board_rows)]

    def solve_puzzle(self, source, destination):
        """
        :param source:
        :param destination:
        :return:
        """

        if source == destination:
            self._path.append(source)
            return self._path

        # Mark the source node as visited and update its distance to 0.
        m = source[0]
        n = source[1]
        self._visited[m][n] = (True, 0)

        # Perform BFS operations and fill out distances to each node from source.
        # Add source to the queue.
        self._queue.append(source)
        self.bfs(source, destination)

        # If we have reached our destination, backtrack and find the nodes that make up the min_path to the destination.
        if self._path_tuple == destination:
            self.write_path(source, destination)
            result = self._path
            self.cleanup()
            return result

        # Destination is unreachable.
        else:
            self.cleanup()
            return None


if __name__ == "__main__":

    Puzzle = [
        ['-', '-', '-', '-', '-'],
        ['-', '-', '#', '-', '-'],
        ['-', '-', '-', '-', '-'],
        ['#', '-', '#', '#', '-'],
        ['-', '#', '-', '-', '-']
    ]

    my_maze1 = BinaryMaze(Puzzle)
    print(my_maze1.solve_puzzle((0, 2), (2, 2)))
    print(my_maze1.solve_puzzle((0, 0), (4, 0)))
    print(my_maze1.solve_puzzle((0, 0), (4, 4)))
    print(my_maze1.solve_puzzle((4, 4), (0, 0)))

    Puzzle2 = [
        ['-', '-', '-', '-'],
        ['-', '-', '#', '-'],
        ['-', '-', '-', '-'],
        ['#', '-', '#', '-'],
        ['-', '#', '-', '-']
    ]

    my_maze2 = BinaryMaze(Puzzle2)
    print(my_maze2.solve_puzzle((0, 0), (4, 3)))
    print(my_maze2.solve_puzzle((0, 0), (1, 0)))

    Puzzle3 = [
        ['-', '-', '-', '-', '-'],
        ['-', '-', '#', '-', '-'],
        ['-', '-', '-', '-', '-'],
        ['#', '-', '#', '#', '-']
    ]

    my_maze3 = BinaryMaze(Puzzle3)
    print(my_maze3.solve_puzzle((0, 0), (3, 4)))

    Puzzle4 = [
        ['-', '-', '-', '-'],
        ['-', '-', '#', '-'],
        ['-', '-', '-', '-']
    ]

    my_maze4 = BinaryMaze(Puzzle)
    print(my_maze4.solve_puzzle((0, 0), (2, 3)))

    Puzzle5 = [
        ['-', '-', '-'],
        ['-', '-', '#'],
        ['-', '-', '-'],
        ['#', '-', '-']
    ]
    my_maze5 = BinaryMaze(Puzzle5)
    print(my_maze1.solve_puzzle((1, 1), (1, 1)))
