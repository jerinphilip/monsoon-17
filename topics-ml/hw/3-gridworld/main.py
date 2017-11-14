from sarsa import SARSA
from gridworld import GridWorld
from agent import Agent

grid = GridWorld();
agent = Agent()
sarsa = SARSA()

s = agent.position()
a = (0, 1)

while s != grid.goal:
    def step(s, a):
        maybe_a = sarsa.choose(s)
        a_ = agent.move(maybe_a)
        s_ = grid.move(s, a_)
        agent.position(s_)
        r = agent.reward(grid)
        print(s, a, r, s_, a_)
        return (s_, a_)
    s, a = step(s, a)
step(s, a)
