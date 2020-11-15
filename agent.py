import pygame
from snake import Snake
from pygame.locals import *
import random
import numpy as np

CELL_SIZE = 50
width = 500
height = 500
directions = ["UP", "DOWN", "LEFT", "RIGHT"]


class Agent():
    def __init__(self, snake, states, actions, epsilon, gamma, alpha, Q):
        self.snake = snake
        self.grid_dims = snake.ENV_HEIGHT / CELL_SIZE
        self.epsilon = epsilon
        self.Q = Q
        self.s = (0, float("inf"))
        self.r = 0
        self.a = 0
        self.s_prime = (0, float("inf"))
        self.gamma = gamma
        self.alpha = alpha
        self.num_states = states
        self.num_actions = actions

    def legalAction(self, curr_dir, action):
        if curr_dir == "UP" and action == "DOWN":
            return False
        if curr_dir == "DOWN" and action == "UP":
            return False
        if curr_dir == "RIGHT" and action == "LEFT":
           return False
        if curr_dir == "LEFT" and action == "RIGHT":
            return False
        return True
    
    
    def takeAction(self):
        if np.random.rand() < self.epsilon: ##choose random action

            action = random.choice(directions)
            curr_dir = self.snake.getDirection()

            while not self.legalAction(curr_dir, action): ##if the action isn't valid, choose another
                action = random.choice(directions)

            self.snake.updateDirection(action)
            self.a = self.dir_to_num(action)
            #print(action)

        else: ##choose greedy action
            options = self.Q[self.s[0]]
            act_num = np.argmax(options)
            action = self.num_to_dir(act_num)
            curr_dir = self.snake.getDirection()

            if not self.legalAction(curr_dir, action): ##if action isn't valid, choose the next best action
                valid_opts = {}
                for i in range(len(options)):
                    act_word = self.num_to_dir(i)
                    if self.legalAction(curr_dir, act_word):
                        valid_opts[i] = options[i]
                    
                best_val = float("-inf")
                best_act = 0
                for opt_num in valid_opts:
                    if valid_opts[opt_num] > best_val:
                        best_val, best_act = valid_opts[opt_num], opt_num
                act_num = best_act
                action = self.num_to_dir(act_num)

                    
            self.a = act_num              
            self.snake.updateDirection(action)
            #print(action)




    def make_state(self):
        old = self.snake.getState()
        dir_num = self.dir_to_num(old[2])

        quad_num = self.apple_quad(old[1], old[0][0])
        obs = self.get_obstacles(old[0][0])
        state_list = [quad_num] + obs
        state_tup = tuple(state_list)
        num = np.ravel_multi_index(state_tup, (4, 2, 2, 2, 2))
        #print(num)
        return num

    def get_obstacles(self, head):
        obs = [0, 0, 0, 0] #list of if obstacles are present up, right, down, left
        if head[1] == 0:
            obs[0] = 1
        if head[0] == self.snake.ENV_WIDTH - CELL_SIZE:
            obs[1] = 1
        if head[1] == self.snake.ENV_HEIGHT - CELL_SIZE:
            obs[2] = 1
        if head[0] == 0:
            obs[3] = 1
        new_obs = self.check_body(head, obs)
        return new_obs

    def check_body(self, head, obs):
        for i in range(1, len(self.snake.body)):
            snek = self.snake.body[i]
            if head[1] == snek[1] - CELL_SIZE:
                obs[0] = 1
            if head[0] == snek[0] + CELL_SIZE:
                obs[1] = 1
            if head[1] == snek[1] + CELL_SIZE:
                obs[2] = 1
            if head[0] == snek[0] - CELL_SIZE:
                obs[3] = 1
        return obs


    def apple_quad(self, apple, head):
         if apple[0] < head[0] and apple[1] < head[1]:
             #top left
             return 0
         if apple[0] >= head[0] and apple[1] < head[1]:
             #top right
             return 1
         if apple[0] >= head[0] and apple[1] >= head[1]:
             #bottom left
             return 2
         else:
             #bottom right
             return 3

    def dir_to_num(self, dir):
        if dir == "UP":
            return 0
        if dir == "RIGHT":
            return 1
        if dir == "DOWN":
            return 2
        if dir == "LEFT":
                return 3

    def num_to_dir(self, num):
        if num == 0:
            return "UP"
        if num == 1:
            return "RIGHT"
        if num == 2:
            return "DOWN"
        if num == 3:
            return "LEFT"

    def updateQ(self):
        gamma, Q, alpha = self.gamma, self.Q, self.alpha
        s_prime_row = self.Q[self.s_prime[0]]
        max_new_Q = s_prime_row.max()
        self.Q[self.s[0], self.a]  += alpha * (self.r + gamma * max_new_Q - Q[self.s[0], self.a])

    def getAppleDist(self):
        x, y = self.snake.getHeadLocation()
        apple = self.snake.getState()[1]
        new_dist = abs(x - apple[0]) + abs(y - apple[1])
        return new_dist

    def updateAppleDist(self, dist):
        self.old_dist = dist
    
    def gotCloser(self):
        new_dist = self.getAppleDist()
        if new_dist > self.old_dist:
            self.old_dist = new_dist
            return False
        else:
            self.old_dist = new_dist
            return True