import numpy as np
from collections import defaultdict, Counter

import gym
env = gym.make("Blackjack-v0")
observation = env.reset()

boxes = {}

box_actions = {}

n = int(input("Iterations to train (n): "))

for _ in range(n):
    hand_sum = env._get_obs()[0]

    if not hand_sum in boxes:
        boxes[hand_sum] = { 'hit': 5, 'stay': 5 }
    if not hand_sum in box_actions:
        box_actions[hand_sum] = { 'hit': 0, 'stay': 0 }

    # True => Hit
    # False => Stay

    action = np.random.choice(['hit', 'stay'], 1, [boxes[hand_sum]['hit'], boxes[hand_sum]['stay']])[0]
    box_actions[hand_sum][action] += 1

    observation, reward, done, _ = env.step(True if action == 'hit' else False)
    
    if done:
        if reward >= 0:
            for hand_sum in box_actions:
                boxes[hand_sum]['hit'] += box_actions[hand_sum]['hit']
                boxes[hand_sum]['stay'] += box_actions[hand_sum]['stay']
        elif reward < 0:
            box_actions[hand_sum][action] -= 1
        box_actions = {}
        env.reset()
    # observation = (hand sum, exposed dealer card, has usable ace?)

for box in sorted(boxes):
    box_num = str(box)
    box = boxes[box]
    print(box_num, "=>", box['hit'], box['stay'], "(hit|stay)")

"""
hand_sum = int(input("Hand Sum:"))

while hand_sum != -1:
    if hand_sum in boxes:
        action = np.random.choice(['hit', 'stay'], 1, [boxes[hand_sum]['hit'], boxes[hand_sum]['stay']])[0]
        if action == 'hit':
            print("Computer chooses...Hit")
        else:
            print("Computer chooses...Stay")
        print("Ratio was", str(boxes[hand_sum]['hit']) + ":" + str(boxes[hand_sum]['stay']), "(hit:stay)")
    hand_sum = int(input("Hand Sum:"))
"""
