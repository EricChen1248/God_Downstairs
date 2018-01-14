import pygame

keys = []

def add_keys(left, right):
    keys.append(Key(left, right))
    
class Key():
    def __init__(self, left, right):
        self.left = str_to_key(left.lower())
        self.right = str_to_key(right.lower())

def str_to_key(key):
    if key == 'left':
        return 276
    if key == 'right':
        return 275
    if key.isalpha():
        return ord(key)
    if key.isdigit():
        return 256 + int(key)