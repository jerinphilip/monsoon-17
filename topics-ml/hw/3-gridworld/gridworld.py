def GridWorld():
    grid = lambda t: t
    start, bad, goal = (1, 0), (2, 1), (3, 3)

    def legal_state(state):
        x, y = state
        bounded = lambda t: 0 <= t and t < 4
        return (bounded(x) and bounded(y))

    def legal_action(action):
        x, y = action
        return (abs(x + y) == 1 and x*y == 0)

    def move(state, action):
        x, y = state
        dx, dy = action
        if state == goal:
            return state

        if not legal_action(action):
            return state

        candidate = (x+dx, y+dy)
        if legal_state(candidate):
            return candidate
        return state

    setattr(grid, 'move', move)
    setattr(grid, 'start', start)
    setattr(grid, 'goal', goal)
    setattr(grid, 'bad', bad)

    return grid


if __name__ == '__main__':
    grid = GridWorld();
    for i in [1, -1]:
        def attempt(state, move):
            state_ = grid.move(state, move)
            print(state, "->", state_)

        attempt((0, 0), (0, i))
        attempt((0, 0), (i, 0))
        attempt((1, 1), (0, i))
        attempt((1, 1), (i, 0))
        attempt((3, 3), (0, i))
        attempt((3, 3), (i, 0))

