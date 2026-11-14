"""Trace a seeded CartPole episode without a display or training."""
import argparse
import json
import platform

import gymnasium as gym
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-steps", type=int, default=50)
    args = parser.parse_args()
    if args.max_steps < 1:
        parser.error("--max-steps must be positive")
    env = gym.make("CartPole-v1", max_episode_steps=args.max_steps)
    try:
        print(json.dumps(dict(python=platform.python_version(), gymnasium=gym.__version__,
                              numpy=np.__version__, seed=args.seed, max_steps=args.max_steps)))
        print(f"observation_space={env.observation_space}")
        print(f"action_space={env.action_space}")
        # Seed the environment and the separate action-sampling generator.
        env.action_space.seed(args.seed)
        observation, info = env.reset(seed=args.seed)
        print(json.dumps(dict(event="reset", observation=observation.tolist(), info=info)))
        total_reward = 0.0
        for step in range(1, args.max_steps + 1):
            action = int(env.action_space.sample())
            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += float(reward)
            print(json.dumps(dict(step=step, action=action, observation=observation.tolist(),
                                  reward=float(reward), terminated=bool(terminated),
                                  truncated=bool(truncated), info=info)))
            if terminated or truncated:
                print(json.dumps(dict(event="episode_end", steps=step, total_reward=total_reward,
                                      terminated=bool(terminated), truncated=bool(truncated))))
                break
    finally:
        env.close()


if __name__ == "__main__":
    main()
