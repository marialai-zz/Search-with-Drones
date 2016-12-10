UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

import random

class Drone: 
    
    def __init__(self,width, height):
        self.coordinates = Coordinates(0,0)
        #initial_x = random.randint(0,width-1)
        #initial_y = random.randint(0,height-1)
        # self.coordinates = Coordinates(initial_x, initial_y)
        DMap.board[self.coordinates.x][self.coordinates.y] += 1
        self.range = 2  #units of manhattan distance 
        # TO DO: speed, use radio range
        self.map= Map(width, height)
        self.N_TRANSMISSIONS = 0

    def __manhattan(self, directions, row_min, row_max, column_min, column_max):
        distance_dict = {'up': 0, 'down': 0, 'right': 0, 'left': 0}
        for key in [UP,DOWN,RIGHT,LEFT]:
            if not (key in directions):
                del distance_dict[key]
        for row in range(row_min, column_max):
            for column in range(column_min, column_max):
                if (self.map.board[row][column] == 1):
                    for key in distance_dict:
                        distance_dict[key] += abs(self.coordinates.x - row) + abs(self.coordinates.y - column)
        max_value = max(distance_dict.iteritems())[1]
        max_directions = []
        for key in distance_dict:
            if distance_dict[key] == max_value:
                max_directions.append(key)
        return max_directions[random.randint(0,len(directions)-1)]

    def move_logic(self,algo):
        # Obtain possible directions for Drone to move
        directions = drone.coordinates.getDirections(drone.coordinates)
        if algo == 'RANDOM':
            return directions[random.randint(0,len(directions)-1)]
        if algo == 'MANH_LOCAL':
            local_range = 3
            row_min = max([0, self.coordinates.x - local_range])
            row_max = min([self.map.width, self.coordinates.x + local_range])
            column_min = max([0, self.coordinates.y - local_range])
            column_max = min([self.map.height, self.coordinates.y + local_range])
            return self.__manhattan(directions, row_min, row_max, column_min, column_max)
        if algo == 'MANH_ALL':
            return self.__manhattan(directions, 0, self.map.width, 0, self.map.height)

    def move(self,direction):
        DMap.board[self.coordinates.x][self.coordinates.y] -= 1
        if direction == UP:
            coordinate = Coordinates(self.coordinates.x - 1, self.coordinates.y)
        else:
            if direction == DOWN:
                coordinate = Coordinates(self.coordinates.x + 1, self.coordinates.y)
            else:
                if direction == RIGHT:
                    coordinate = Coordinates(self.coordinates.x, self.coordinates.y + 1)
                else:
                    coordinate = Coordinates(self.coordinates.x, self.coordinates.y - 1)

        # Update coordinates after moved
        self.coordinates = coordinate
        DMap.board[self.coordinates.x][self.coordinates.y] += 1

        # Update Drone's individual map
        self.map.update([self.coordinates])

    def transmit(self):
        for drone in drones:
            if id(self) != id(drone):
                if (abs(self.coordinates.x - drone.coordinates.x) + abs(self.coordinates.y - drone.coordinates.y)) <= self.range:
                    self.N_TRANSMISSIONS += 1
                    for row in range(self.map.width):
                        for column in range(self.map.height):
                            if drone.map.board[row][column] == 1:
                                self.map.board[row][column] == 1

class Coordinates:
    
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    
    # Return all available valid directions that a drone can move to
    def getDirections(self,coordinates):
        self.x=coordinates.x
        self.y=coordinates.y
        directions=[]
        if(coordinates.x-1>=0):
            directions.append(UP)
        if(coordinates.y-1>=0):
            directions.append(LEFT)
        if(coordinates.x+1<HEIGHT):
            directions.append(DOWN)
        if(coordinates.y+1<WIDTH):
            directions.append(RIGHT)
        return directions

class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.overlaps = 0 # relevant for DMap
        self.board = []
        # Generate rows with length of width
        for row in range(self.height):
            self.board.append([])
            for column in range(self.width):
                # Assign 0 to each row
                self.board[row].append(0)

    def update (self,list_coordinates):
        # update board
        if len(list_coordinates)!=0:
            # change coordinate value to 1
            for coordinate in list_coordinates:
                self.board[coordinate.x][coordinate.y]=1 
    
    #print board
    def print_Map(self):
        for row in range(self.height):
            for column in range(self.width):
                print (str(self.board[row][column])),
            print "\n"


    #check if board is finished, applicable for universal map
    def finished(self):
        f=True
        for row in range(self.height):
            for column in range(self.width):
                   if (self.board[row][column]!=1):
                        f=False

        return f 

    # Relevant for DMap (DroneMap), after one set of moves, count overlaps
    def count_overlaps(self):
        for row in range(self.width):
            for column in range(self.height):
                if self.board[row][column] > 1:
                    self.overlaps += self.board[row][column] - 1

# Set width and height of map
WIDTH=15
HEIGHT=15

# Set number of drones
N_DRONES=3
# Set max number of steps
N_STEPS=5000

N_TRIALS = 200
ALGORITHM = "RANDOM"
# ALGORITHM = "MANH_LOCAL"
# ALGORITHM = "MANH_ALL"

print(ALGORITHM)

trial_times = []
trial_overlaps = []
trial_transmissions = []

for trial in range(N_TRIALS):

    # Initialize UniversalMap
    UMap= Map(WIDTH,HEIGHT)

    # Initialize DroneMap, which tracks locations of drones
    DMap = Map(WIDTH,HEIGHT)

    # List of drone objects
    drones=[]

    # Count step
    STEP=0 

    N_TRANSMISSIONS = 0

    for n in range(N_DRONES):
        drone=Drone(WIDTH,HEIGHT)
        drones.append(drone)

    # Simulation
    while(UMap.finished()!=True):

        # Move drones
        for drone in drones:
            # Update map based on drone's initial coordinates
            UMap.update([drone.coordinates])

            # Move Drone 
            # print('Drone coordinates: (' + str(drone.coordinates.x) + "," + str(drone.coordinates.y) + ")")
            d = drone.move_logic(ALGORITHM)
            # print ('Direction:' + d)
            drone.move(d)
            # Print Coordinates after Drone moves
            # print('Drone new coordinates: (' + str(drone.coordinates.x) + "," + str(drone.coordinates.y) + ")")

            # Update Drone map
            drone.map.update([drone.coordinates])
            # drone.map.print_Map()

            # Update Universal Map
            UMap.update([drone.coordinates])
            # UMap.print_Map() 

            # print ("done")
        for drone in drones:
            drone.transmit()
        # Update number of steps
        STEP += 1
        DMap.count_overlaps()
        if (STEP >= N_STEPS):
            break;
    
    trial_times.append(STEP)
    trial_overlaps.append(DMap.overlaps)
    for drone in drones:
        N_TRANSMISSIONS += drone.N_TRANSMISSIONS
    trial_transmissions.append(N_TRANSMISSIONS)
    print ('Trial ' + str(trial) + ': ' + str(STEP) + ' time steps. ' + str(DMap.overlaps) + ' overlaps. ' + str(N_TRANSMISSIONS) + ' transmissions')
print(ALGORITHM + ' Average Time: ' + str(sum(trial_times)/N_TRIALS) + ' time steps')
print(ALGORITHM + ' Average Overlap: ' + str(sum(trial_overlaps)/N_TRIALS) + ' overlaps')
print(ALGORITHM + ' Average # of Transmissions: ' + str(sum(trial_transmissions)/N_TRIALS))