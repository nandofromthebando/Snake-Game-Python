#!/usr/bin/env python3

import curses
from random import randint

#setup window
curses.initscr()
win = curses.newwin(20, 60, 0, 0) 
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1) #-1 

#snake and food 
snake = [(4,10), (4,9), (4,8)]
food = (10,20)

win.addch(food[0], food[1], '$')
#game logic
score = 0

def check_obstacle_collision(snake, obstacles):
    head = snake[0]
    if head in obstacles:
        return True
    return False

#esc key is defined as key 27
ESC = 27
key = curses.KEY_RIGHT

#implementation of level changes 
levels = [
    {"name": "Easy", "speed": 200, "obstacles": [[(5, 5), (5, 6), (5, 7)], [(10, 15), (10, 16), (10, 17)]], "target_length": 5},
    {"name": "Medium", "speed": 150, "obstacles": [[(8, 8), (8, 9)], [(12, 12), (12, 13), (12, 14)], [(5, 15), (5, 16)]], "target_length": 10},
    {"name": "Hard", "speed": 100, "obstacles": [[(5, 15), (5, 16), (5, 17)], [(10, 5), (10, 6), (10, 7)], [(7, 7), (7, 8), (7, 9)]], "target_length": 15},
]

#intitialize
current_level = 0
level = levels[current_level]
difficulty = level["name"]
win.timeout(level["speed"])
target_length = level["target_length"]
obstacles = level["obstacles"]

while key != ESC:
    # Display current difficulty level and target length
    win.addstr(0, 2, 'Level: ' + difficulty)
    win.addstr(1, 2, 'Target Length: ' + str(target_length))
    win.addstr(2, 2, 'Score: ' + str(score))  # Display the score separately

    # Adjust game speed based on difficulty
    if difficulty == 'easy':
        win.timeout(200)
    elif difficulty == 'medium':
        win.timeout(150)
    elif difficulty == 'hard':
        win.timeout(100)

    for cluster in obstacles:
        for obstacle in cluster:
            y, x = obstacle
            win.addch(y, x, '#')

    if check_obstacle_collision(snake, cluster):
        # Handle collision with obstacles 
        if len(snake) > 1:
            snake.pop()  # Remove the last segment of the snake
        else:
            # Snake has only one segment, game over logic can be added here
            break

    # Check if snake's length reaches the target for the current level
    if len(snake) >= target_length:
        if current_level < len(levels) - 1:
            current_level += 1
            level = levels[current_level]
            difficulty = level["name"]
            target_length = level["target_length"]
            obstacles = level["obstacles"]
            win.timeout(level["speed"])  # Adjust the game speed for the new level
        else:
            # You've completed all levels (end of the game)
            break

    win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) #THis function adjust speed

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

    #Calculate next coordinates for snake
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1
    snake.insert(0, (y,x)) #append 0(n)
#check if we hit the border
    if y == 0: break
    if y == 19: break
    if x == 0: break
    if x == 59: break

    #if snake runs over itself
    if snake[0] in snake[1:]: break 
    if snake[0] == food:
        #eat the food
        score += 1
        food = ()
        while food == ():
            food = (randint(1,18), randint(1,58))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '$')
#move snake
    else: 
        last = snake.pop()
        win.addch(last[0], last[1], ' ')
    
    win.addch(snake[0][0], snake[0][1], 'o')
    
curses.endwin()
print (f"Final Score = {score}")