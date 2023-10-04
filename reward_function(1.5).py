# speed range: 1.5 - 4
import math


class Reward:
    def __init__(self):
        self.first_racingpoint_index = 0

    def reward_function(self, params):

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):

            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [
            [3.06664, 0.69989, 4.0, 0.03654],
            [3.21372, 0.69357, 4.0, 0.0368],
            [3.36169, 0.6893, 4.0, 0.03701],
            [3.51032, 0.68657, 4.0, 0.03716],
            [3.65944, 0.68518, 4.0, 0.03728],
            [3.80869, 0.68499, 4.0, 0.03731],
            [3.9577, 0.68593, 4.0, 0.03725],
            [4.10629, 0.688, 4.0, 0.03715],
            [4.25437, 0.69122, 4.0, 0.03703],
            [4.40189, 0.69562, 4.0, 0.0369],
            [4.54878, 0.70129, 4.0, 0.03675],
            [4.69495, 0.7083, 4.0, 0.03659],
            [4.84035, 0.71677, 3.4, 0.03641],
            [4.9849, 0.7268, 2.9, 0.03622],
            [5.12852, 0.73849, 2.9, 0.03602],
            [5.27111, 0.75197, 1.9, 0.03673],
            [5.41256, 0.76741, 1.9, 0.04065],
            [5.55265, 0.78511, 1.9, 0.04555],
            [5.69115, 0.80542, 1.9, 0.04999],
            [5.82783, 0.82863, 1.9, 0.05776],
            [5.96225, 0.85532, 1.8, 0.06526],
            [6.09384, 0.88621, 1.7, 0.07114],
            [6.22194, 0.92207, 1.6, 0.08314],
            [6.34568, 0.96381, 1.6, 0.08162],
            [6.46387, 1.01256, 1.6, 0.0799],
            [6.57482, 1.06969, 1.6, 0.078],
            [6.67653, 1.13638, 1.5, 0.08108],
            [6.76588, 1.21406, 1.5, 0.07893],
            [6.83839, 1.3035, 1.5, 0.07675],
            [6.8965, 1.40041, 1.5, 0.07534],
            [6.94112, 1.50274, 1.5, 0.07442],
            [6.96947, 1.60974, 1.5, 0.0738],
            [6.97707, 1.71948, 1.6, 0.06875],
            [6.96702, 1.82873, 1.6, 0.06857],
            [6.94149, 1.93565, 1.6, 0.0687],
            [6.90175, 2.03894, 1.6, 0.06917],
            [6.84699, 2.13674, 1.6, 0.07005],
            [6.77532, 2.22592, 1.8, 0.06356],
            [6.69013, 2.30621, 2.0, 0.05853],
            [6.59411, 2.37815, 2.3, 0.05217],
            [6.48935, 2.44258, 2.3, 0.0473],
            [6.37761, 2.50053, 3.0, 0.04196],
            [6.26056, 2.55329, 3.5, 0.03668],
            [6.13955, 2.60203, 4.0, 0.03262],
            [6.01585, 2.648, 4.0, 0.03299],
            [5.89082, 2.69257, 4.0, 0.03318],
            [5.76067, 2.73919, 4.0, 0.03456],
            [5.63058, 2.78629, 4.0, 0.03459],
            [5.5006, 2.83412, 4.0, 0.03462],
            [5.37081, 2.88295, 4.0, 0.03467],
            [5.2413, 2.93305, 4.0, 0.03472],
            [5.11223, 2.98473, 4.0, 0.03476],
            [4.9838, 3.03838, 4.0, 0.03479],
            [4.85635, 3.09451, 4.0, 0.03482],
            [4.73023, 3.15374, 4.0, 0.03483],
            [4.60596, 3.21695, 4.0, 0.03486],
            [4.48296, 3.2828, 4.0, 0.03488],
            [4.36104, 3.35081, 4.0, 0.0349],
            [4.24006, 3.42061, 4.0, 0.03492],
            [4.11988, 3.49191, 4.0, 0.03493],
            [4.00046, 3.56448, 4.0, 0.03494],
            [3.88179, 3.63809, 4.0, 0.03491],
            [3.76397, 3.71247, 3.5, 0.03981],
            [3.64724, 3.7873, 2.9, 0.04781],
            [3.53105, 3.86073, 2.5, 0.05498],
            [3.41419, 3.93239, 2.5, 0.05483],
            [3.29624, 4.00105, 2.5, 0.05459],
            [3.17677, 4.06545, 2.5, 0.05429],
            [3.0554, 4.12417, 2.5, 0.05393],
            [2.93169, 4.17515, 2.5, 0.05352],
            [2.80549, 4.21581, 2.8, 0.04735],
            [2.67785, 4.24822, 3.0, 0.04389],
            [2.5493, 4.27301, 2.9, 0.04515],
            [2.42021, 4.29067, 2.7, 0.04825],
            [2.29093, 4.30153, 2.5, 0.0519],
            [2.16175, 4.30562, 2.3, 0.05619],
            [2.03303, 4.30283, 2.0, 0.06438],
            [1.90519, 4.29292, 1.8, 0.07123],
            [1.7788, 4.27535, 1.6, 0.07975],
            [1.65459, 4.24957, 1.6, 0.07929],
            [1.53376, 4.21418, 1.6, 0.07869],
            [1.41797, 4.16786, 1.6, 0.07794],
            [1.30974, 4.10893, 1.6, 0.07702],
            [1.21287, 4.03538, 1.6, 0.07602],
            [1.13093, 3.94692, 1.7, 0.07093],
            [1.06435, 3.84609, 1.9, 0.06359],
            [1.01121, 3.73603, 2.1, 0.0582],
            [0.96999, 3.61869, 2.3, 0.05407],
            [0.93956, 3.49541, 2.5, 0.05079],
            [0.91891, 3.36729, 2.7, 0.04807],
            [0.90708, 3.23527, 2.9, 0.04571],
            [0.90334, 3.10018, 3.2, 0.04223],
            [0.90681, 2.9629, 3.3, 0.04161],
            [0.91698, 2.82419, 3.5, 0.03974],
            [0.93341, 2.68483, 3.6, 0.03898],
            [0.95571, 2.54557, 3.6, 0.03918],
            [0.98342, 2.40706, 3.4, 0.04155],
            [1.01626, 2.26986, 3.2, 0.04409],
            [1.05392, 2.13444, 2.9, 0.04847],
            [1.09624, 2.00121, 2.7, 0.05177],
            [1.14311, 1.87057, 2.4, 0.05783],
            [1.19482, 1.7431, 2.1, 0.0655],
            [1.25158, 1.61938, 1.9, 0.07164],
            [1.31382, 1.50015, 1.9, 0.07079],
            [1.38221, 1.38643, 1.9, 0.06984],
            [1.45757, 1.27943, 1.9, 0.06888],
            [1.54096, 1.18072, 1.9, 0.06801],
            [1.63386, 1.09253, 1.9, 0.06742],
            [1.7384, 1.01844, 2.2, 0.05824],
            [1.85098, 0.955, 2.4, 0.05384],
            [1.97002, 0.90067, 2.6, 0.05033],
            [2.09459, 0.85453, 2.9, 0.0458],
            [2.2239, 0.81579, 3.1, 0.04354],
            [2.35729, 0.78373, 3.3, 0.04157],
            [2.49419, 0.75767, 3.6, 0.03871],
            [2.63406, 0.73695, 4.0, 0.03535],
            [2.77639, 0.72086, 4.0, 0.03581],
            [2.92074, 0.70874, 4.0, 0.03621]]

        # planned speed based on waypoints
        # manually adjust the list for better performance, e.g. lower the speed before turning
        above_three_five = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 93, 94, 95, 114, 115, 116, 117, 118]
        above_three = [12, 41, 71, 91, 92, 96, 97, 112, 113]
        above_two_five = [13, 14, 40, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 88, 89, 90, 98, 99, 110, 111]
        above_two = [38, 39, 75, 76, 86, 87, 100, 101, 108, 109]
        below_two = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 77, 78, 79, 80, 81, 82, 83, 84, 85, 102, 103, 104, 105, 106, 107]
        # planned speed based on waypoints
        # observe which side the car is expected to run at
        right_track = [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
        center_track = [118, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 47, 61]
        left_track = [i for i in range(0, 119) if i not in right_track + center_track]

        # obvious sides
        strong_left = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
        strong_right = [50, 51, 52, 53, 54, 55, 56]

        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        x = params['x']
        y = params['y']
        distance_from_center = params['distance_from_center']
        is_left_of_center = params['is_left_of_center']
        heading = params['heading']
        progress = params['progress']
        steps = params['steps']
        speed = params['speed']
        steering_angle = abs(params['steering_angle'])
        track_width = params['track_width']
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################
        reward = 1e-3

        # Zero reward if off track ##
        if is_offtrack is True:
            return reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            return reward

        # Reward if car goes close to optimal racing line
        def get_distance_reward(threshold, distance, multiplier):
            distance_reward = max(0, 1 - (distance / threshold))

            return distance_reward * multiplier

        DIST_THRESH = track_width * 0.5
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])

        if (distance_from_center < 0.01 * track_width):
            if closest_index in center_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
        elif is_left_of_center:
            if closest_index in left_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_left:
                reward += get_distance_reward(DIST_THRESH, dist, 5)
        else:
            if closest_index in right_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_right:
                reward += get_distance_reward(DIST_THRESH, dist, 5)

        def get_speed_reward(ceiling, threshold, diff):
            return ceiling - diff/threshold

        # Reward if speed falls within optimal range
        PENALTY_RATIO = 0.9
        SPEED_DIFF_NO_REWARD = 1
        speed_diff = abs(optimals[2]-speed)
        if speed_diff > SPEED_DIFF_NO_REWARD:
            return 1e-3

        if closest_index in above_three_five:
            if speed >= 3.5:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 3:
                reward *= PENALTY_RATIO
        elif closest_index in above_three:
            if speed >= 3:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 8:
                reward *= PENALTY_RATIO
        elif closest_index in above_two_five:
            if speed >= 2.5:
                reward += get_speed_reward(0.8, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 15:
                reward *= PENALTY_RATIO
        elif closest_index in above_two:
            if speed >= 2:
                reward += get_speed_reward(1, SPEED_DIFF_NO_REWARD, speed_diff)
        else:
            if speed < 2:
                reward += get_speed_reward(3, SPEED_DIFF_NO_REWARD, speed_diff)

        # Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 2000 # should be adapted to track length and other rewards
        TARGET_STEPS = 110
        if progress == 100:
            reward += REWARD_FOR_FASTEST_TIME / (steps - TARGET_STEPS)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()


def reward_function(params):
    return reward_object.reward_function(params)
