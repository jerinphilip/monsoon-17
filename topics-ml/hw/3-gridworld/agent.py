import numpy as np

def Agent(**kwargs):
    _agent = lambda t: t
    _params = {
        "a": 0.9,
        "b": 0.05,
        "position": (0, 0)
    }

    _params.update(kwargs)

    def position(state=None):
        if state is None:
            return _params["position"]
        _params["position"] = state

    def move(action):
        x, y = action
        laterals = [(y, x), (-y, -x)]
        possible = [action] + laterals
        probs    = [_params["a"], _params["b"], _params["b"]]
        index = np.random.choice(len(possible), p=probs)
        return possible[index]

    def reward(env):
        _reward = {
            env.goal: 100,
            env.bad: -70
        }
        return _reward.get(_params["position"], -1)

    setattr(_agent, 'move', move)
    setattr(_agent, 'position', position)
    setattr(_agent, 'reward', reward)
    return _agent

if __name__ == '__main__':
    agent = Agent()
    for x in range(1000):
        print (agent.move((0, -1)))
