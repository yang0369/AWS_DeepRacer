# AWS DeepRacer Experiments

# DeepRacer

# About This Repo

This repository includes all my reward functions, route calculations and analytics. By them, I trained a virtual car which finished three laps for Invent:2018 track in 25.798 seconds.

# Quick Tour
This repo includes mainly three parts:

- Calculations: run the scripts to calculate the optimized racing line, and corresponding (speeds, steering angle)
- Reward Functions: a python function defines all the reward for good actions
- Analytics: use this to analyse the training logs

To run the python scripts, it's recommended to create a separated environment using the requirement.txt.

For tech guru, you can just pip install all the dependencies yourself.

For non-tech users, you can simply run this command:
`pip install -r requirement.txt`

Note the reward function is only applicable to AWS DeepRacer Invent:2018 track, for customization or other tracks, follow the detailed guidelines below.
# Calculate Optimized Route



# Tips

1. validate if your reward function is working by analysing logs

2. Modify Speed to get a smooth U-turn
- modify the planned speed
- assign more reward to waypoints before sharp U-turn

3. Heavy penalty for steering angle at highspeed while less penalty for low speed
The logic is that low speed usually is to prepare for a sharp turn, so the steering angle may be larger than expected

4. Train by shorter time and observe if it is progressing


# Acknowledgement



# Reference
https://github.com/dgnzlz/Capstone_AWS_DeepRacer
