import numpy as np
from collections import defaultdict, Counter

import gym
env = gym.make("Blackjack-v0")
observation = env.reset()

boxes = {}

box_actions = {}

for _ in range(10000):
    hand_sum = env._get_obs()[0]

    if not hand_sum in boxes:
        boxes[hand_sum] = [True, False]
    if not hand_sum in box_actions:
        box_actions[hand_sum] = []

    # True => Hit
    # False => Stay

    action = np.random.choice(boxes[hand_sum])
    box_actions[hand_sum].append(action)

    observation, reward, done, _ = env.step(action)
    
    if done:
        if reward > 0:
            for box in box_actions:
                boxes[box].extend(box_actions[box])
        elif reward < 0:
            for box in box_actions:
                for a in box_actions[box]:
                    if Counter(boxes[box])[a] > 1:
                        boxes[box].remove(a)
        box_actions = {}
        env.reset()
    # observation = (hand sum, exposed dealer card, has usable ace?)

for key in sorted(boxes):
    count = Counter(boxes[key])
    output = str(key) + ' => '
    output += 'hit/stay: ' + str(count[True])
    output += '/' + str(count[False])
    #print(output)

x = int(input("Hand Sum:"))

while x != -1:
    if x in boxes:
        hit = np.random.choice(boxes[x])
        if hit:
            print("Computer chooses...Hit")
        else:
            print("Computer chooses...Stay")
        count = Counter(boxes[x])
        hit = int(count[True])
        stay = int(count[False])
        print("Ratio was", str(hit) + ":" + str(stay), "(hit:stay)")
    x = int(input("Hand Sum:"))
