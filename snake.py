import os
import pygame
import numpy as np
import time
import keyboard
from random import randint

from utilities.input_manager import InputManager
from utilities.display import Color, Frame
from utilities.dummy import DummyDisplay

FPS = 30 # Screen refresh rate (CANNOT BE MODIFIED)
SIM_RATE = 1000 # Handle inputs at 1 kHz

NS_PER_FRAME = 1_000_000_000 // FPS
NS_PER_SUBTICK = 1_000_000_000 // SIM_RATE

# Defining some colours
SNAKE = Color(50, 240, 0) # Green snake
HEAD = Color(10, 150, 0) # Darker snake head
FOOD = Color(240, 50, 0) # Red food

# Defining some directions (top-left = 0,0)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

class Snake:
    def __init__(self, display=None):
        KEYBINDS = {
            pygame.K_UP: self._dirUp,
            pygame.K_DOWN: self._dirDown,
            pygame.K_LEFT: self._dirLeft,
            pygame.K_RIGHT: self._dirRight,
            pygame.K_RETURN: self._pause,
            pygame.K_BACKSPACE: self._restart
        }

        self._display = display if display is not None else DummyDisplay()
        self._displayFrame = self._display.makeframe()

        self._inputManager = InputManager(KEYBINDS)

        self._resetGame()

    def play(self):
        while True:
            self._frames += 1
            frameTime = time.perf_counter()
            while time.perf_counter() - frameTime < 1/FPS:
                simTime = time.perf_counter()
                self._inputManager.process_events()

                while time.perf_counter() - simTime < 1/SIM_RATE:
                    pass # wait until next subtick
            
            # move snake every 5 frames (6 fps)
            if self._frames % 5 == 0 and self._alive:
                self._moveSnake()

            self._updateDisplayFrame()
            self._display.send(self._displayFrame)

    def _moveSnake(self):
        oldHead = self._snake[0]
        newHead = ((oldHead[0] + self._dir[0]) % 17, (oldHead[1] + self._dir[1]) % 9)

        if newHead in self._snake:
            #self._snake = None
            self._food = None
            self._alive = False
        elif newHead == self._food:
            self._snake = [newHead] + self._snake
            self._makeNewFood()
        else:
            self._snake = [newHead] + self._snake[:-1]

    def _makeNewFood(self):
        while self._food in self._snake:
            self._food = (randint(0, 16), randint(0, 9))

    def _updateDisplayFrame(self):
        newFrame = Frame()
        if self._food is not None:
            newFrame[self._food] = FOOD
        if self._snake is not None:
            newFrame[self._snake[0]] = HEAD
            for cell in self._snake[1:]:
                newFrame[cell] = SNAKE
        if not self._alive:
            pass # game over screen here

        self._displayFrame[:] = newFrame[:]

    def _dirUp(self, eventDown):
        if self._dir != DOWN and self._lcFrame < self._frames and eventDown:
            self._lcFrame = self._frames
            self._dir = UP
    def _dirDown(self, eventDown):
        if self._dir != UP and self._lcFrame < self._frames and eventDown:
            self._lcFrame = self._frames
            self._dir = DOWN
    def _dirLeft(self, eventDown):
        if self._dir != RIGHT and self._lcFrame < self._frames and eventDown:
            self._lcFrame = self._frames
            self._dir = LEFT
    def _dirRight(self, eventDown):
        if self._dir != LEFT and self._lcFrame < self._frames and eventDown:
            self._lcFrame = self._frames
            self._dir = RIGHT
    
    def _pause(self):
        pass # impl later

    def _restart(self):
        pass # impl later
    
    def _resetGame(self):
        self._snake = [(5, 4), (6, 4), (7, 4)]
        self._food = (10, 2)
        self._alive = True
        self._dir = UP
        self._frames = 0
        self._lcFrame = 0
        self.score = 0

if __name__ == "__main__":
    snake = Snake()
    snake.play()
