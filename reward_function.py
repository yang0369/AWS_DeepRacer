# speed: 1.5 - 4
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

        # Gives back indexes that lie between start and end index of a cyclical list
        # (start index is included, end index is not)
        def indexes_cyclical(start, end, array_len):

            if end < start:
                end += array_len

            return [index % array_len for index in range(start, end)]

        # Calculate how long car would take for entire lap, if it continued like it did until now
        def projected_time(first_index, closest_index, step_count, times_list):

            # Calculate how much time has passed since start
            current_actual_time = (step_count-1) / 15

            # Calculate which indexes were already passed
            indexes_traveled = indexes_cyclical(first_index, closest_index, len(times_list))

            # Calculate how much time should have passed if car would have followed optimals
            current_expected_time = sum([times_list[i] for i in indexes_traveled])

            # Calculate how long one entire lap takes if car follows optimals
            total_expected_time = sum(times_list)

            # Calculate how long car would take for entire lap, if it continued like it did until now
            try:
                projected_time = (current_actual_time/current_expected_time) * total_expected_time
            except:
                projected_time = 9999

            return projected_time

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [
            [3.07252, 0.71197, 4.0, 0.03617],
            [3.21818, 0.70312, 4.0, 0.03648],
            [3.36499, 0.69661, 4.0, 0.03674],
            [3.5127, 0.69201, 4.0, 0.03695],
            [3.66113, 0.68908, 4.0, 0.03711],
            [3.80992, 0.68773, 4.0, 0.0372],
            [3.95858, 0.68789, 4.0, 0.03717],
            [4.10683, 0.68949, 4.0, 0.03707],
            [4.25451, 0.69258, 4.0, 0.03693],
            [4.40148, 0.6972, 4.0, 0.03676],
            [4.54765, 0.70341, 4.0, 0.03658],
            [4.69294, 0.71127, 4.0, 0.03637],
            [4.83726, 0.72083, 4.0, 0.03616],
            [4.98057, 0.73216, 4.0, 0.03594],
            [5.12278, 0.74533, 4.0, 0.0357],
            [5.26378, 0.76046, 4.0, 0.03545],
            [5.40346, 0.77771, 3.6, 0.03909],
            [5.54164, 0.79728, 3.3, 0.04229],
            [5.67809, 0.81945, 2.9, 0.04767],
            [5.81249, 0.84462, 2.5, 0.0547],
            [5.94446, 0.87323, 2.2, 0.06138],
            [6.07348, 0.90586, 1.9, 0.07004],
            [6.19889, 0.94318, 1.7, 0.07697],
            [6.32, 0.98584, 1.7, 0.07553],
            [6.43556, 1.03498, 1.7, 0.07386],
            [6.54389, 1.09189, 1.7, 0.07198],
            [6.64298, 1.15771, 1.5, 0.07931],
            [6.73021, 1.23339, 1.5, 0.07699],
            [6.80235, 1.31919, 1.5, 0.07473],
            [6.85914, 1.41276, 1.5, 0.07297],
            [6.90312, 1.51126, 1.5, 0.07192],
            [6.93131, 1.61419, 1.5, 0.07114],
            [6.93908, 1.71981, 1.6, 0.06619],
            [6.92884, 1.82494, 1.7, 0.06213],
            [6.90388, 1.9279, 1.7, 0.06232],
            [6.86525, 2.02755, 1.7, 0.06287],
            [6.81052, 2.12148, 1.7, 0.06395],
            [6.74027, 2.20778, 1.9, 0.05857],
            [6.65743, 2.28638, 2.1, 0.05438],
            [6.56437, 2.3578, 2.4, 0.04888],
            [6.4629, 2.42269, 2.7, 0.04461],
            [6.35458, 2.48188, 3.1, 0.03982],
            [6.24098, 2.53647, 3.7, 0.03406],
            [6.12352, 2.58757, 4.0, 0.03203],
            [6.00338, 2.63622, 4.0, 0.0324],
            [5.88149, 2.68353, 4.0, 0.03269],
            [5.75405, 2.73483, 4.0, 0.03435],
            [5.62676, 2.78767, 4.0, 0.03446],
            [5.49979, 2.84179, 4.0, 0.03451],
            [5.37316, 2.89706, 4.0, 0.03454],
            [5.24688, 2.95343, 4.0, 0.03457],
            [5.12095, 3.01083, 4.0, 0.0346],
            [4.99539, 3.06922, 4.0, 0.03462],
            [4.87022, 3.12861, 4.0, 0.03464],
            [4.74547, 3.18905, 4.0, 0.03465],
            [4.62128, 3.25078, 4.0, 0.03467],
            [4.49758, 3.31359, 4.0, 0.03468],
            [4.37434, 3.37734, 4.0, 0.03469],
            [4.25151, 3.44192, 4.0, 0.03469],
            [4.12906, 3.50724, 4.0, 0.03469],
            [4.007, 3.57327, 4.0, 0.03469],
            [3.88534, 3.63999, 4.0, 0.03469],
            [3.76412, 3.70742, 3.6, 0.03853],
            [3.64354, 3.77556, 3.1, 0.04468],
            [3.52557, 3.84345, 2.7, 0.05041],
            [3.40739, 3.91, 2.7, 0.05023],
            [3.28852, 3.97416, 2.7, 0.05003],
            [3.16856, 4.03438, 2.7, 0.04971],
            [3.04718, 4.08908, 2.7, 0.04931],
            [2.92416, 4.13646, 2.7, 0.04883],
            [2.79955, 4.17448, 3.0, 0.04343],
            [2.67408, 4.2049, 3.1, 0.04165],
            [2.54812, 4.22834, 3.0, 0.04271],
            [2.42195, 4.24527, 2.8, 0.04546],
            [2.29581, 4.25602, 2.5, 0.05064],
            [2.16992, 4.26063, 2.3, 0.05477],
            [2.04455, 4.25905, 2.0, 0.06269],
            [1.92002, 4.25101, 1.8, 0.06933],
            [1.79674, 4.23603, 1.7, 0.07305],
            [1.67542, 4.21301, 1.7, 0.07264],
            [1.55714, 4.18053, 1.7, 0.07215],
            [1.44347, 4.13709, 1.7, 0.07158],
            [1.33691, 4.08077, 1.7, 0.0709],
            [1.24136, 4.0094, 1.7, 0.07015],
            [1.1602, 3.92306, 1.8, 0.06583],
            [1.09331, 3.82474, 1.9, 0.06259],
            [1.03917, 3.71725, 2.1, 0.05731],
            [0.99642, 3.60245, 2.3, 0.05326],
            [0.96403, 3.48165, 2.5, 0.05002],
            [0.94121, 3.35589, 2.7, 0.04734],
            [0.92724, 3.22604, 2.9, 0.04503],
            [0.92146, 3.09299, 3.1, 0.04296],
            [0.92331, 2.95759, 3.3, 0.04104],
            [0.9321, 2.82071, 3.5, 0.03919],
            [0.94745, 2.68318, 3.6, 0.03844],
            [0.96904, 2.54578, 3.6, 0.03863],
            [0.99659, 2.40927, 3.5, 0.03979],
            [1.02977, 2.2743, 3.3, 0.04212],
            [1.06829, 2.14139, 3.0, 0.04613],
            [1.11191, 2.01097, 2.8, 0.04911],
            [1.16042, 1.88339, 2.5, 0.0546],
            [1.2138, 1.75904, 2.2, 0.06151],
            [1.27204, 1.63828, 2.0, 0.06703],
            [1.3356, 1.52185, 2.0, 0.06633],
            [1.40513, 1.41071, 2.0, 0.06555],
            [1.48131, 1.30595, 2.0, 0.06477],
            [1.56515, 1.20911, 2.0, 0.06405],
            [1.65806, 1.12235, 2.0, 0.06356],
            [1.7618, 1.04875, 2.3, 0.0553],
            [1.87337, 0.98546, 2.5, 0.05131],
            [1.99122, 0.93094, 2.8, 0.04638],
            [2.11433, 0.88409, 3.1, 0.04249],
            [2.24181, 0.84389, 3.3, 0.04051],
            [2.37316, 0.80979, 3.5, 0.03877],
            [2.50791, 0.78125, 3.8, 0.03625],
            [2.64562, 0.75775, 4.0, 0.03493],
            [2.7859, 0.73875, 4.0, 0.03539],
            [2.92832, 0.72368, 4.0, 0.03581]]

        # planned speed based on waypoints
        above_three_five = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 93, 94, 95, 96, 113, 114, 115, 116, 117, 118]
        above_three = [17, 41, 63, 70, 71, 72, 91, 92, 97, 98, 111, 112]
        above_two_five = [18, 19, 40, 64, 65, 66, 67, 68, 69, 73, 74, 88, 89, 90, 99, 100, 109, 110]
        above_two = [20, 38, 39, 75, 76, 86, 87, 101, 102, 103, 104, 105, 106, 107, 108]
        right_track = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
        center_track = [1, 2, 3, 4, 5, 6, 7, 8, 9, 47, 61]
        left_track = [i for i in range(0, 119) if i not in right_track + center_track]
        strong_left = [
            17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
            65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
            101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
        ]
        strong_right = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58]

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
        DISTANCE_MULTIPLE = 3
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
        distance_reward = max(0, 1 - (dist/(track_width*0.2)))
        reward += distance_reward * DISTANCE_MULTIPLE

        # Reward if car goes correct side of track
        if (distance_from_center < 0.01 * track_width):
            if closest_index in center_track:
                reward += 1
        elif is_left_of_center:
            if closest_index in left_track:
                reward += 1
            if closest_index in strong_left:
                reward += 1
        else:
            if closest_index in right_track:
                reward += 1
            if closest_index in strong_right:
                reward += 1

        # Reward if speed is close to optimal speed
        SPEED_REWARD = 2
        SPEED_DIFF_NO_REWARD = 1
        speed_diff = abs(optimals[2]-speed)
        if speed_diff > SPEED_DIFF_NO_REWARD:
            return 1e-3
        speed_reward = SPEED_REWARD - speed_diff/(SPEED_DIFF_NO_REWARD)
        reward += speed_reward

        # Reward if speed falls within optimal range
        PENALTY_RATIO = 0.5
        if closest_index in above_three_five:
            if speed >= 3.5:
                reward += 0.5
            if steering_angle > 3.5:
                reward *= PENALTY_RATIO
        elif closest_index in above_three:
            if speed >= 3:
                reward += 0.5
            if steering_angle > 5:
                reward *= PENALTY_RATIO
        elif closest_index in above_two_five:
            if speed >= 2.5:
                reward += 0.5
            if steering_angle > 8:
                reward *= PENALTY_RATIO
        elif closest_index in above_two:
            if speed >= 2:
                reward += 0.5
            if steering_angle > 13:
                reward *= PENALTY_RATIO
        else:
            if speed < 2:
                reward += 0.5
            if steering_angle > 18:
                reward *= PENALTY_RATIO

        # # Reward if less steps
        # STANDARD_TIME = 11  # seconds (time that is easily done by model)
        # FASTEST_TIME = 8  # seconds (best time of 1st place on the track)
        # REWARD_PER_STEP_FOR_FASTEST_TIME = 1
        # times_list = [row[3] for row in racing_track]
        # projected_time = projected_time(self.first_racingpoint_index, closest_index, steps, times_list)
        # try:
        #     steps_prediction = projected_time * 15 + 1
        #     reward_prediction = max(1e-3, (-REWARD_PER_STEP_FOR_FASTEST_TIME*(FASTEST_TIME) /
        #                                    (STANDARD_TIME-FASTEST_TIME))*(steps_prediction-(STANDARD_TIME*15+1)))
        #     steps_reward = min(REWARD_PER_STEP_FOR_FASTEST_TIME, reward_prediction / steps_prediction)
        # except:
        #     steps_reward = 0
        # reward += steps_reward

        # Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 1000 # should be adapted to track length and other rewards
        TARGET_STEPS = 110
        if progress == 100:
            reward += REWARD_FOR_FASTEST_TIME / (steps - TARGET_STEPS)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()


def reward_function(params):
    return reward_object.reward_function(params)
