from sarsa import SARSA
from qlearn import QLearn
from expected_sarsa import ExpectedSARSA
from gridworld import GridWorld
from agent import Agent
from argparse import ArgumentParser
import os
import random
import pickle

def algo_args(parser):
    parser.add_argument('--algo', choices=['qlearn', 'sarsa', 'esarsa'], default='qlearn')



parser = ArgumentParser()
algo_args(parser)
args = parser.parse_args()

for eps in [0.05, 0.2]:
    fname = '{}-{}.csv'.format(args.algo, eps)
    fpath = os.path.join("exps", fname)
    with open(fpath, "w+") as fp:
        total_rewards = 0
        options = {
                "qlearn": lambda: QLearn(eps=eps),
                "sarsa": lambda: SARSA(eps=eps),
                "esarsa": lambda: ExpectedSARSA(eps=eps)
        }      
        algo = options.get(args.algo)()

        for episode in range(10000):
            grid = GridWorld();
            agent = Agent()
            s = agent.position()
            actions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            a = random.choice(actions)
            episode_reward = 0

            def step(s, a):
                s_ = grid.move(s, a)
                agent.position(s_)
                maybe_a = algo.choose(s_)
                a_ = agent.move(maybe_a)
                r = agent.reward(grid)
                algo.update(s, a, r, s_, a_)
                return (s_, a_, r)

            steps = 0
            while s != grid.goal:
                #print((s, a), "->", end='')
                s, a, r = step(s, a)
                episode_reward += r
                steps += 1
                #print((s, a), "Reward:", r)
            #print((s, a), "->", end='')
            # s, a, r = step(s, a)
            # episode_reward += r
            #print((s, a), "Reward:", r)

            total_rewards += episode_reward
            values = [eps, episode, episode_reward, total_rewards, total_rewards/(episode+1), steps]
            print(','.join(map(str, values)), file=fp)
    policy_fname = '{}-{}.policy'.format(args.algo, eps)
    pfpath = os.path.join("exps", policy_fname)
    with open(pfpath, "wb+") as ofp:
        pickle.dump(algo.policy(), ofp)

    value_fname = '{}-{}.value'.format(args.algo, eps)
    vfpath = os.path.join("exps", value_fname)
    with open(vfpath, "wb+") as ofp:
        pickle.dump(algo.value(), ofp)
