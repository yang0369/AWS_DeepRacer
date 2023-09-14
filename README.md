# Enhancing Your AWS DeepRacer Performance with Gradient Descent Algorithm and Personalized Waypoints

## Showcase
![Alt Text]("./video.gif")

## DeepRacer
AWS DeepRacer is an innovative and exciting offering from Amazon Web Services (AWS) that combines the world of artificial intelligence and autonomous driving in a captivating and educational way. It is designed to provide developers, students, and enthusiasts with a hands-on experience in reinforcement learning, a powerful machine learning technique. With AWS DeepRacer, individuals can train and fine-tune autonomous racing cars using reinforcement learning algorithms and then compete in virtual or physical racing events.

This platform not only offers a fun and engaging way to explore the cutting-edge field of machine learning but also serves as a valuable tool for honing AI skills and fostering creativity in solving complex problems. Participants can experiment with various machine learning techniques, compete in global races, and even have the opportunity to qualify for the AWS DeepRacer League Championship. Overall, AWS DeepRacer is a thrilling introduction to the world of AI and autonomous systems.

## Repository Overview
In this repository, you'll discover a collection of reward functions, route calculations, and analytics that played a pivotal role in training my virtual car. With these efforts, my car achieved an impressive feat by completing three laps on the Invent:2018 track in 24.583 seconds! It's worth noting that there's still untapped potential to further enhance its performance with additional training hours.

If you're eager to dive into the world of DeepRacer, you can access the DeepRacer portal through this link: [DeepRacer Portal](https://us-east-1.console.aws.amazon.com/deepracer/home?region=us-east-1#welcome).

## Quick Tour
This repository is primarily organized into three main sections:

- Calculations: In this section, you can execute scripts that calculate the optimized racing line and determine the corresponding speeds and steering angles for the virtual car.

- Reward Functions: Here, you'll find a Python function that defines the reward system for rewarding good actions and behavior during training.

- Analytics: This section provides tools and scripts for analyzing the training logs, helping you gain insights into your virtual car's performance and progress.

To efficiently run the Python scripts, it is recommended to set up a separate environment using the provided requirement.txt file. Tech-savvy individuals can manually install the required dependencies using pip.

For users less familiar with technical details, you can effortlessly install all the necessary dependencies by executing the following command:
`pip install -r requirement.txt`

Please note that the reward function has been specifically tailored for the AWS DeepRacer Invent:2018 track. If you wish to customize it for other tracks or make modifications, you can follow the detailed sharing by [link].
## Calculate Optimized Route

The core of this approach hinges on the calculation of an optimized route, which draws inspiration from this repository: [Link to Repositor](https://github.com/dgnzlz/Capstone_AWS_DeepRacer), but has been tailored with some key modifications.

As I progressed through the training process, I encountered challenges related to the convergence of the calculated best route. Several factors contributed to this challenge:

- Incomplete Consideration of Simulation Factors: The initial calculation did not take into account all the underlying factors within the simulation. For instance, it did not consider the car's inability to abruptly decelerate from a speed of 4 to 1.5.

- Extended Convergence Time: Achieving a smooth convergence took a considerable amount of time, but due to limited training hours, it was not possible to train until full convergence was achieved.

- Track Discrepancy: The original track used by the author was "Spain_track," while our track is "re:Invent 2018." This difference led to certain parameters not being suitable for our specific track.


To enhance performance, I primarily implemented the following steps:

- Weightage Reallocation: I improved the performance by redistributing the weightage assigned to each action within the reward function, making it more effective.

- Speed Optimization: Specifically, I fine-tuned the speed settings for waypoints leading up to sharp U-turns, ensuring better overall performance.

- Enhanced Rewards: To encourage smoother U-turns, I introduced additional rewards for actions such as "strong_left" and "strong_right," promoting better maneuvering.
## Tips

Drawing from my own hands-on experimentation, I've compiled a set of valuable tips that can greatly aid in your model training process:

Reward Function Validation: Ensure the effectiveness of your reward function by meticulously analyzing your training logs using the "Analyze_Logs/Training_analysis.ipynb" tool.

U-Turn Smoothness: Work on modifying the speed and steering angle settings to achieve a smoother execution of U-turns. This can significantly enhance your model's performance.

Steering Penalty: Consider imposing a substantial penalty for high steering angles, especially when the car is operating at high speeds. Conversely, apply a less severe penalty when the car is moving at lower speeds.

Training Duration: Experiment with shorter training durations, such as half an hour instead of the usual 2 hours, and closely observe the progress. This can help you gauge how your model is evolving and whether adjustments are needed.
## Acknowledgement
My experience with training this model has been an absolute delight and a valuable learning journey. Not only did I gain practical insights into reinforcement learning, but I also had a blast doing it, thanks to the enjoyable racing game aspect. I want to extend my appreciation to the organizers for making this experience possible through their generosity (trainig hours are not cheap)!

I'd like to acknowledge the pivotal role played by the two authors, [dgnzlz](https://github.com/dgnzlz) and [GitHub User oscarYCL](https://github.com/oscarYCL), whose repositories, Capstone_AWS_DeepRacer and deepracer-waypoints-workshop, were instrumental references in completing this Git repository. Their creativity and contributions were invaluable.

Last but not least, this is a teamwork, I enjoyed working this model with my teammates.

## Reference
https://github.com/dgnzlz/Capstone_AWS_DeepRacer
https://github.com/oscarYCL/deepracer-waypoints-workshop
https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html
